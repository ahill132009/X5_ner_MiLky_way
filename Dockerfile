FROM python:3.12-slim

WORKDIR /code

# Copy requirements first for better layer caching
COPY ./app/requirements.txt /code/requirements.txt
COPY ./app/download_model.py /code/download_model.py
COPY ./app/.env /code/.env


# Install PyTorch CPU version from official index
RUN pip install torch --no-cache-dir --index-url https://download.pytorch.org/whl/cpu

# Install other dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app/env.yaml /code/env.yaml
# Create directory to store model & tokenizer
RUN mkdir -p /code/app/nlp_models
COPY ./app/download_model.py /code/download_model.py

# Create model dir and download
RUN mkdir -p /code/nlp_models
RUN python /code/download_model.py

# Copy the rest of the app (after model is downloaded)
COPY ./app /code/app

# Set environment variables
ENV BASE_DIR=/code/
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code/app


# Expose port
EXPOSE 8000

# Run FastAPI app
# CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "localhost:8000", "--workers", "4", "--timeout", "60"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]