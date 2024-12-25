from concurrent import futures
import grpc
import glossary_pb2
import glossary_pb2_grpc

# In-memory glossary storage
glossary = {}

class GlossaryServiceServicer(glossary_pb2_grpc.GlossaryServiceServicer):
    def GetAllTerms(self, request, context):
        return glossary_pb2.TermList(terms=[
            glossary_pb2.Term(name=name, description=desc)
            for name, desc in glossary.items()
        ])

    def AddTerm(self, request, context):
        if request.name in glossary:
            return glossary_pb2.OperationStatus(success=False, message="Term already exists")
        glossary[request.name] = request.description
        return glossary_pb2.OperationStatus(success=True, message="Term added successfully")

    def UpdateTerm(self, request, context):
        if request.name not in glossary:
            return glossary_pb2.OperationStatus(success=False, message="Term not found")
        glossary[request.name] = request.description
        return glossary_pb2.OperationStatus(success=True, message="Term updated successfully")

    def DeleteTerm(self, request, context):
        if request.name not in glossary:
            return glossary_pb2.OperationStatus(success=False, message="Term not found")
        del glossary[request.name]
        return glossary_pb2.OperationStatus(success=True, message="Term deleted successfully")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(GlossaryServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server is running on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
