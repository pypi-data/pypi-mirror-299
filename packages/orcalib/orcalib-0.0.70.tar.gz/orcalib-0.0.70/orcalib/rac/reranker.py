from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, TypedDict, cast

import torch
from sentence_transformers import CrossEncoder
from torch import Tensor, nn
from torch.utils.data import Dataset
from transformers import EarlyStoppingCallback, Trainer, TrainingArguments

from orcalib.torch_layers import CosineSimilarity, SentenceEmbeddingGenerator


class SamplePair(TypedDict):
    query_text: str
    memory_text: str
    label_match: bool


class MemoryPairsDataset(Dataset):
    def __init__(
        self,
        samples: list[tuple[str, int]],
        lookup_fn: Callable[[str, int], list[tuple[str, int]]],
        num_memories: int,
    ):
        self.lookup_fn = lookup_fn
        self.num_samples = len(samples)
        self.num_memories = num_memories
        self.samples = samples
        self.memories: dict[int, list[tuple[str, int]]] = {}

    def __len__(self) -> int:
        return self.num_samples * self.num_memories

    def __getitem__(self, idx: int) -> SamplePair:
        assert isinstance(idx, int)
        i = idx // self.num_memories
        memory_offset = idx % self.num_memories
        query_text, query_label = self.samples[i]
        if i not in self.memories:
            self.memories[i] = self.lookup_fn(query_text, self.num_memories)
        memory_text, memory_label = self.memories[i][memory_offset]
        return SamplePair(query_text=query_text, memory_text=memory_text, label_match=query_label == memory_label)

    def split(self, test_samples: int) -> tuple[MemoryPairsDataset, MemoryPairsDataset]:
        shuffled_indices = torch.randperm(len(self.samples)).tolist()
        indices = dict(test=shuffled_indices[:test_samples], train=shuffled_indices[test_samples:])
        return (
            MemoryPairsDataset(
                [s for i, s in enumerate(self.samples) if i in indices["train"]], self.lookup_fn, self.num_memories
            ),
            MemoryPairsDataset(
                [s for i, s in enumerate(self.samples) if i in indices["test"]], self.lookup_fn, self.num_memories
            ),
        )


@dataclass
class RerankResult:
    scores: list[float]
    """The scores of the reranked memories."""
    indices: list[int]
    """The indices of the reranked memories in the original list."""


# TODO: make this class contain all reranker architectures instead of implementing them as subclasses
class Reranker(ABC):
    """
    A reranker is a model that reranks a list of memories for a given query.
    """

    compression: int

    @abstractmethod
    def rerank(self, query: str, memories: list[str], top_k: int | None = None) -> RerankResult:
        """
        Rerank the memories for the given query.

        Args:
            query: The query with which the memories were retrieved.
            memories: The texts of the memories to rerank.
            top_k: The number of memories to return. If None, all memories are returned.

        Returns:
            The reranked memories in the order of their scores.
        """
        pass

    @abstractmethod
    def finetune(
        self,
        dataset: MemoryPairsDataset,
        output_dir: str = "./temp/reranker",
        training_args: TrainingArguments | None = None,
    ) -> None:
        """
        Fit the reranker to the given memories and labels.
        """
        pass


class CrossEncoderReranker(Reranker):
    def __init__(self, base_model: str):
        super().__init__()
        # TODO: enable custom pretrained models and models without pretrained classification heads
        self.model = CrossEncoder(base_model)

    def rerank(self, query: str, memories: list[str], top_k: int | None = None) -> RerankResult:
        res = self.model.rank(query, memories, top_k=top_k)
        scores = [cast(float, r["score"]) for r in res]
        indices = [cast(int, r["corpus_id"]) for r in res]
        return RerankResult(scores, indices)

    # TODO: add ability to fine tune cross encoders


# TODO: add method to cache reranker embeddings
class SharedEncoderReranker(Reranker, nn.Module):
    trainer: Trainer | None = None

    def __init__(self, base_model: str, compression=5):
        super().__init__()
        self.compression = compression
        self.encoder = SentenceEmbeddingGenerator(base_model, frozen=False)
        self.head = CosineSimilarity()
        self.criterion = nn.BCEWithLogitsLoss()

    def forward(
        self,
        query_ids: Tensor,
        query_mask: Tensor,
        memory_ids: Tensor,
        memory_mask: Tensor,
        labels: Tensor | None = None,
    ):
        query_embeds = self.encoder(query_ids, query_mask)  # batch_size x embedding_dim
        memory_embeds = self.encoder(memory_ids, memory_mask)  # batch_size x embedding_dim
        scores = self.head(query_embeds, memory_embeds)  # batch_size
        return dict(
            scores=scores,
            loss=self.criterion(scores, labels) if labels is not None else None,
        )

    @torch.no_grad()
    def score(self, query: str, memories: list[str]) -> Tensor:
        query_ids, query_mask = self.encoder.tokenize(query, return_tensors=True)
        memory_ids, memory_mask = self.encoder.tokenize(memories, return_tensors=True)
        return self.forward(query_ids, query_mask, memory_ids, memory_mask)["scores"]  # num_memories

    # TODO: allow passing in cached memory embeddings
    @torch.no_grad()
    def rerank(self, query: str, memories: list[str], top_k: int | None = None) -> RerankResult:
        scores = self.score(query, memories)
        indices = (torch.topk(scores, k=top_k).indices if top_k is not None else scores.argsort()).tolist()
        return RerankResult(scores[indices].tolist(), indices)

    def finetune(
        self,
        dataset: MemoryPairsDataset,
        output_dir: str = "./temp/reranker",
        training_args: TrainingArguments | None = None,
    ) -> None:
        train_dataset, eval_dataset = dataset.split(
            min(len(dataset.samples) // 10, 5000 // dataset.num_memories)
        )  # 10% of dataset capped at 5000 ultimate samples

        # using a fixed sequence length is not ideal, but required with HF trainer for no good reason
        max_sequence_length = self.encoder.get_max_sequence_length([e[0] for e in dataset.samples])

        def collate_fn(batch: list[SamplePair]) -> dict[str, Tensor]:
            query_ids, query_mask = self.encoder.tokenize(
                [b["query_text"] for b in batch], sequence_length=max_sequence_length, return_tensors=True
            )
            memory_ids, memory_mask = self.encoder.tokenize(
                [b["memory_text"] for b in batch], sequence_length=max_sequence_length, return_tensors=True
            )
            labels = torch.tensor([1.0 if b["label_match"] else 0.0 for b in batch]).to(self.encoder.device)
            return dict(
                query_ids=query_ids,
                query_mask=query_mask,
                memory_ids=memory_ids,
                memory_mask=memory_mask,
                labels=labels,
            )

        self.trainer = Trainer(
            model=self,
            args=TrainingArguments(
                output_dir=output_dir,
                eval_steps=200,
                save_steps=200,
                per_device_train_batch_size=32,
                per_device_eval_batch_size=32,
                weight_decay=0.01,
                num_train_epochs=1,
                learning_rate=1e-5,
                logging_steps=20,
                warmup_steps=20,
                **training_args.to_dict() if training_args is not None else {},
                # the following parameters cannot be overridden by the user
                eval_strategy="steps",
                save_strategy="steps",
                metric_for_best_model="eval_loss",
                greater_is_better=False,
                load_best_model_at_end=True,
                save_total_limit=2,
                remove_unused_columns=False,
            ),
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],
            data_collator=collate_fn,
        )
        self.trainer.train()
