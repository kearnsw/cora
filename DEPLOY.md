## Rasa EKS setup

Rasa with AWS EKS and Helm. The main Rasa docs on this are [here](https://rasa.com/docs/rasa-x/installation-and-setup/openshift-kubernetes/#kubernetes-openshift). Rasa Helm chart git repo is [here](https://github.com/rasahq/rasa-x-helm).

- Create AWS EKS Cluster
  - Need an EKS role first. [This page](https://docs.aws.amazon.com/eks/latest/userguide/service_IAM_role.html) has instructions on how to check if the role exists. [This page](https://docs.aws.amazon.com/eks/latest/userguide/service_IAM_role.html#create-service-role) describes how to create the role.
  - Make sure you are in the right AWS region before creating the EKS Cluster
- [Amazon page](https://docs.aws.amazon.com/eks/latest/userguide/helm.html) on using Helm with EKS
  - [Install aws-iam-authenticator](https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html) locally first
  - [Create a kubeconfig for Amazon EKS](https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html)
    - `aws eks --region us-west-2 update-kubeconfig --name wa-covid-bot`
  - `export KUBECONFIG=~/.kube/wa-covid`

## ToDo

- Setup channel `credentials.yml` which go under `values.yml` for Helm. See [docs](https://rasa.com/docs/rasa-x/installation-and-setup/openshift-kubernetes/#configure-rasa-open-source-channels)
- Update app docker image in `values.yml` (I presume we will need this for additional libraries - dynamoDB)
- Figure out how to assign AWS instance types to Rasa node types to reduce resource usage
  - Multiple node groups?
  - Recommended [container specs](https://rasa.com/docs/rasa-x/installation-and-setup/openshift-kubernetes/#deploy-to-a-cluster-logging)
  - AWS [instance specs](https://aws.amazon.com/ec2/instance-types/)

## Rasa k8s Notes

- [Rasa Enterprise Install](https://rasa.com/docs/rasa-x/installation-and-setup/openshift-kubernetes/#rasa-enterprise-installation)
- [Creating Rasa X users](https://rasa.com/docs/rasa-x/installation-and-setup/openshift-kubernetes/#create-update-rasa-x-users)
- [HTTPS Setup](https://rasa.com/docs/rasa-x/installation-and-setup/openshift-kubernetes/#using-https)
- [Access Logs](https://rasa.com/docs/rasa-x/installation-and-setup/openshift-kubernetes/#accessing-logs)