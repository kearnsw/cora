# Latest rasa-sdk version: https://hub.docker.com/r/rasa/rasa-sdk/tags
# export VERS=0.1.1
# docker build -t wacovid/cora-actions:latest -t wacovid/cora-actions:${VERS} .
# docker login --username=wacovid --password=xyzzy
# docker push wacovid/cora-actions
# docker build -t test:actions .
# docker run -p 5055:5055 test:actions
FROM rasa/rasa-sdk:1.8.1

SHELL ["/bin/bash", "-c"]

USER root

RUN apt-get update -qq && \
    apt-get install -y \
      curl \
      iputils-ping \
      aws-requests-auth
#    apt-get clean \
#    rm -rf /var/lib/apt/lists/* \
#    rm -rf /tmp/* \
#    rm -rf /var/tmp/* \
#    mkdir /app

# To install packages from PyPI
RUN pip install --no-cache-dir \
  overrides \
  aws_requests_auth

USER 1001

WORKDIR /app

COPY . .

RUN ls -li

#RUN pip install -e . --no-cache-dir

#VOLUME ["/app/actions"]

EXPOSE 5055

ENTRYPOINT ["./entrypoint.sh"]

CMD ["start", "--actions", "actions.actions"]