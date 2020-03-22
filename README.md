
## Action Server Docker Build

Build image locally:

```
export VERS=0.1.0
docker build -t wacovid/cora-actions:latest -t wacovid/cora-actions:${VERS} .
```

Test locally:

```
docker build -t wacovid/cora-actions .
docker run -p 5055:5055 wacovid/cora-actions
```

Push to Docker hub:

```
docker login --username=wacovid --password=xyzzy
docker push wacovid/cora-actions
```

## Runnnig Locally

From the command line in separate windows, you can run the following:

```
rasa run actions --debug
rasa shell --conversation-id 206-555-1212
```

## ToDo

