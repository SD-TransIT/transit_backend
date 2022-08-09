FROM python:3.10.5-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /backend
COPY requirements.txt /backend/
RUN pip install -r requirements.txt
RUN pip install tox
COPY . /backend/
ENTRYPOINT ["/backend/docker-entrypoint.sh"]
RUN ["chmod", "+x", "/backend/docker-entrypoint.sh"]
