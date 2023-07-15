FROM python:3.11.0rc2-slim

WORKDIR /app
# Create Environment variable for the image
# PYTHONBUFFERED: Will give the output directly to the terminal (use for logging)
# PYTHONDONTWRITEBYTECODE: Prevent python from creating .pyc which we do not use and bring bugs
ENV PYTHONBUFFERD=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY pyproject.toml poetry.lock ./

RUN python -m pip install --no-cache-dir --upgrade pip && \
          pip install poetry && \
          poetry config virtualenvs.create false && \
          poetry install

COPY . .
COPY ./entrypoint.sh ./entrypoint.sh

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["bash", "entrypoint.sh"]
