import os
import grpc
import glossary_pb2
import glossary_pb2_grpc

def run_fetcher():
    server_url = os.getenv("SERVER_URL", "localhost:50051")
    print(f"Connecting to server at: {server_url}")

    with grpc.insecure_channel(server_url) as channel:
        stub = glossary_pb2_grpc.GlossaryServiceStub(channel)

        # Get all terms
        term_list = stub.GetAllTerms(glossary_pb2.Empty())
        for term in term_list.terms:
            print(f"{term.name}: {term.description}")

if __name__ == '__main__':
    run_fetcher()
