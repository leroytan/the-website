cd backend
poetry install
poetry run python -m uvicorn api.index:app --reload