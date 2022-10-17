FROM apache/superset:latest
USER root
USER superset
RUN superset superset fab create-admin \
               --username admin \
               --firstname Superset \
               --lastname Admin \
               --email admin@superset.com \
               --password admin

RUN superset superset db upgrade
RUN superset superset init