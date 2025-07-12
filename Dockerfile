# Stage 1: Builder Stage
# This stage installs Python dependencies and prepares the environment.
FROM python:3.12-slim AS builder

RUN mkdir /medata
WORKDIR /medata

# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 

RUN pip install --upgrade pip
COPY requirements.txt  /medata/
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production Stage
# This stage sets up the production environment with the installed dependencies.
FROM python:3.12-slim

RUN useradd -m -r django && \
    mkdir /medata && \
    chown -R django /medata

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

WORKDIR /medata

COPY --chown=django:django manage.py /medata/
COPY --chown=django:django medata /medata/medata
COPY --chown=django:django apps /medata/apps
COPY --chown=django:django frontend/dist /medata/frontend/dist
COPY --chown=django:django static /medata/static

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

USER django

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "medata.wsgi:application"]