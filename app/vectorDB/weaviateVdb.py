import weaviate
from weaviate.classes.config import Configure, Property, DataType
from app.embedding.vectorizer import OpenAIVectorizer
from app.utils.config import env

def insert_data(context_name, chunk_name, text):
    vectorizer = OpenAIVectorizer(
        base_url=env.EMBEDDING_ENDPOINT,
        api_key="speak and see it done",
        model=env.EMBEDDING_MODEL_UID,
    )

    text_vector = vectorizer.vectorize(text)

    client = weaviate.connect_to_custom(
        http_host="weaviate",
        http_port=8080,
        http_secure=False,
        grpc_host="weaviate",
        grpc_port=50051,
        grpc_secure=False,
    )

    if not client.collections.exists("ChunkEmbedding"):
        ChunkEmbedding = client.collections.create(
            "ChunkEmbedding",
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
        ChunkEmbedding = client.collections.get("ChunkEmbedding")

    uuid = ChunkEmbedding.data.insert(
        properties={
            "context_name": context_name,
            "chunk_name": chunk_name,
            "text": text,
        },
        # Specify the named vectors, following the collection definition
        vector={
            "text_vector": text_vector,
        },
    )

    client.close()
    return uuid


if __name__ == "__main__":
    # context_name = "A delicious Riesling"
    # chunk_name = "This wine is a delicious Riesling which pairs well with seafood."
    # text = "Germany"

    # uuid = insert_data(context_name, chunk_name, text)
    # print(uuid)
    
    client=weaviate.connect_to_local("weaviate")
    ChunkEmbedding = client.collections.get("ChunkEmbedding")

    for item in ChunkEmbedding.iterator(
        include_vector=True  # If using named vectors, you can specify ones to include e.g. ['title', 'body'], or True to include all
    ):
        print(item.properties)
        print(item.vector)

    client.close()