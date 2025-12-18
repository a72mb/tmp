FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get upgrade
RUN apt-get update
RUN apt-get install -y wget build-essential
RUN apt-get clean
RUN apt-get update
RUN apt-get -y install default-libmysqlclient-dev pkg-config python3-dotenv

# Change the working directory to the `app` directory
WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_TOOL_BIN_DIR=/usr/local/bin
COPY pyproject.toml /app
COPY uv.lock /app
COPY .env /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy the project into the image
COPY . /app

ENV FLASK_APP=knights

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"

# Expose the port
EXPOSE 8080

# CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
CMD ["gunicorn", "-b", "0.0.0.0:8080", "knights:app"]