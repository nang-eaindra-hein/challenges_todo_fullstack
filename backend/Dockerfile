
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app #start from run mk file name

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

ENV LITESTAR_APP="app:app" 
EXPOSE 8000 

CMD ["uv", "run", "litestar", "run", "--host", "0.0.0.0","--reload", "--port", "8000"] 
