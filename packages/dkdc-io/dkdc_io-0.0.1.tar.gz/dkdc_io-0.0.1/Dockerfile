FROM python:slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
ENV PATH=/root/.local/bin:$PATH
ADD . /app
WORKDIR /app
RUN uv pip install 'dkdc-io @ .' --system
CMD ["dkdc-io", "server"]
