import grpc
import glossary_pb2
import glossary_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = glossary_pb2_grpc.GlossaryServiceStub(channel)

        # Add a term
        response = stub.AddTerm(glossary_pb2.Term(name="API", description="Application Programming Interface"))
        print(response.message)

        # Get all terms
        term_list = stub.GetAllTerms(glossary_pb2.Empty())
        for term in term_list.terms:
            print(f"{term.name}: {term.description}")

        # Update a term
        response = stub.UpdateTerm(glossary_pb2.Term(name="API", description="Updated description")) 
        print(response.message)

        # Delete a term
        response = stub.DeleteTerm(glossary_pb2.TermRequest(name="API"))
        print(response.message)

if __name__ == '__main__':
    run()
