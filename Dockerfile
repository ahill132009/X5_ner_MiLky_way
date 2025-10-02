FROM pytorch/pytorch:2.6.0-cuda12.4-cudnn9-runtime
WORKDIR /code


COPY ./app/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --no-deps --upgrade -r /code/requirements.txt


COPY ./app /code/app

# Set environment variables
ENV BASE_DIR=/code/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]