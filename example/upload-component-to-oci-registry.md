# Upload OCM Component Archive to an OCI Image

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
#### Generate a public and private key

```bash
❯ openssl genpkey -algorithm RSA -out ./private-key.pem
❯ openssl rsa -in ./private-key.pem -pubout > public-key.pem
```

### Add resources

Resources yaml:

```yaml
name: 'server'
version: '0.0.2'
type: 'ociImage'
relation: 'external'
access:
  type: 'ociRegistry'
  imageReference: 'ghcr.io/yitsushi/hello-world:1.0.7'
```

```bash
❯ ocm add resources ./hello-world-component resources.yaml
processing resources.yaml...
  processing document 1...
    processing index 0
found 1 resources
```

### Upload to OCI Registry

We can sign before we upload the component, but we can sign it after upload too.

#### Sign Local Component

```bash
❯ ocm sign componentversions -s ww-ocm-sig -K private-key.pem -k public-key.pem ./hello-world-component
applying to version "github.com/yitsushi/hello-world:1.0.7"...
  resource 0:  "name"="server": digest sha256:2f97e43aea52dede928ccd2e1bcd75325b157bd2d5e893e3cd179e6eb5de1488[ociArtifactDigest/v1]
successfully signed github.com/yitsushi/hello-world:1.0.7 (digest sha256:0452632bf29b38bc8887387019f87d459a9e88c517b744f9e5ad807bc672c479)
```

#### Login to OCI Registry

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
*** push application/vnd.gardener.cloud.cnudie.component-descriptor.v2+yaml+tar sha256:4e972b297e47151dacd2582b9acaf9a94cda0203fe148e81d4e5f59cd7b8710b: unknown-sha256:4e972b297e47151dacd2582b9acaf9a94cda0203fe148e81d4e5f59cd7b8710b
*** push application/vnd.gardener.cloud.cnudie.component.config.v1+json sha256:2eae2829e60c287ac2dabd3daed4fed9a45a021ebe0c0ff29e9db20b160f3b53: unknown-sha256:2eae2829e60c287ac2dabd3daed4fed9a45a021ebe0c0ff29e9db20b160f3b53
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
artefact-index.json
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
