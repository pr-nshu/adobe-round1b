# Use a lightweight Python image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/data/input/docs /app/data/output /app/models/sentence_transformers

# Copy the pre-downloaded Sentence Transformer model
# Download the model first using:
# python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2').save_pretrained('./models/sentence_transformers/all-MiniLM-L6-v2')"
COPY models/sentence_transformers/all-MiniLM-L6-v2/ /app/models/sentence_transformers/all-MiniLM-L6-v2/

# Copy the application code
COPY app/ /app/app/

# Copy the data directories (input configuration and PDFs)
COPY data/input/ /app/data/input/

# Ensure output directory exists and is writable
RUN chmod -R 777 /app/data/output

# Command to run the application
CMD ["python", "/app/app/main.py"]
