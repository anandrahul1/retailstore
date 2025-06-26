FROM python:3.11-slim

WORKDIR /app

# Copy shared dependencies
COPY ../../shared/requirements.txt /app/shared/requirements.txt
RUN pip install -r /app/shared/requirements.txt

# Copy shared modules
COPY ../../shared/ /app/shared/

# Copy service files
COPY . /app/

# Install service-specific dependencies if any
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

EXPOSE 8001

CMD ["python", "main.py"]