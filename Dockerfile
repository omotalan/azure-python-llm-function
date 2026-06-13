# NOTE: This image is for local development and CI validation only.
# For production Azure Functions deployment, use the official base image:
# mcr.microsoft.com/azure-functions/python:4-python3.11

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "pytest", "tests/", "-v"]