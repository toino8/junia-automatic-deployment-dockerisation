.PHONY: hello
hello:
	  python hello.py

.PHONY: frontend-v1
frontend-v1:
	  docker build -f Dockerfile.basic -t frontend:0.0.1 .

.PHONY: frontend-v2
frontend-v2:
	  docker build -f Dockerfile.standard -t frontend:0.0.2 .

.PHONY: frontend-v3
frontend-v3:
	  docker build -f Dockerfile.standardv2 -t frontend:0.0.3 .

.PHONY: frontend-v4
frontend-v4:
	  docker build -f Dockerfile.advanced -t frontend:0.0.4 .

.PHONY: frontend-v5
frontend-v5:
	  docker build -f Dockerfile.advancedv2 -t frontend:0.0.5 .

.PHONY: frontend-v6
frontend-v6:
	  docker build -f Dockerfile.chiselled -t frontend:0.0.6 .

.PHONY: frontend-v7
frontend-v7:
	  docker build -f Dockerfile.chiselled.full -t frontend:0.0.7 .

.PHONY: tests
tests:
	  python -m pytest -v tests/
