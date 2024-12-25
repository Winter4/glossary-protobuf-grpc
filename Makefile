generate-proto:
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. glossary.proto

run-server:
	python3 server.py

run-test-client:
	python3 test_client.py

run-fetch-client:
	python3 fetch_client.py