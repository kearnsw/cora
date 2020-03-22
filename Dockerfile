# Latest rasa-sdk version: https://hub.docker.com/r/rasa/rasa-sdk/tags
# docker build -t test:actions .
FROM rasa/rasa-sdk:1.8.1

SHELL ["/bin/bash", "-c"]

USER root

RUN apt-get update -qq && \
#    apt-get install -y <NAME_OF_REQUIRED_PACKAGE> && \
    apt-get clean \
#    rm -rf /var/lib/apt/lists/* \
#    rm -rf /tmp/* \
#    rm -rf /var/tmp/* \
    mkdir /app

# To install packages from PyPI
#RUN pip install --no-cache-dir <A_REQUIRED_PACKAGE_ON_PYPI>

USER 1001

WORKDIR /app

COPY . .

RUN ls -li

#RUN pip install -e . --no-cache-dir

#VOLUME ["/app/actions"]

EXPOSE 5055

ENTRYPOINT ["./entrypoint.sh"]

CMD ["start", "--actions", "actions.actions"]