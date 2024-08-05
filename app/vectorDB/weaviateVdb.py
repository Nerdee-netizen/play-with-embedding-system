import weaviate
from weaviate.classes.config import Configure, Property, DataType
from app.embedding.vectorizer import OpenAIVectorizer
from app.utils.config import env
from abc import ABC, abstractmethod

class VectrorDatabase_Insert(ABC):

    @abstractmethod
    def insert_data(self):
        pass


class WeaviateVdb_Insert(VectrorDatabase_Insert):
    def __init__(
        self,
        http_host="weaviate",
        http_port=8080,
        http_secure=False,
        grpc_host="weaviate",
        grpc_port=50051,
        grpc_secure=False,
    ):
        self.http_host = http_host
        self.http_port = http_port
        self.http_secure = http_secure
        self.grpc_host = grpc_host
        self.grpc_port = grpc_port
        self.grpc_secure = grpc_secure


    def connect_to_db(self):
        client = weaviate.connect_to_custom(
            http_host=self.http_host,
            http_port=self.http_port,
            http_secure=self.http_secure,
            grpc_host=self.grpc_host,
            grpc_port=self.grpc_port,
            grpc_secure=self.grpc_secure,
        )

        return client
    
    def connect_to_table(self, client: weaviate.client.Client, table_name="ChunkEmbedding"):
        if not client.collections.exists(table_name):
            table_handle = client.collections.create(
                table_name,
                vectorizer_config=[
                    # Set a named vector
                    Configure.NamedVectors.none(  # Use the "text2vec-cohere" vectorizer
                        name="text_vector"  # Set the source property(ies)
                    )
                ],
                properties=[  # Define properties
                    Property(name="context_name", data_type=DataType.TEXT),
                    Property(name="chunk_name", data_type=DataType.TEXT),
                    Property(name="text", data_type=DataType.TEXT),
                ],
            )
        else:
            table_handle = client.collections.get(table_name)

        return table_handle
    
    def insert_data(self, context_name, chunk_name, text, text_vector):

        client = self.connect_to_db()

        table_handle=self.connect_to_table(client)

        uuid = table_handle.data.insert(
            properties={
                "context_name": context_name,
                "chunk_name": chunk_name,
                "text": text,
            },
            vector={
                "text_vector": text_vector,
            },
        )

        client.close()
        return uuid


if __name__ == "__main__":
    context_name = "A delicious Riesling"
    chunk_name = "This wine is a delicious Riesling which pairs well with seafood."
    text = "Germany"

    vectorizer = OpenAIVectorizer(base_url=env.EMBEDDING_ENDPOINT,
        api_key="speak and see it done",
         model=env.EMBEDDING_MODEL_UID,
     )
    text_vector = vectorizer.vectorize(text)

    Vdb=WeaviateVdb_Insert()
    
    uuid=Vdb.insert_data(context_name, chunk_name, text, text_vector)
    print(uuid)
    
    client=weaviate.connect_to_local("weaviate")
    ChunkEmbedding = client.collections.get("ChunkEmbedding")

    for item in ChunkEmbedding.iterator(
        include_vector=False  # If using named vectors, you can specify ones to include e.g. ['title', 'body'], or True to include all
    ):
        print(item.properties)
        print(item.vector)

    client.close()