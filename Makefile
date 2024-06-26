.PHONY: docs docs_pdf

app:
	@echo "Running streamlit_app..."
	streamlit run web_app/streamlit_app.py

fastapi:
	@echo "Running fastapi_app..."
	uvicorn app:app --reload --port 8001 & sleep 2 && open http://0.0.0.0:8001/docs

run_pipeline:
	@echo "Running pipeline..."
	python3 train_pipeline.py

test:
	@echo "Running tests..."
	pytest

build_docker:
	@echo "Building docker images..."
	docker build -t edipool/demandforecast_app:latest -f ./Dockerfile .
	docker build -t edipool/demandforecast_streamlit:latest -f ./web_app/Dockerfile ./web_app

push_docker:
	@echo "Pushing docker images to registry..."
	docker push edipool/demandforecast_app:latest
	docker push edipool/demandforecast_streamlit:latest

start_services:
	@echo "Starting services..."
	docker run --name app -v ./src/:/usr/src/app/ -p 8001:8000 -d edipool/demandforecast_app:latest
	docker run --name prometheus -v ./prometheus_data/prometheus.yml:/etc/prometheus/prometheus.yml -p 9090:9090 -d prom/prometheus
	docker run --name grafana -v ./grafana_data:/var/lib/grafana -p 3000:3000 -d grafana/grafana
	docker run --name streamlit_app -p 8501:8501 --depends-on app,grafana,prometheus -d edipool/demandforecast_streamlit:latest

stop_services:
	@echo "Stopping services..."
	docker stop app prometheus grafana streamlit_app
	docker rm app prometheus grafana streamlit_app

save_tree:
	@ echo "Saving project structure..."
	tree -L 4 -I 'venv|__pycache__|mlruns|dist|grafana_data|*egg-info|build|source|make.bat' > project_structure.txt

docs:
	@echo "Updating documentation..."
	@cd docs && make html

docs_pdf:
	@echo "Building PDF documentation..."
	@cd docs && sphinx-build -b latex source build/latex && cd build/latex && pdflatex demand_forecast.tex && pdflatex demand_forecast.tex

# Run linting
lint:
	find . -name '*.py' | xargs pylint --disable=E0401,W0611,R0902,R0903 > logs/pylint_report.txt || true

# Run sort imports and black
format:
	isort . && black .
