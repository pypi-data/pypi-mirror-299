# Retrieval Augmented Classification (RAC)

RAC is a set of tools that streamline configuring and tuning an Orca classification model.

The basic workflow is as follows:

1. Create a memoryset
2. Import data
3. Insert data into memoryset
4. Create a RAC model
5. Evaluate / Finetune model
6. Save pretrained model

## Setup

### Create Memoryset

Connect to an Orca instance with your api keys and configure the database to store a memoryset.

To keep your credentials secure, we recommend storing them in environment variables and not checking them into source control. You can use a tool like [dotenv](https://saurabh-kumar.com/python-dotenv/) to make this easy during local development.

```
import os
import dotenv

dotenv.load_dotenv()

api_key=os.getenv("ORCADB_API_KEY")
secret_key=os.getenv("ORCADB_SECRET_KEY")
endpoint=os.getenv("ORCADB_ENDPOINT")

memoryset = LabeledMemoryset(uri=f"{endpoint}/database_name#table_name",api_key,secret_key)
```

The `uri` field allows specifying the table name as a memory. You can also pass in a specific embedding model if you don't want to use the default (CLIP)

For testing purposes the uri can be set to a `file://databasename#tablename` value and RAC will create a local file-based lanceDB database. This convenience method is not as fully featured as an Orca instance and not intended for production use.

### Load dataset

Importing data from HuggingFace is very straightforward:

```
from datasets import load_dataset

ds = load_dataset("frgfm/imagenette", "320px")
```

Additionally datasets can be loaded from a wide variety of data structures:

- Pandas dataframe
- list[tuple[InputType, int]]
- Dataset
- TorchDataset
- TorchDataLoader
- dict
- list[dict]

Most formats except for the list of tuples will require specific keys to be present before inserting into a memoryset. More details below.

### Insert data into Memoryset

Data can be inserted into a memoryset with the syntax below. RAC expects memoryset rows to have one `label` column and one of either `value`, `image`, or `text` columns. If a row has exactly two columns with one named `label` it will infer that the other is `value`. If there are > 2 columns without `label` and one of `value`, `image`, or `text` then it will require renaming.

```
memoryset.insert(ds['train'])
```

### Create a RAC model

`num_classes` is the only required arguments to create a RAC model. However, you must `attach` a `memoryset` to the model before using it. If you previously changed the embedding model for your memoryset you should ensure that this model uses the same one.

```
from orcalib.rac import RAC

model = RACModel(num_classes=10, memoryset=memoryset)
```

Optionally you can configure:

- `head`: Defaulted to a simple MMOE head
- `memory_width_override`: For controlling memory width
- `reranker`: To set a reranker protocol

### Evaluate

To evaluate a model: call `evaluate` on your model and pass in the dataset. There are optional args for `log` and `batch_size`.

```
model.evaluate(ds['validation'], log=True, batch_size=64)
```

The `evaluate` method returns `f1`, `roc_auc`, and `accuracy` for the dataset. `roc_auc` will not be calculated if the eval dataset doesn't include all labels.

Here is a sample output:

```
(
    f1=0.9959246634143168,
    roc_auc=0.9996387297127575,
    accuracy=0.9959235668789809
)
```

### Finetune

Finetune will finetune the model on a given dataset. There are optional flags to log progress or plot visualizations. You can also pass a training config to override the default learning rate, batch size, or number of epochs.

```
model.finetune(ds['train])
```

- `log=True` will output progress bars to keep you informed of the tuning status
- `plot=True` will show graphs of accuracy / loss as the tuning is progressing

### Predict

Predict evaluates one input. It returns a prediction result.

```
model.predict(ds['train'][0])
```

### Explain

Explain provides insights on model behavior.
It has a few return options:

- `pretty_print=True` will log two tables: memories accessed and label analysis.
- `plot=True` will display graphs: a pie chart of label distribution, mean memory lookup scores per label, memory lookup score distribution per label, and mean / variance of scores per label.

Calling `explain` with no args will return the dict that is used to generate the other outputs.

```
model.explain(inpt=ds['train'], plot=True)
```

`explain` can be called on an input (with the arg `inpt=...`) or on a prediction result (`prediction_result=...`). If an input is passed then `predict()` is called under the hood.

### Evaluate and explain

As compared to `explain`, this provides insights on a full `evaluate` run. This is performed in a less memory-efficient way than `evaluate` due to requiring more artifacts per run.

```
model.evaluate_and_explain(inpt=ds['train'], plot=True)
```

- `plot=True` Will display graphs: lookups per memory, high-error memories, Accuracy by memory label
- `log=True` Will output progress bars and contextual feedback regarding the steps

### Save

Once you are finished tuning your model you can save it to disk.

```
model.save("imagenette.pth")
```

### Load

To load a previously trained model you can use:

```
model.load("imagenette.pth")
```

### Attach

Attach a memoryset to a model. This will detach any previously attached memorysets.

```
model.attach(my_new_memoryset)
```

### Use

Temporarily attach a memoryset to a model. This can be useful when swapping memorysets to ensure that they aren't accidentally switched.

```
with model.use(my_memoryset):
    ...
```

After `.use` is finished running the model is left in a detached state.
