from app.vectorDB.weaviateVdb import WeaviateVdbInsert
from app.embedding.vectorizer import OpenAIVectorizer
from app.utils.config import env
from concurrent import futures
import grpc
import embeddingservice_pb2
import embeddingservice_pb2_grpc
import weaviate
from weaviate.client import WeaviateClient


def get_weaviate_client_custom(env) -> WeaviateClient:
    headers = None
    if env.WEAVIATE_TOKEN:
        headers = {"Authorization": f"Bearer {env.WEAVIATE_TOKEN}"}

    client = weaviate.connect_to_custom(
        http_host=env.WEAVIATE_HTTP_HOST,
        http_port=env.WEAVIATE_HTTP_PORT,
        http_secure=env.WEAVIATE_HTTP_SECURE,
        grpc_host=env.WEAVIATE_GRPC_HOST,
        grpc_port=env.WEAVIATE_GRPC_PORT,
        grpc_secure=env.WEAVIATE_GRPC_SECURE,
        headers=headers,
    )
    assert client.is_live() == True
    assert client.is_ready() == True
    return client


class EmbeddingServiceServicer(embeddingservice_pb2_grpc.EmbeddingServiceServicer):
    def TextEmbedding(self, request, context):
        vectorizer = OpenAIVectorizer(
            base_url=env.EMBEDDING_ENDPOINT,
            api_key="speak and see it done",
            model=env.EMBEDDING_MODEL_UID,
        )
        embedding = vectorizer.vectorize(request.text)

        flat_embedding = embedding.flatten().tolist()

        metadata = embeddingservice_pb2.Metadata(
            dim1=embedding.shape[0], dim2=embedding.shape[1]
        )

        response = embeddingservice_pb2.TextEmbeddingResponse(
            vector=flat_embedding, metadata=metadata
        )

        return response

    def Chunk2Vdb(self, request, context):
        vectorizer = OpenAIVectorizer(
            base_url=env.EMBEDDING_ENDPOINT,
            api_key="speak and see it done",
            model=env.EMBEDDING_MODEL_UID,
        )
        text_vector = vectorizer.vectorize(request.text)

        client = get_weaviate_client_custom(env)
        Vdb = WeaviateVdbInsert(client, request.table_name)

        uuid = Vdb.insert_data(
            context_name=request.context_name,
            context_id=request.context_id,
            chunk_name=request.chunk_name,
            chunk_id=request.chunk_id,
            text=request.text,
            open_url=request.open_url,
            text_vector=text_vector,
        )

        client.close()

        if uuid:
            response = embeddingservice_pb2.Chunk2VdbResponse(reponse=True)
        else:
            response = embeddingservice_pb2.Chunk2VdbResponse(reponse=False)
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    embeddingservice_pb2_grpc.add_EmbeddingServiceServicer_to_server(
        EmbeddingServiceServicer(), server
    )

    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
