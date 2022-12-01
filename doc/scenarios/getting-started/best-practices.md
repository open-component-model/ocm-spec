# Best Practices for working with the Open-Component-Model

This chapter contains guidelines for common scenarios how to work with the Open Component Model.

- [Best Practices for working with the Open-Component-Model](#best-practices-for-working-with-the-open-component-model)
  - [Building multiarch images](#building-multiarch-images)
  - [Separate between Build and Publish](#separate-between-build-and-publish)
  - [Templating input files](#templating-input-files)
  - [Using Makefiles](#using-makefiles)
  - [Pipeline integration](#pipeline-integration)


## Building multiarch images
At the time of writing this guide Docker is not able to build multi-architecture (multiarch)
images natively. Instead the `buildx` plugin is used. However this implies building and pushing
images in one step to a remote container registry as the local docker image store does not
support multi-arch images.

The OCM CLI has therefore some built-in support for dealing with multi-arch images. This allows
building all artifacts locally and push them in a separate step to a container registry. This
is done by building single-arch images in a first step (still using `buildx` for cross-platform
building). In a second step all images are bundled in a component (CA) or common transport (CTF)
archive. This archive can be processed as usual (e.g. for signing or transfer to other locations).
When pushed to an image registry multi-arch images are generated with a multi-arch-image manifest.

The following steps illustrate this procedure. For a simple project with a Go binary and a
helm-chart assume the following file structure:

```shell
 tree .
.
├── Dockerfile
├── go.mod
├── helmchart
│   ├── Chart.yaml
│   ├── templates
│   │   ├── ...
│   └── values.yaml
└── main.go
```

The dockerfile has the following content:

```Dockerfile
FROM golang:1.19 AS builder

WORKDIR /app
COPY go.mod ./
COPY main.go ./
# RUN go mod download
RUN go build -o /helloserver main.go

# Create a new release build stage
FROM gcr.io/distroless/base-debian10

# Set the working directory to the root directory path
WORKDIR /
# Copy over the binary built from the previous stage
COPY --from=builder /helloserver /helloserver

ENTRYPOINT ["/helloserver"]
```

Now we want to build images for two platforms using docker and buildx. Note the `--load` option for
`buildx` to store the image in the local docker store. Note the architecture suffix in the tag to be
able to distinguish the images for the different platforms. Note also that the tag has a different
syntax than the `--platform` argument for `buildx` as slashes are not allowed in tags.

```shell
$ TAG_PREFIX=eu.gcr.io/my-project/acme # path to you OCI registry
$ PLATFORM=linux/amd64
$ VERSION=0.1.0

$ docker buildx build --load -t ${TAG_PREFIX}/simpleserver:0.1.0-linux-amd64 --platform linux/amd64 .
[+] Building 54.4s (14/14) FINISHED
 => [internal] load build definition from Dockerfile                                                                          0.0s
 => => transferring dockerfile: 660B                                                                                          0.0s
 => [internal] load .dockerignore                                                                                             0.0s
 => => transferring context: 2B                                                                                               0.0s
 => [internal] load metadata for gcr.io/distroless/base-debian10:latest                                                       1.6s
 => [internal] load metadata for docker.io/library/golang:1.19                                                                1.2s
 => [builder 1/5] FROM docker.io/library/golang:1.19@sha256:dc76ef03e54c34a00dcdca81e55c242d24b34d231637776c4bb5c1a8e851425  49.2s
 => => resolve docker.io/library/golang:1.19@sha256:dc76ef03e54c34a00dcdca81e55c242d24b34d231637776c4bb5c1a8e8514253          0.0s
 => => sha256:14a70245b07c7f5056bdd90a3d93e37417ec26542def5a37ac8f19e437562533 156B / 156B                                    0.2s
 => => sha256:a2b47720d601b6c6c6e7763b4851e25475118d80a76be466ef3aa388abf2defd 148.91MB / 148.91MB                           46.3s
 => => sha256:52908dc1c386fab0271a2b84b6ef4d96205a98a8c8801169554767172e45d8c7 85.97MB / 85.97MB                             42.9s
 => => sha256:195ea6a58ca87a18477965a6e6a8623112bde82c5b568a29c56ce4581b6e6695 54.59MB / 54.59MB                             33.8s
 => => sha256:c85a0be79bfba309d1f05dc40b447aa82b604593531fed1e7e12e4bef63483a5 10.88MB / 10.88MB                              3.4s
 => => sha256:e4e46864aba2e62ba7c75965e4aa33ec856ee1b1074dda6b478101c577b63abd 5.16MB / 5.16MB                                1.5s
 => => sha256:a8ca11554fce00d9177da2d76307bdc06df7faeb84529755c648ac4886192ed1 55.04MB / 55.04MB                             19.3s
 => => extracting sha256:a8ca11554fce00d9177da2d76307bdc06df7faeb84529755c648ac4886192ed1                                     1.1s
 => => extracting sha256:e4e46864aba2e62ba7c75965e4aa33ec856ee1b1074dda6b478101c577b63abd                                     0.1s
 => => extracting sha256:c85a0be79bfba309d1f05dc40b447aa82b604593531fed1e7e12e4bef63483a5                                     0.1s
 => => extracting sha256:195ea6a58ca87a18477965a6e6a8623112bde82c5b568a29c56ce4581b6e6695                                     1.1s
 => => extracting sha256:52908dc1c386fab0271a2b84b6ef4d96205a98a8c8801169554767172e45d8c7                                     1.5s
 => => extracting sha256:a2b47720d601b6c6c6e7763b4851e25475118d80a76be466ef3aa388abf2defd                                     2.8s
 => => extracting sha256:14a70245b07c7f5056bdd90a3d93e37417ec26542def5a37ac8f19e437562533                                     0.0s
 => [stage-1 1/3] FROM gcr.io/distroless/base-debian10@sha256:101798a3b76599762d3528635113f0466dc9655ecba82e8e33d410e2bf5cd  30.7s
 => => resolve gcr.io/distroless/base-debian10@sha256:101798a3b76599762d3528635113f0466dc9655ecba82e8e33d410e2bf5cd319        0.0s
 => => sha256:f291067d32d8d06c3b996ba726b9aa93a71f6f573098880e05d16660cfc44491 8.12MB / 8.12MB                               30.6s
 => => sha256:2445dbf7678f5ec17f5654ac2b7ad14d7b1ea3af638423fc68f5b38721f25fa4 657.02kB / 657.02kB                            1.3s
 => => extracting sha256:2445dbf7678f5ec17f5654ac2b7ad14d7b1ea3af638423fc68f5b38721f25fa4                                     0.1s
 => => extracting sha256:f291067d32d8d06c3b996ba726b9aa93a71f6f573098880e05d16660cfc44491                                     0.1s
 => [internal] load build context                                                                                             0.1s
 => => transferring context: 575B                                                                                             0.0s
 => [builder 2/5] WORKDIR /app                                                                                                0.1s
 => [builder 3/5] COPY go.mod ./                                                                                              0.0s
 => [builder 4/5] COPY main.go ./                                                                                             0.0s
 => [builder 5/5] RUN go build -o /helloserver main.go                                                                        2.4s
 => [stage-1 2/3] COPY --from=builder /helloserver /helloserver                                                               0.0s
 => exporting to oci image format                                                                                             0.8s
 => => exporting layers                                                                                                       0.2s
 => => exporting manifest sha256:04d69fc3245757d327d96b1a83b7a64543d970953c61d1014ae6980ed8b3ba2a                             0.0s
 => => exporting config sha256:08641d64f612661a711587b07cfeeb6d2804b97998cfad85864a392c1aabcd06                               0.0s
 => => sending tarball                                                                                                        0.6s
 => importing to docker
```

Repeat this command for the second platform:

```shell
$ docker buildx build --load -t ${TAG_PREFIX}/simpleserver:0.1.0-linux-arm64 --platform linux/arm64 .
docker buildx build --load -t ${TAG_PREFIX}/simpleserver:0.1.0-linux-arm64 --platform linux/arm64 .
[+] Building 40.1s (14/14) FINISHED
 => [internal] load .dockerignore                                                                                             0.0s
 => => transferring context: 2B                                                                                               0.0s
 => [internal] load build definition from Dockerfile                                                                          0.0s
 => => transferring dockerfile: 660B                                                                                          0.0s
 => [internal] load metadata for gcr.io/distroless/base-debian10:latest                                                       1.0s
 => [internal] load metadata for docker.io/library/golang:1.19                                                                1.1s
 => [builder 1/5] FROM docker.io/library/golang:1.19@sha256:dc76ef03e54c34a00dcdca81e55c242d24b34d231637776c4bb5c1a8e851425  37.7s
 => => resolve docker.io/library/golang:1.19@sha256:dc76ef03e54c34a00dcdca81e55c242d24b34d231637776c4bb5c1a8e8514253          0.0s
 => => sha256:cd807e8b483974845eabbdbbaa4bb3a66f74facd8c061e01e923e9f1da608271 157B / 157B                                    0.2s
 => => sha256:fecd6ba4b3f93b6c90f4058b512f1b0a44223ccb3244f0049b16fe2c1b41cf45 115.13MB / 115.13MB                           35.6s
 => => sha256:4fb255e3f99867ec7a2286dfbbef990491cde0a5d226d92be30bad4f9e917fa4 81.37MB / 81.37MB                             31.8s
 => => sha256:426e8acfed2a5373bd99b22b5a968d55a148e14bc0e0f51c5cf0d779afefe291 54.68MB / 54.68MB                             26.7s
 => => sha256:3d7b1480fa4dae5cbbb7d091c46ae0ae52f501418d4cfeb849b87023364e2564 10.87MB / 10.87MB                              3.0s
 => => sha256:a3e29af4daf3531efcc63588162e8bdcf3434aa5d72df4eabeb5e20c6695e303 5.15MB / 5.15MB                                1.3s
 => => sha256:077c13527d405646e2f6bb426e04716ae4f8dd2fdd8966dcb0194564a2b57896 53.70MB / 53.70MB                             13.3s
 => => extracting sha256:077c13527d405646e2f6bb426e04716ae4f8dd2fdd8966dcb0194564a2b57896                                     0.9s
 => => extracting sha256:a3e29af4daf3531efcc63588162e8bdcf3434aa5d72df4eabeb5e20c6695e303                                     0.3s
 => => extracting sha256:3d7b1480fa4dae5cbbb7d091c46ae0ae52f501418d4cfeb849b87023364e2564                                     0.1s
 => => extracting sha256:426e8acfed2a5373bd99b22b5a968d55a148e14bc0e0f51c5cf0d779afefe291                                     1.2s
 => => extracting sha256:4fb255e3f99867ec7a2286dfbbef990491cde0a5d226d92be30bad4f9e917fa4                                     1.4s
 => => extracting sha256:fecd6ba4b3f93b6c90f4058b512f1b0a44223ccb3244f0049b16fe2c1b41cf45                                     2.0s
 => => extracting sha256:cd807e8b483974845eabbdbbaa4bb3a66f74facd8c061e01e923e9f1da608271                                     0.0s
 => [stage-1 1/3] FROM gcr.io/distroless/base-debian10@sha256:101798a3b76599762d3528635113f0466dc9655ecba82e8e33d410e2bf5cd  25.7s
 => => resolve gcr.io/distroless/base-debian10@sha256:101798a3b76599762d3528635113f0466dc9655ecba82e8e33d410e2bf5cd319        0.0s
 => => sha256:21d6a6c3921f47fb0a96eb028b4c3441944a6e5a44b30cd058425ccc66279760 7.13MB / 7.13MB                               25.5s
 => => sha256:7d441aeb75fe3c941ee4477191c6b19edf2ad8310bac7356a799c20df198265c 657.02kB / 657.02kB                            1.3s
 => => extracting sha256:7d441aeb75fe3c941ee4477191c6b19edf2ad8310bac7356a799c20df198265c                                     0.1s
 => => extracting sha256:21d6a6c3921f47fb0a96eb028b4c3441944a6e5a44b30cd058425ccc66279760                                     0.1s
 => [internal] load build context                                                                                             0.0s
 => => transferring context: 54B                                                                                              0.0s
 => [builder 2/5] WORKDIR /app                                                                                                0.2s
 => [builder 3/5] COPY go.mod ./                                                                                              0.0s
 => [builder 4/5] COPY main.go ./                                                                                             0.0s
 => [builder 5/5] RUN go build -o /helloserver main.go                                                                        0.3s
 => [stage-1 2/3] COPY --from=builder /helloserver /helloserver                                                               0.0s
 => exporting to oci image format                                                                                             0.5s
 => => exporting layers                                                                                                       0.2s
 => => exporting manifest sha256:267ed1266b2b0ed74966e72d4ae8a2dfcf77777425d32a9a46f0938c962d9600                             0.0s
 => => exporting config sha256:67102364e254bf5a8e58fa21ea56eb40645851d844f5c4d9651b4af7a40be780                               0.0s
 => => sending tarball                                                                                                        0.3s
 => importing to docker
```

Check that the images were created correctly:
```shell
$ docker image ls
REPOSITORY                                              TAG                 IMAGE ID       CREATED              SIZE
eu.gcr.io/acme/simpleserver   0.1.0-linux-arm64   67102364e254   6 seconds ago        22.4MB
eu.gcr.io/acme/simpleserver   0.1.0-linux-amd64   08641d64f612   About a minute ago   25.7MB
```

In the next step we create a component archive and a transport archive
```shell
$ PROVIDER=acme
$ COMPONENT=github.com/$(PROVIDER)/simpleserver
$ VERSION=0.1.0
$ mkdir gen
$ ocm create ca ${COMPONENT} ${VERSION} --provider ${PROVIDER} --file gen/ca
```

Create the file `resources.yaml`. Note the variants in the image input and the type `dockermulti`:

```yaml
---
name: chart
type: helmChart
input:
  type: helm
  path: helmchart
---
name: image
type: ociImage
version: 0.1.0
input:
  type: dockermulti
  repository: eu.gcr.io/acme/simpleserver
  variants:
  - "eu.gcr.io/acme/simpleserver:0.1.0-linux-amd64"
  - "eu.gcr.io/acme/simpleserver:0.1.0-linux-arm64"
```

Create the component archive:

```shell
$ ocm add resources ./gen/ca resources.yaml
processing resources.yaml...
  processing document 1...
    processing index 1
  processing document 2...
    processing index 1
found 2 resources
adding resource helmChart: "name"="chart","version"="<componentversion>"...
adding resource ociImage: "name"="image","version"="0.1.0"...
  image 0: eu.gcr.io/acme/simpleserver:0.1.0-linux-amd64
  image 1: eu.gcr.io/acme/simpleserver:0.1.0-linux-arm64
  image 2: INDEX
locator: github.com/acme/simpleserver, repo: eu.gcr.io/acme/simpleserver, version 0.1.0
```

The resulting `component-descriptor.yaml` in `gen/ca` is:

```shell
component:
  componentReferences: []
  name: github.com/acme/simpleserver
  provider: acme
  repositoryContexts: []
  resources:
  - access:
      localReference: sha256.9dd0f2cbae3b8e6eb07fa947c05666d544c0419a6e44bd607e9071723186333b
      mediaType: application/vnd.oci.image.manifest.v1+tar+gzip
      referenceName: github.com/acme/simpleserver/helloserver:0.1.0
      type: localBlob
    name: chart
    relation: local
    type: helmChart
    version: 0.1.0
  - access:
      localReference: sha256.4e26c7dd46e13c9b1672e4b28a138bdcb086e9b9857b96c21e12839827b48c0c
      mediaType: application/vnd.oci.image.index.v1+tar+gzip
      referenceName: github.com/acme/simpleserver/eu.gcr.io/acme/simpleserver:0.1.0
      type: localBlob
    name: image
    relation: local
    type: ociImage
    version: 0.1.0
  sources: []
  version: 0.1.0
meta:
  schemaVersion: v2
```

Note that there is only one resource of type `image` with media-type `application/vnd.oci.image.index.v1+tar+gzip`
which is the standard media type for multiarch-images.

<details><summary>Analyzing the blobs directory </summary>

```shell
$ ls -l gen/ca/blobs
total 24M
-rw-r--r-- 1 d058463 staff  24M Dec  1 09:50 sha256.4e26c7dd46e13c9b1672e4b28a138bdcb086e9b9857b96c21e12839827b48c0c
-rw-r--r-- 1 d058463 staff 4.7K Dec  1 09:50 sha256.9dd0f2cbae3b8e6eb07fa947c05666d544c0419a6e44bd607e9071723186333b
```

The file sha256.4e26... contains the multi-arch image:

```shell
$ tar tvf gen/ca/blobs/sha256.4e26c7dd46e13c9b1672e4b28a138bdcb086e9b9857b96c21e12839827b48c0c
-rw-r--r--  0 0      0         741 Jan  1  2022 index.json
-rw-r--r--  0 0      0          38 Jan  1  2022 oci-layout
drwxr-xr-x  0 0      0           0 Jan  1  2022 blobs
-rw-r--r--  0 0      0     3051520 Jan  1  2022 blobs/sha256.05ef21d763159987b9ec5cfb3377a61c677809552dcac3301c0bde4e9fd41bbb
-rw-r--r--  0 0      0         723 Jan  1  2022 blobs/sha256.117f12f0012875471168250f265af9872d7de23e19f0d4ef05fbe99a1c9a6eb3
-rw-r--r--  0 0      0     6264832 Jan  1  2022 blobs/sha256.1496e46acd50a8a67ce65bac7e7287440071ad8d69caa80bcf144892331a95d3
-rw-r--r--  0 0      0     6507520 Jan  1  2022 blobs/sha256.66817c8096ad97c6039297dc984ebc17c5ac9325200bfa9ddb555821912adbe4
-rw-r--r--  0 0      0         491 Jan  1  2022 blobs/sha256.75a096351fe96e8be1847a8321bd66535769c16b2cf47ac03191338323349355
-rw-r--r--  0 0      0     3051520 Jan  1  2022 blobs/sha256.77192cf194ddc77d69087b86b763c47c7f2b0f215d0e4bf4752565cae5ce728d
-rw-r--r--  0 0      0        1138 Jan  1  2022 blobs/sha256.91018e67a671bbbd7ab875c71ca6917484ce76cde6a656351187c0e0e19fe139
-rw-r--r--  0 0      0    17807360 Jan  1  2022 blobs/sha256.91f7bcfdfda81b6c6e51b8e1da58b48759351fa4fae9e6841dd6031528f63b4a
-rw-r--r--  0 0      0        1138 Jan  1  2022 blobs/sha256.992b3b72df9922293c05f156f0e460a220bf601fa46158269ce6b7d61714a084
-rw-r--r--  0 0      0    14755840 Jan  1  2022 blobs/sha256.a83c9b56bbe0f6c26c4b1d86e6de3a4862755d208c9dfae764f64b210eafa58c
-rw-r--r--  0 0      0         723 Jan  1  2022 blobs/sha256.e624040295fb78a81f4b4b08b43b4de419f31f21074007df8feafc10dfb654e6

$ tar xvf gen/ca/blobs/sha256.4e26c7dd46e13c9b1672e4b28a138bdcb086e9b9857b96c21e12839827b48c0c -O - index.json | jq .
x index.json
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.index.v1+json",
  "manifests": [
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:e624040295fb78a81f4b4b08b43b4de419f31f21074007df8feafc10dfb654e6",
      "size": 723
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:117f12f0012875471168250f265af9872d7de23e19f0d4ef05fbe99a1c9a6eb3",
      "size": 723
    },
    {
      "mediaType": "application/vnd.oci.image.index.v1+json",
      "digest": "sha256:75a096351fe96e8be1847a8321bd66535769c16b2cf47ac03191338323349355",
      "size": 491,
      "annotations": {
        "org.opencontainers.image.ref.name": "0.1.0",
        "software.ocm/tags": "0.1.0"
      }
    }
  ],
  "annotations": {
    "software.ocm/main": "sha256:75a096351fe96e8be1847a8321bd66535769c16b2cf47ac03191338323349355"
  }
}
```
</details>

You can create a transport archive from the component archive.

```shell
cm transfer ca gen/ca gen/ctf
transferring version "github.com/acme/simpleserver:0.1.0"...
...resource 0(github.com/acme/simpleserver/helloserver:0.1.0)...
...resource 1(github.com/acme/simpleserver/eu.gcr.io/acme/simpleserver:0.1.0)...
...adding component version...
```

Or you can push it directly to the OCM repository:

```shell
$ OCMREPO=ghcr.io/${PROVIDER}
$ ocm transfer ca gen/ca $OCMREPO
transferring version "github.com/acme/simpleserver:0.1.0"...
...resource 0(github.com/acme/simpleserver/helloserver:0.1.0)...
...resource 1(github.com/acme/simpleserver/eu.gcr.io/acme/simpleserver:0.1.0)...
...adding component version...
```

The repository then should contain three additional artifacts. Depending on the OCI registry and
their corresponding UIs you may see that the uploaded OCI image is a multiarch-image. For example on
github packages you can see under `OS/Arch` that there are two platforms `linux/amd64` and
`linux/arm64`

For better automation and reuse you may consider templating resource files and makefiles (see below)

## Separate between Build and Publish
* CTF as contract between build and build system
* do not push in build, create a CTF
* allows e.g. signing before pushing

## Templating input files
* resources.yaml can be templated

## Using Makefiles
Developing with the Open Component Model usually is an iterative process of building artifacts, publishing them, generating component descriptors and analyzing them. This implies repeating commands with many parameters and modifying input files again and again. To simplify and speedup this process a `Makefile` and the `make` utility can be helpful. The following example can be used as a starting point and modified according to your needs.

We use the following file system layout for this example

```shell

```

```makefile
```

## Pipeline integration

