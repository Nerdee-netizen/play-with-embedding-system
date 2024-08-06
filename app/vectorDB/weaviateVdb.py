import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.client import WeaviateClient
from app.embedding.vectorizer import OpenAIVectorizer
from app.utils.config import env
from abc import ABC, abstractmethod


class VectrorDatabaseInsert(ABC):

    @abstractmethod
    def insert_data(self):
        pass


class WeaviateVdbInsert(VectrorDatabaseInsert):

    def __init__(self, client: WeaviateClient, table_name="ChunkEmbedding"):
        self.client = client
        self.table_name = table_name

    def connect_to_table(self):
        if not self.client.collections.exists(self.table_name):
            table_handle = self.client.collections.create(
                self.table_name,
                vectorizer_config=[
                    # Set a named vector
                    Configure.NamedVectors.none(name="text_vector")
                ],
                properties=[  # Define properties
                    Property(name="context_name", data_type=DataType.TEXT),
                    Property(name="context_id", data_type=DataType.TEXT),
                    Property(name="chunk_name", data_type=DataType.TEXT),
                    Property(name="chunk_id", data_type=DataType.TEXT),
                    Property(name="text", data_type=DataType.TEXT),
                    Property(name="open_url", data_type=DataType.TEXT),
                ],
            )
        else:
            table_handle = self.client.collections.get(self.table_name)

        return table_handle

    def insert_data(
        self,
        context_name: str,
        context_id: str,
        chunk_name: str,
        chunk_id: str,
        text: str,
        open_url: str,
        text_vector,  # np.ndarray
    ):

        table_handle = self.connect_to_table()
        uuid = table_handle.data.insert(
            properties={
                "context_name": context_name,
                "context_id": context_id,
                "chunk_name": chunk_name,
                "chunk_id": chunk_id,
                "text": text,
                "open_url": open_url,
            },
            vector={
                "text_vector": text_vector,
            },
        )
        self.client.close()
        return uuid


if __name__ == "__main__":
    context_name = "A delicious Riesling"
    context_id = "Germany"
    chunk_name = "This wine is a delicious Riesling which pairs well with seafood."
    chunk_id = "Riesling"
    text = "Germany"
    open_url = "https://en.wikipedia.org/wiki/Germany"

    vectorizer = OpenAIVectorizer(
        base_url=env.EMBEDDING_ENDPOINT,
        api_key="speak and see it done",
        model=env.EMBEDDING_MODEL_UID,
    )
    text_vector = vectorizer.vectorize(text)

    client = weaviate.connect_to_local("weaviate")
    Vdb = WeaviateVdbInsert(client, "ChunkEmbedding")

    uuid = Vdb.insert_data(
        context_name, context_id, chunk_name, chunk_id, text, open_url, text_vector
    )
    print(uuid)
    client.close()

    client = weaviate.connect_to_local("weaviate")
    ChunkEmbedding = client.collections.get("ChunkEmbedding")

    for item in ChunkEmbedding.iterator(
        include_vector=False  # If using named vectors, you can specify ones to include e.g. ['title', 'body'], or True to include all
    ):
        print(item.properties)
        print(item.vector)

    client.close()
