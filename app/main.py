from app.vectorDB.weaviateVdb import insert_data
from app.embedding.vectorizer import OpenAIVectorizer
from app.utils.config import env
import numpy as np
from concurrent import futures
import grpc
import embeddingservice_pb2
import embeddingservice_pb2_grpc

class EmbeddingServiceServicer(embeddingservice_pb2_grpc.EmbeddingServiceServicer):
    def TextEmbedding(self, request, context):
        vectorizer = OpenAIVectorizer(
            base_url=env.EMBEDDING_ENDPOINT,
            api_key="speak and see it done",
            model=env.EMBEDDING_MODEL_UID,
        )
        embedding = vectorizer.vectorize(request.text)
        # Flatten the embedding
        flat_embedding = embedding.flatten().tolist()
        
        # Create metadata
        metadata = embeddingservice_pb2.Metadata(dim1=embedding.shape[0], dim2=embedding.shape[1])
        
        # Create response
        response = embeddingservice_pb2.TextEmbeddingResponse(vector=flat_embedding, metadata=metadata)
        
        return response
    
    def Chunk2Vdb(self, request, context):

        if insert_data(context_name=request.context_name, chunk_name=request.chunk_name, text=request.text):
            response=embeddingservice_pb2.Chunk2VdbResponse(reponse=True)
        else:
            response=embeddingservice_pb2.Chunk2VdbResponse(reponse=False)
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    embeddingservice_pb2_grpc.add_EmbeddingServiceServicer_to_server(EmbeddingServiceServicer(), server)

    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()