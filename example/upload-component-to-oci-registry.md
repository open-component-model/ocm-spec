# Upload OCM Component to an OCI Registry

1. Create resources
1. Create sources
1. Create a component archive
1. Sign before
1. Upload to OCI Registry
1. Sign after (if not before)
1. Download it

## Resources

```yaml
name: 'server'
version: '0.0.2'
type: 'ociImage'
relation: 'external'
access:
  type: 'ociRegistry'
  imageReference: 'ghcr.io/yitsushi/hello-world:1.0.7'
```

## Sources

No configured sources.

## Flow

### Create Skeleton

```bash
❯ ocm create componentarchive github.com/yitsushi/hello-world 1.0.7 yitsushi hello-world-component
```

The output is a directory like this:

```
.
├── hello-world-component
│   ├── blobs
│   └── component-descriptor.yaml
├── in
    └── resources.yaml
```

The file `component-descriptor.yaml` has this content:

```yaml
component:
  componentReferences: []
  name: github.com/yitsushi/hello-world
  provider: yitsushi
  repositoryContexts: []
meta:
  schemaVersion: v2
```
#### Generate a public and private key

```bash
❯ openssl genpkey -algorithm RSA -out ./private-key.pem
❯ openssl rsa -in ./private-key.pem -pubout > public-key.pem
```

### Add resources

Create a file named `resources yaml`:

```yaml
name: 'server'
version: '0.0.1'
type: 'ociImage'
relation: 'external'
access:
  type: 'ociRegistry'
  imageReference: 'docker.io/sap/ocm:example-0.0.1'
```

```bash
❯ ocm add resources ./hello-world-component resources.yaml
processing resources.yaml...
  processing document 1...
    processing index 0
found 1 resources
```

The file `component-descriptor.yaml` then has this content:

```yaml
component:
  componentReferences: []
  name: github.com/yitsushi/hello-world
  provider: yitsushi
  repositoryContexts: []
  resources:
  - access:
      imageReference: ghcr.io/yitsushi/hello-world:1.0.7
      type: ociRegistry
    name: server
    relation: external
    type: ociImage
    version: 0.0.2
  sources: []
  version: 1.0.7
meta:
  schemaVersion: v2
```
### Add sources (optional)

For this example we do not need any sources but you can create a file `sources.yaml` the same way and
add it to the component-descriptor with `ocm add sources ...`

### Upload to OCI Registry

We can sign before we upload the component, but we can sign it after upload too.

#### Sign Local Component (optional)

```bash
❯ ocm sign componentversions -s ww-ocm-sig -K private-key.pem -k public-key.pem ./hello-world-component
applying to version "github.com/yitsushi/hello-world:1.0.7"...
  resource 0:  "name"="server": digest sha256:2f97e43aea52dede928ccd2e1bcd75325b157bd2d5e893e3cd179e6eb5de1488[ociArtifactDigest/v1]
successfully signed github.com/yitsushi/hello-world:1.0.7 (digest sha256:0452632bf29b38bc8887387019f87d459a9e88c517b744f9e5ad807bc672c479)
```

The file `component-descriptor.yaml` then has this content:

```yaml
component:
  componentReferences: []
  name: github.com/sap/ocm-basic-flow
  provider: sap
  repositoryContexts: []
  resources:
  - access:
      imageReference: ghcr.io/yitsushi/hello-world:1.0.7
      type: ociRegistry
    digest:
      hashAlgorithm: sha256
      normalisationAlgorithm: ociArtifactDigest/v1
      value: 2f97e43aea52dede928ccd2e1bcd75325b157bd2d5e893e3cd179e6eb5de1488
    name: server
    relation: external
    type: ociImage
    version: 0.0.2
  sources: []
  version: 0.0.1
meta:
  schemaVersion: v2
signatures:
- digest:
    hashAlgorithm: sha256
    normalisationAlgorithm: jsonNormalisation/v1
    value: d0503b73aa55ee9c6cec8d5c342f8333dd4b93490081919e3f07a745318cabfe
  name: sap-ocm-sig
  signature:
    algorithm: RSASSA-PKCS1-V1_5
    mediaType: application/vnd.ocm.signature.rsa
    value: 3fba054401ffd9c94942ac4cb10175ce54e081f98413ddff1159f50a36bb7a44e6396f1ca4e847f12518c5aea1c9f3c9096235aacd05753a0d55eaa11bb63b7ae2f61fb182c6753795b1762f84b2eeebf718fb3807938b6ebb414cac21889c24fb401093e33798b47f798241efec9b7b0d45d9aba0cb1aaf0ba9e5207c17e7dbf5274dd4eb670c47c1f258b3c1b4fe2c9e94be8247a658bf64b06523e0c13590308afb1991fefa10c2c0bc3f95c16b035ca54a1529fdba6edbaed40509d975a81367fa71619ab13a2918a66c64bc403f80fdf2839951d2b318990308c35847162958994ebbad3669a00b342563b886b3fc5d026555dfe6d6b6e78479d76e481b
```

#### Login to OCI Registry

The command-line-client can reuse docker credentials for authenticating against an OCI registry with a correspondig configuration (see `ocm -h` for more information). For doing the upload you will need write access to an OCI registry.

```bash
# General format
docker login registry.address.tld

# Docker Hub
docker login

# GitHub Container Registry
# For password use a Personal Access Token.
docker login ghcr.io
```

#### Upload

```bash
❯ ocm  transfer componentarchive ./hello-world-component  ghcr.io/sap
transferring version "github.com/yitsushi/hello-world:1.0.7"...
INFO[0000] trying next host - response was http.StatusNotFound  host=ghcr.io
INFO[0001] trying next host - response was http.StatusNotFound  host=ghcr.io
...adding component version...
*** push application/vnd.ocm.software.component-descriptor.v2+yaml+ta sha256:4e972b297e47151dacd2582b9acaf9a94cda0203fe148e81d4e5f59cd7b8710b: unknown-sha256:4e972b297e47151dacd2582b9acaf9a94cda0203fe148e81d4e5f59cd7b8710b
*** push application/vnd.ocm.software.component.config.v1+json sha256:2eae2829e60c287ac2dabd3daed4fed9a45a021ebe0c0ff29e9db20b160f3b53: unknown-sha256:2eae2829e60c287ac2dabd3daed4fed9a45a021ebe0c0ff29e9db20b160f3b53
*** push application/vnd.oci.image.manifest.v1+json sha256:d3418290d87f05f52c1801557c00d3e43eb0bcf1bb960331b3967c639541582f: manifest-sha256:d3418290d87f05f52c1801557c00d3e43eb0bcf1bb960331b3967c639541582f
pusher for ghcr.io/sap/component-descriptors/github.com/yitsushi/hello-world:1.0.7
pushing 1.0.7
*** push application/vnd.oci.image.manifest.v1+json sha256:d3418290d87f05f52c1801557c00d3e43eb0bcf1bb960331b3967c639541582f: manifest-sha256:d3418290d87f05f52c1801557c00d3e43eb0bcf1bb960331b3967c639541582f
```

#### Sign Remote OCI Registry

```bash
❯ ocm sign componentversion \
    --signature ww-ocm-sig \
    -k public-key.pem -K private-key.pem \
    --repo OCIRepository::ghcr.io/sap \
    github.com/yitsushi/hello-world:1.0.7
applying to version "github.com/yitsushi/hello-world:1.0.7"...
  resource 0:  "name"="server": digest sha256:2f97e43aea52dede928ccd2e1bcd75325b157bd2d5e893e3cd179e6eb5de1488[ociArtifactDigest/v1]
successfully signed github.com/yitsushi/hello-world:1.0.7 (digest sha256:0452632bf29b38bc8887387019f87d459a9e88c517b744f9e5ad807bc672c479)
```

#### Verify

```bash
❯ ocm verify componentversion \
    --signature ww-ocm-sig \
    --public-key=public-key.pem \
    --repo OCIRepository::ghcr.io/sap \
    github.com/yitsushi/hello-world:1.0.7
applying to version "github.com/yitsushi/hello-world:1.0.7"...
  resource 0:  "name"="server": digest sha256:2f97e43aea52dede928ccd2e1bcd75325b157bd2d5e893e3cd179e6eb5de1488[ociArtifactDigest/v1]
successfully verified github.com/yitsushi/hello-world:1.0.7 (digest sha256:0452632bf29b38bc8887387019f87d459a9e88c517b744f9e5ad807bc672c479)
```

### Download it

```bash
❯ ocm transfer components -t tgz \
    --repo ghcr.io/sap github.com/yitsushi/hello-world:1.0.7 \
    ./ctf.tgz
transferring version "github.com/yitsushi/hello-world:1.0.7"...
...adding component version...
1 versions transferred
```

#### Verify content

```bash
❯ tar ztf ctf.tgz
artifact-index.json
blobs
blobs/sha256.2eae2829e60c287ac2dabd3daed4fed9a45a021ebe0c0ff29e9db20b160f3b53
blobs/sha256.4e972b297e47151dacd2582b9acaf9a94cda0203fe148e81d4e5f59cd7b8710b
blobs/sha256.d3418290d87f05f52c1801557c00d3e43eb0bcf1bb960331b3967c639541582f
```

#### Verfify signature

```bash
❯ ocm verify componentversion \
    --signature ww-ocm-sig --public-key=public-key.pem \
    ./ctf.tgz
applying to version "github.com/yitsushi/hello-world:1.0.7"...
  resource 0:  "name"="server": digest sha256:2f97e43aea52dede928ccd2e1bcd75325b157bd2d5e893e3cd179e6eb5de1488[ociArtifactDigest/v1]
successfully verified github.com/yitsushi/hello-world:1.0.7 (digest sha256:0452632bf29b38bc8887387019f87d459a9e88c517b744f9e5ad807bc672c479)
```
