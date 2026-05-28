# Use the official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy the dashboard requirements and install them
COPY dashboard/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the container
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Set the command to run the Streamlit dashboard
CMD ["streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
