FROM jeeter30/flaskapi_api:base

COPY . /app

EXPOSE 8443

ENTRYPOINT [ "/app/bootstrap.sh" ]