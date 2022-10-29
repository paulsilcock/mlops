FROM python:3.10-slim-bullseye as rel
WORKDIR /app
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache pip install -r requirements.txt
RUN rm -Rf /root/.cache
COPY mlops/service ./mlops/service
ENTRYPOINT ["python", "-m"]
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "mlops.service.app:app"]

FROM rel as test
COPY requirements-test.txt .
RUN --mount=type=cache,target=/root/.cache pip install -r requirements-test.txt
RUN rm -Rf /root/.cache
COPY mlops/stages ./mlops/stages
COPY tests ./tests
RUN pytest tests/**/*

FROM rel as dev
COPY requirements-debug.txt .
RUN --mount=type=cache,target=/root/.cache pip install -r requirements-debug.txt
RUN rm -Rf /root/.cache
ENTRYPOINT ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678"]
CMD ["-m", "uvicorn", "--host", "0.0.0.0", "--port", "8080", "mlops.service.app:app"]

FROM rel as dvc
COPY requirements-dvc.txt .
RUN --mount=type=cache,target=/root/.cache pip install -r requirements-dvc.txt
RUN rm -Rf /root/.cache
