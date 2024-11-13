# Stage 1: Builder
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --user -r requirements.txt

# Stage 2: Final image
FROM python:3.12-alpine

# Set environment variables to avoid issues with permissions
ENV PATH=/root/.local/bin:$PATH

# Set working directory
WORKDIR /app

# Copy only the necessary libraries from the builder stage
COPY --from=builder /root/.local /root/.local

# Copy the application code
COPY . .

# Expose the app port
EXPOSE 5000

# Start the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
