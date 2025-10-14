# Gunakan base image Python
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy semua isi project
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Tentukan environment variable default
ENV RUN_MODE=flask

# Expose port Flask (jika mode Flask)
EXPOSE 5000

# Jalankan berdasarkan mode
CMD if [ "$RUN_MODE" = "flask" ]; then \
        python visualizer_flask/app.py; \
    else \
        python main.py --a house_multifeature.csv --skip-header; \
    fi
