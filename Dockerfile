FROM python:3.11.4-slim as installer

WORKDIR /app

COPY . /app/

RUN python -m venv /app/env

RUN . /app/env/bin/activate && \
python -m ensurepip --upgrade && \
python -m pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu  && \
python -m pip install --no-cache-dir -r /app/requirements.txt

FROM python:3.11.4-slim as final

WORKDIR /app

COPY --from=installer /app /app

ENV SENTENCE_TRANSFORMERS_HOME=./.cache
ENV HF_HOME=./.cache
ENV TOKENIZERS_PARALLELISM=false
ENV HF_TOKEN=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

RUN chown -R 2000:2000 /app
USER 2000:2000

EXPOSE 8000

CMD ["/app/env/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]