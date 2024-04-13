FROM python:3.9-slim

WORKDIR /app

COPY . .

# Run the tests
RUN pip install pytest
RUN pytest tests.py

# Start the database
CMD ["python", "./database.py"]
