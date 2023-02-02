# Best Practices for Structuring Software with OCM
TODO: Work-in-progress

## Static and Dynamic Variable Substitution

Looking at the [settings file](README.md#building-the-common-transport-archive) shows that
some variables like the `version` or the `commit` will change frequently with every build
or release. Often these will be auto-generated during build.

Other variables like the version of used 3rd-party components will change from  time to
time and will be set manually by a developer or release manager. It is useful to separate
between static and dynamic variables. Static files can be checked-in into source control and
are maintained manually. Dynamic variables can be generated during build.

Example:
manually maintained:

```yaml
NAME: microblog
COMPONENT_NAME_PREFIX: github.com/acme.org/microblog
PROVIDER: ocm.software
ELASTIC_VERSION: 8.5.1
MARIADB_VERSION: 10.6.11
MARIADB_CHART_VERSION: 11.4.2
NGINX_VERSION: 1.5.1
NGINX_CHART_VERSION: 4.4.2
```

auto generated from a build script:
```yaml
VERSION: 0.23.1
COMMIT: 5f03021059c7dbe760ac820a014a8a84166ef8b4
```

```shell
ocm add componentversions --create --file ../gen/ctf --settings ../gen/dynamic_settings.yaml --settings static_settings.yaml components.yaml
```

## Debugging: Explain the blobs directory

For analysing and debugging the transport archive some commands can help to find what is contained in the archive and what is stored in which blob:

```
tree ../gen/ctf
../gen/ctf
├── artifact-index.json
└── blobs
    ├── ...
    ├── sha256.59ff88331c53a2a94cdd98df58bc6952f056e4b2efc8120095fbc0a870eb0b67
    ├── ...
```

```shell
ocm get resources -r -o wide ../gen/ctf
...
---
REFERENCEPATH: github.com/acme.org/microblog/nginx-controller:1.5.1
NAME         : nginx-controller-chart
VERSION      : 1.5.1
IDENTITY     :
TYPE         : helmChart
RELATION     : local
ACCESSTYPE   : localBlob
ACCESSSPEC   : {"localReference":"sha256:59ff88331c53a2a94cdd98df58bc6952f056e4b2efc8120095fbc0a870eb0b67","mediaType":"application/vnd.oci.image.manifest.v1+tar+gzip","referenceName":"github.com/acme.org/microblog/nginx-controller/ingress-nginx:4.4.2"}
...
```

## Self-contained transport archives
The transport archive created from as components file by using the command `ocm add  componentversions --create ...` does not automatically resolve image references to external registries. If you want create a transport archive with all images contained as local artifact you need to convert it in a second step:

```
ocm transfer ctf --copy-resources <ctf-dir> <new-ctf-dir-or-oci-repo-url>
```

Note that this archive can become huge if there an many external images involved!

## Deployment from transport archives

TODO:

## CICD integration

Configure rarely changing variables in a static file and generate dynamic variables
during build from environment. See [explanation above](#static-and-dynamic-variable-substitution).