FROM python:3.10-slim

# Set up workdir
WORKDIR /app

# Install basic tools
RUN pip install --no-cache-dir streamlit requests

# Copy files to the container
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
