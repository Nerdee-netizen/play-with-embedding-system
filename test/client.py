import grpc

import embeddingservice_pb2
import embeddingservice_pb2_grpc


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = embeddingservice_pb2_grpc.EmbeddingServiceStub(channel)

        # Call the Sum method
        textembedding_request = embeddingservice_pb2.TextEmbeddingRequest(
            text="Hello, World!"
        )
        textembedding_response = stub.TextEmbedding(textembedding_request)
        print(f"{textembedding_response.metadata}")

        # Call the Subtract method
        Chunk2Vdb_request = embeddingservice_pb2.Chunk2VdbRequest(
            context_name="context_name",
            context_id="context_id",
            chunk_name="chunk_name",
            chunk_id="chunk_id",
            text="",
            open_url="",
        )
        Chunk2Vdb_response = stub.Chunk2Vdb(Chunk2Vdb_request)
        print(f"{Chunk2Vdb_response.reponse}")


if __name__ == "__main__":
    run()
