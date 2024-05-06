FROM python:3.11-slim

WORKDIR /workspace

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Poetry for managing dependencies
RUN pip install --upgrade pip && \
    pip install poetry

# Copy only the dependencies specification to the container
COPY pyproject.toml poetry.lock* .

# Install project dependencies but avoid installing the project package itself
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-dev

# For Dev
RUN apt update && apt install -y vim git

# Copy the rest of the project files to the container
COPY . .

WORKDIR /workspace/app

# The default command to run the app using uvicorn
CMD ["bash"]