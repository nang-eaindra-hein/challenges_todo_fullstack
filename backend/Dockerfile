
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app #start from run mk file name

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .


ENV PATH="/app/.venv/bin:$PATH"
CMD ["litestar", "--app", "app.main:app", "run", "--reload", "--host", "0.0.0.0", "--port", "8000"]