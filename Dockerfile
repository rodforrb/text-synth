ARG PYTHON_IMG=3-alpine

FROM python:${PYTHON_IMG}

EXPOSE 5000

ENV USR nonroot
ENV HOME /home/${USR}
ENV PROJECT_DIR ${HOME}/code
ENV PYTHONUNBUFFERED 1

ENV HOST=127.0.0.1
ENV HOST_PORT=5000

# module holding our project instance
ENV FLASK_APP=wsgi.py
ENV FLASK_DEBUG=1
ENV FLASK_ENV=development
# which configuration class to use; see config.py
ENV FLASK_CONFIG_DEFAULT=Dev

RUN addgroup -g 1000 ${USR}\
  && adduser -S -h ${HOME} -u 1000 -G ${USR} ${USR}

COPY --chown=nonroot:nonroot . ${PROJECT_DIR}

RUN apk add --no-cache --update fish
RUN apk add gcc libc-dev zlib-dev libffi-dev g++ make
RUN pip install --no-cache-dir -r ${PROJECT_DIR}/requirements.txt

# we make sure to run the project as a regular user
USER ${USR}
WORKDIR ${PROJECT_DIR}
CMD ["python", "wsgi.py"]
