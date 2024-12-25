install:
	pip install --no-cache-dir -r requirements.txt

generate-proto:
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. glossary.proto

run-server:
	python3 server.py

run-test-client:
	python3 test_client.py

run-fetch-client:
	python3 fetch_client.py

build-image:
	docker image build -t glossary-protobuf-grpc  .

compose-up:
	docker compose up --attach test-client

compose-down:
	docker compose down