# emdantic

Embed pydantic models

Embantic is an OVM (Object Vector Mapper) which embeds pydantic models to vectors allowing for semantic search and retrieval of arbitrary mutlimodal objects.

## Installation

```sh
pip install embantic
```

## Usage

Create a data model you would like to embed

```python
from emdantic import EmbModel

class Foo(EmbModel):
    a: int
    b: str
    c: float
    d: bool
    e: list[int]
    f: dict[str, int]
    g: Image.Image
    h: Optional[EmbModel]
```

Embed the data model

```python
foo = Foo(
    a=1, 
    b="hello", 
    c=3.14, 
    d=True, 
    e=[1, 2, 3], 
    f={"a": 1, "b": 2},
    g=Image.open("path/to/image.png")
)

vectors = foo.embed()
```

Or embed the data model and store the embeddings in a vector database

```python
foo.store()
```

Search for objects by text

```python
results: List[Foo] = Foo.search("hello")
```

Search for objects by image

```python
results: List[Foo] = Foo.search(Image.open("path/to/image.png"))
```

Specify the embedding models to use

```python
class Foo(EmbModel):
    __text_model__ = "text-embedding-ada-002"
    __image_model__ = "SigLIP-400M"

    ...
```

## Backends

### Vector Databases

Vector database backends are configured using `EMDANTIC_VECTOR_BACKEND` environment variable. Supported backeends are currently: `faiss`


### Embedding Models

Embedding models are configured using the `__text_model__` and `__image_model__` parameters on the `EmbModel` class. Supported models are currently: `text-embedding-ada-002` and `SigLIP-400M`.

Alternatively, you can set the `EMDANTIC_TEXT_EMBEDDING_MODEL` and `EMDANTIC_IMAGE_EMBEDDING_MODEL` environment variable as the model defaults.

### Database

Embdantic also uses a database to store the raw objects in JSON format. The database is configured using the `EMDANTIC_DATABASE_BACKEND` environment variable. Supported databases are currently: `sqlite`.