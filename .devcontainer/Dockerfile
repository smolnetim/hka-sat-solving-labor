FROM mcr.microsoft.com/devcontainers/python:0-3.11

COPY . .

RUN pip install -r requirements.txt
RUN python -m ipykernel install --user
