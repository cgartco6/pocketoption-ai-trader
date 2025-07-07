FROM python:3.10-slim

# Install system dependencies for PyYAML and other libraries
RUN apt-get update && apt-get install -y libyaml-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]
