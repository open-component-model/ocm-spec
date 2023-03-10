# Deploying Software with OCM

- [Deploying Software with OCM](#deploying-software-with-ocm)
  - [Introduction](#introduction)
  - [Localization](#localization)
  - [Example](#example)

## Introduction

In the chapter [Structuring Sofware with OCM](../structuring/README.md) we have created a transport
archive containig all required parts (images, helm charts) for installing the application. This
archive is self-contained and can be transferred with a single command from the OCM tooling. After
pushing this archive to an OCI-registry we have a shared location that can be used as a s source of
deployment without any external references. As an alternative you can transport the archive using
other mechanisms (file transfer, USB-stick) and push it on a target location to an OCI registry.

To actually deploy the application we need to get access to the helm charts contained in the archive.
We can use the ocm CLI to retrieve their location. See the [example](#example) below.

## Localization

The deployments in a Kubernetes cluster require an image for instantiating a container. With each
transport of the archive the image location changes. The image location can be set as a helm value
for a helm based installation. The actual value for the current deployment has to be extracted from
the component-descriptor and inserted into a helm values file for a helm based installation. In the
example below we will do the necessary steps. For real deplyoments you will usually use tools to
automate this. The
[toi installation toolkit](https://github.com/open-component-model/ocm/blob/main/docs/reference/ocm_bootstrap_componentversions_toi-bootstrapping.md)
is one tool supporting this. The [Flux OCM controllers](https://ocm.software/docs/guides/getting-started-with-ocm-flux/)
offer this functionality too.

## Example
Let's assume that we have pushed the transport archive to an OCI registry. We need the identity of the
component version and the location of the component-descriptors in the OCI registry:

ComponentVersion:
name: `github.com/jensh007/microblog-deployment`
version: `0.23.1`

URL of OCI registry: `ghcr.io/acme.org/microblogapp`

It is convenient to put this into an environment variable:

```yaml
OCMREPO=github.com/acme.org/microblog
```

Getting all component-versions of the application with the ocm cli:

```yaml
ocm get component ${OCM_REPO}//github.com/jensh007/microblog-deployment:0.23.1 -o yaml

---
context: []
element:
  component:
    componentReferences:
    - componentName: github.com/jensh007/microblog
      name: microblog
      version: 0.23.1
    - componentName: github.com/jensh007/nginx-controller
      name: nginx-controller
      version: 1.5.1
    - componentName: github.com/jensh007/mariadb
      name: mariadb
      version: 10.11.2
    - componentName: github.com/jensh007/elasticsearch
      name: elasticsearch
      version: 8.5.1
    - componentName: github.com/jensh007/redis
      name: redis
      version: 7.0.9
    name: github.com/jensh007/microblog-deployment
    provider:
      name: ocm.software
    repositoryContexts:
    ...
    resources: []
    sources: []
    version: 0.23.1
  meta:
    ...
```

With this we can drill down to the installable helm charts and the container images:

```shell
ocm get resource ${OCM_REPO}//github.com/jensh007/microblog:0.23.1 -o wide

NAME            VERSION IDENTITY TYPE      RELATION ACCESSTYPE  ACCESSSPEC
microblog-chart 0.23.1           helmChart local    ociArtifact {"imageReference":"ghcr.io/acme.org/microblogapp/github.com/jensh007/microblog/microblog:0.23.1"}
microblog-image 0.23.1           ociImage  local    ociArtifact {"imageReference":"ghcr.io/acme.org/microblogapp/github.com/jensh007/microblog/images/microblog:0.23.1"}
```

With this information we can create  a helm values file with the updated image reference:

`microblog_values_localized.yaml`:

```yaml
image:
    repository: ghcr.io/acme.org/microblogapp/github.com/jensh007/microblog/images/microblog
    tag: "0.23.1"
imagePullSecrets:
  - name: gcr-secret
```

For a private registry you may also need to specify an image pull secret. This secret has to be present on the target cluster before calling helm commands.

```yaml
image:
    ...
imagePullSecrets:
  - name: gcr-secret
```

Note: For a real application deployment there will be more localized settings. Number of replicas, domain names in Ingress specs are typical examples.

The following steps will act on a target cluster. For this we assume that your `KUBECONFIG` enviroment variable is set correctly (or append `--kubeconfig` option).
We will need a namespace in the target cluster. We use the namespace `dev`for this example:

```
kubectl create namespace dev
```

With the localized values we can instruct `helm` to perform an installation:

```shell
helm install -n dev microblog oci://ghcr.io/acme.org/microblogapp/github.com/jensh007/microblog/microblog --version 0.23.1  --values microblog_values_localized.yaml

Pulled: ghcr.io/acme.org/microblogapp/github.com/jensh007/microblog/microblog:0.23.1
Digest: sha256:2841665cf3f669ed0a45e70c77bbe27a91ae4dde2d119117ae1e7c1f486ce510
NAME: microblog
LAST DEPLOYED: Fri Mar 10 09:28:04 2023
NAMESPACE: dev
STATUS: deployed
REVISION: 1
NOTES:
1. Get the application URL by running these commands:
  https://microblog.ocm2.hubforplay.shoot.canary.k8s-hana.ondemand.com/

```

This command instructs helm to create a helm release named `microblog` and use the
helm chart from our OCI-registry. The location was grabbed from the command above.

If the command succeeds you can retrieve the status with:

```shell
helm list
NAME     	NAMESPACE	REVISION	UPDATED                             	STATUS  	CHART              	APP VERSION
microblog	dev      	1       	2023-03-10 09:28:04.658464 +0100 CET	deployed	microblog-0.23.1   	0.23.1
```

You can also check the created pod:

```shell
kubectl get pods
NAME                                              READY   STATUS             RESTARTS      AGE
microblog-7c65dc4d9d-tvr97                        0/2     CrashLoopBackOff   10 (5s ago)   6m5s

k describe pod microblog-7c65dc4d9d-tvr97

...
Containers:
  microblog:
    ...
    Image:         ghcr.io/acme.org/microblogapp/github.com/jensh007/microblog/images/microblog:0.23.1
...

```

The pod is not in the status running yet because it is missing the required dependencies. We need to perform the additional steps to install them. The steps are the same so we do not repeat them in detail again:

```shell
ocm get resource ${OCM_REPO}//github.com/jensh007/nginx-controller:1.5.1 -o wide
ocm get resource ${OCM_REPO}//github.com/jensh007/mariadb:10.11.2 -o wide
ocm get resource ${OCM_REPO}//github.com/jensh007/elasticsearch:8.5.1 -o wide
ocm get resource ${OCM_REPO}//github.com/jensh007/redis:7.09 -o wide
```

Create files:

* nginx_values_localized.yaml
* mariadb_values_localized.yaml
* elasticsearch_values_localized.yaml
* redis_values_localized.yaml

and install with:

```
helm install -n dev nginx oci://ghcr.io/acme.org/microblogapp/github.com/jensh007/nginx-controller/ingress-nginx --version 4.4.2 --values nginx_values_localized.yaml
helm install -n dev mariadb oci://ghcr.io/acme.org/microblogapp/github.com/jensh007/mariadb/mariadb --version 11.4.2 --values mariadb_values_localized.yaml
helm install -n dev elasticsearch oci://ghcr.io/acme.org/microblogapp/github.com/jensh007/elasticsearch/elasticsearch --version 8.5.1 --values elasticsearch_values_localized.yaml
helm install -n dev redis oci://ghcr.io/acme.org/microblogapp/github.com/jensh007/redis/redis --version 17.6.0 --values redis_values_localized.yaml
```

