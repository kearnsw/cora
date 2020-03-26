## Rasa EKS setup

Rasa with AWS EKS and Helm. The main Rasa docs on this are [here](https://rasa.com/docs/rasa-x/installation-and-setup/openshift-kubernetes/#kubernetes-openshift). Rasa Helm chart git repo is [here](https://github.com/rasahq/rasa-x-helm).
- [Amazon page](https://docs.aws.amazon.com/eks/latest/userguide/helm.html) on using Helm with EKS

### AWS Steps

- [Install aws-iam-authenticator](https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html) locally first
- Make sure you are in the right AWS region before creating the EKS Cluster 
- Need an EKS role first. [This page](https://docs.aws.amazon.com/eks/latest/userguide/service_IAM_role.html) has instructions on how to check if the role exists. - Create AWS EKS Cluster

- [Create a kubeconfig for Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html)
- `aws eks --region us-west-2 update-kubeconfig --name wa-covid-bot`
- `export KUBECONFIG=~/.kube/wa-covid`

## ToDo

- Deploy issue:
  - `Error from server (BadRequest): container "rasa-x" in pod "rasa-x-1584834511-rasa-x-68f7669879-vrhcn" is waiting to start: trying and failing to pull image`
  - `Error from server (BadRequest): container "rasa-x" in pod "prod-rasa-x-5bbdddd665-9nb68" is waiting to start: image can't be pulled`
- Setup channel `credentials.yml` which go under `values.yml` for Helm. See [docs](https://rasa.com/docs/rasa-x/installation-and-setup/openshift-kubernetes/#configure-rasa-open-source-channels)
- Update app docker image in `values.yml` (I presume we will need this for additional libraries - dynamoDB)
- Figure out how to assign AWS instance types to Rasa node types to reduce resource usage
  - `values.yml` [nodeSelector](https://github.com/RasaHQ/rasa-x-helm/blob/23ec145c99d68395b9dcdfa760c753943ccd20b4/charts/rasa-x/values.yaml#L201)
  - Recommended [container specs](https://rasa.com/docs/rasa-x/installation-and-setup/openshift-kubernetes/#deploy-to-a-cluster-logging)
  - AWS [instance specs](https://aws.amazon.com/ec2/instance-types/)

## Rasa k8s Notes

- [Rasa Enterprise Install](https://rasa.com/docs/rasa-x/installation-and-setup/openshift-kubernetes/#rasa-enterprise-installation)
- [Creating Rasa X users](https://rasa.com/docs/rasa-x/installation-and-setup/openshift-kubernetes/#create-update-rasa-x-users)
- [HTTPS Setup](https://rasa.com/docs/rasa-x/installation-and-setup/openshift-kubernetes/#using-https)
- [Access Logs](https://rasa.com/docs/rasa-x/installation-and-setup/openshift-kubernetes/#accessing-logs)

## Rasa EKS setup

Rasa with AWS EKS and Helm. The main Rasa docs on this are [here](https://rasa.com/docs/rasa-x/installation-and-setup/openshift-kubernetes/#kubernetes-openshift). Rasa Helm chart git repo is [here](https://github.com/rasahq/rasa-x-helm).

- Create AWS EKS Cluster
  - Need an EKS role first. [This page](https://docs.aws.amazon.com/eks/latest/userguide/service_IAM_role.html) has instructions on how to check if the role exists. [This page](https://docs.aws.amazon.com/eks/latest/userguide/service_IAM_role.html#create-service-role) describes how to create the role.
  - Make sure you are in the right AWS region before creating the EKS Cluster
- [Setup Node Groups](https://docs.aws.amazon.com/eks/latest/userguide/launch-workers.html)
  - Initial t3.small, 8 nodes initially, 12 max?
  - [Create Node IAM Role](https://docs.aws.amazon.com/eks/latest/userguide/worker_node_IAM_role.html)
  - [Create Workder Node Role](https://docs.aws.amazon.com/eks/latest/userguide/worker_node_IAM_role.html#create-worker-node-role)
- [Amazon page](https://docs.aws.amazon.com/eks/latest/userguide/helm.html) on using Helm with EKS
  - [Install aws-iam-authenticator](https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html) locally first
  - [Create a kubeconfig for Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html)
    - `aws eks --region us-west-2 update-kubeconfig --name wa-covid-bot`
  - `export KUBECONFIG=~/.kube/wa-covid`
  - `kubectl get svc`

## EKS Deployment Notes

From the directory containing the `values.yml` do the following:

```
export KUBECONFIG=~/.kube/wa-covid
kubectl -n <your namespace> \
kubectl get svc
kubectl create secret docker-registry gcr-pull-secret --docker-server=gcr.io \
    --docker-username=_json_key --docker-password="$(cat gcr-auth.json)"
kubectl create ns wa-covid-bot
helm repo add rasa-x https://rasahq.github.io/rasa-x-helm
helm install prod -n wa-covid-bot --values values.yml rasa-x/rasa-x
kubectl -n wa-covid-bot get pods
kubectl -n wa-covid-bot logs rasa
kubectl -n wa-covid-bot describe pod rasa-x
kubectl -n wa-covid-bot get service -l app.kubernetes.io/component=nginx
    -o jsonpath="{.items..status..loadBalancer..ingress[0].ip}"
```

### Helm Secrets

- [k8s and Helm Environment Vars](https://medium.com/gammastack/mounting-environment-variables-safely-with-kubernetes-secrets-and-helm-chart-764420dc787b)
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)
- [Helm Best Practices](https://jfrog.com/blog/helm-charts-best-practices/)

```
kubectl create secret docker-registry regsecret --docker-server=$DOCKER_REGISTRY_RUL --docker-username=$USERNAME --docker-password=$PASSWORD --docker-email=$EMAIL
```

```
kubectl create secret generic test-secret --from-literal=username=devuser --from-literal=password='S!B\*d$zDsb'
kubectl delete secret test-secret
kubectl get secrets
kubectl describe secrets/greg-pull-secret
kubectl apply -f ./secret.yaml
```

### Helm Cheatsheet

Preface all of these commands with `helm`. In these examples the release name is `prod`.

| CMD                                                            | Info            |
| -------------------------------------------------------------- | --------------- |
| install prod -n wa-covid-bot --values values.yml rasa-x/rasa-x |                 |
| list -n wa-covid-bot                                           | list releases   |
| uninstall -n wa-covid-bot prod                                 | uninstall chart |
| repo list -n wa-covid-bot                                      | List repos      |
| status -n wa-covid-bot prod                                    | Status          |
| upgrade -n wa-covid-bot prod --values values.yml rasa-x/rasa-x | Upgrade         |
| history prod -n wa-covid-bot                                   | Release history |

### Kubectl Cheatsheet

Preface all of these commands with `kubectl` and you need to have `KUBECONFIG` set to your config file.

`export KUBECONFIG=~/.kube/wa-covid`

| CMD                                                                 | Info                |
| ------------------------------------------------------------------- | ------------------- |
| -n wa-covid-bot get pods                                            | Show running pods   |
| -n wa-covid-bot logs <pod>                                          | Show pod logs       |
| -n wa-covid-bot logs -l app.kubernetes.io/component=rasa-x --follow | logs                |
| -n wa-covid-bot describe pod <pod>                                  | Pod config          |
| -n wa-covid-bot describe pod -l app.kubernetes.io/component=app     | Pod config          |
| -n wa-covid-bot get service -l app.kubernetes.io/component=nginx    | Get ip              |
| -n wa-covid-bot exec -it <pod> -- /bin/bash                         | shell               |
| -n wa-covid-bot delete pod -l app.kubernetes.io/component=app       | Delete/restart pod  |
| -n wa-covid-bot describe pvc                                        | List claims/storage |
| -n wa-covid-bot delete pvc -l app=app                            | Delete all          |

### AWS CLI Cheatsheet

I have profiles for my id, `wa-covid` and the api `wa-covid-api`, set up ~/.aws/credentials.

| CMD | Info |
| --- | ---- |


|
