FROM postgres:latest
# ENV POSTGRES_USER postgres
# ENV POSTGRES_PASSWORD postgres
# ENV POSTGRES_DB postgres
ADD db.sql /docker-entrypoint-initdb.d/
# For future reference: All files in the entrypoint are executed in alphabetic order. 
# This will be useful for migrations in the future