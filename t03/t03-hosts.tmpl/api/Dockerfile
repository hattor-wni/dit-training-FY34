FROM python:3.8.0-buster

RUN useradd -m foo -s /bin/bash

RUN pip install Flask==1.1.1

ARG project_dir=/app/db/
WORKDIR $project_dir
COPY app.py init.py $project_dir
RUN python init.py

CMD ["python", "app.py"]
