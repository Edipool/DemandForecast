
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
