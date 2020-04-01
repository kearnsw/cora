## Access

* The Rasa X UI is at http://rasa.wa-covid-org which is mapped from http://f8a207966bd411ea949d0687da031d8-145421237.us-west-2.elb.amazonaws.com:8000

## Deploy

Deployment notes can be found in [DEPLOY.md](DEPLOY.md)

## Action Server Docker Build

Build image locally:

```
export VERS=0.1.5
docker build -t wacovid/cora-actions:latest -t wacovid/cora-actions:${VERS} .
```

Test locally:

```
docker run -p 5005:5005 wacovid/cora-actions
```

Push to Docker hub:

```
docker login --username=wacovid --password=xyzzy
docker push wacovid/cora-actions
```

View docker hub tags to confirm it has been updated: https://hub.docker.com/r/wacovid/cora-actions/tags

## Restart Kubernetes Action Pod

To update the Kubernetes action agent pod run the following command. Note that you will need the local AWS cli connected to the account and have `kubectl` installed:

```
kubectl -n wa-covid-bot delete pod -l app.kubernetes.io/component=app
```

## Runnnig Locally

From the command line in separate windows, you can run the following:

```
rasa run actions --debug
rasa shell --conversation-id 206-555-1212
```

## ToDo

- [ ] ZipWhip channel setup
- [ ] Spreadsheet to Rasa intents & stories
- [ ] ssl certs for https
- [x] DynamoDB vs Tracker store - will use Tracker store
- [ ] Other Channels/Connector
  - [ ] Website, Kommunicate.io front end Tyler
  - [ ] Steve, olosupport
- Human handover

## Questions

- History of slot values
- How to handle multiple people using the same phone number

## turn.io

- Experts
  - Pippa scrapped FAQ from WHO
  - 10M people since Friday
  - Expected volume is 330 messages/sec
    - 500 msg/sec is WhatsApp current Bus. API limit, setting up multiple numbers to handle this
    - They dynamically change the phone number when it is shared between people
  - Built with their own turn app
- Single bot
  - yes
- Deployment setup, Kubernetes?
  - Yes but Pippa & Neelke aren't doing the deployment
