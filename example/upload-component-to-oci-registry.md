# Upload OCM Component Archive to an OCI Image

1. Create resources
1. Create sources
1. Create a component archive
1. Download images ( optional )
1. Prepare for transfer
1. Create a transport archive
1. Sign it
1. Transfer the archive, verify, and extract

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
❯ ocm create componentarchive docker.io/sap/ocm-oci-flow 0.0.2 sap ocm-oci-flow
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
❯ ocm add resources ./ocm-oci-flow resources.yaml
```

### Upload to OCI Registry

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
❯ ocm  transfer componentarchive ./ocm-oci-flow ghcr.io/sap/ocm-oci-flow
transferring version "ghcr.io/sap/ocm-oci-flow:0.0.2"...
INFO[0000] trying next host - response was http.StatusNotFound  host=ghcr.io
INFO[0001] trying next host - response was http.StatusNotFound  host=ghcr.io
...adding component version...
*** push application/vnd.gardener.cloud.cnudie.component-descriptor.v2+yaml+tar sha256:6fd2a92abaa31ed5c6bc06c22a50a1e44edad4b940cec3b803797dc78e7bfaa8: unknown-sha256:6fd2a92abaa31ed5c6bc06c22a50a1e44edad4b940cec3b803797dc78e7bfaa8
*** push application/vnd.gardener.cloud.cnudie.component.config.v1+json sha256:6d9117f30e603140e3f04e501456ea6e6c0178af5f417c35b3a36ebcdb955dcd: unknown-sha256:6d9117f30e603140e3f04e501456ea6e6c0178af5f417c35b3a36ebcdb955dcd
*** push application/vnd.oci.image.manifest.v1+json sha256:36dca94e452f6bbd75c22c3c93590f527e0ecf0ce3f1c4fbe23a97b44aa1a6b1: manifest-sha256:36dca94e452f6bbd75c22c3c93590f527e0ecf0ce3f1c4fbe23a97b44aa1a6b1
pusher for ghcr.io/sap/ocm-oci-flow/component-descriptors/ghcr.io/sap/ocm-oci-flow:0.0.2
pushing 0.0.2
*** push application/vnd.oci.image.manifest.v1+json sha256:36dca94e452f6bbd75c22c3c93590f527e0ecf0ce3f1c4fbe23a97b44aa1a6b1: manifest-sha256:36dca94e452f6bbd75c22c3c93590f527e0ecf0ce3f1c4fbe23a97b44aa1a6b1
```

### Sign

#### Generate a public and private key

```bash
❯ openssl genpkey -algorithm RSA -out ./private-key.pem
❯ openssl rsa -in ./private-key.pem -pubout > public-key.pem
```

#### Remote OCI Registry

```bash
❯ ocm sign componentversions \
    -s ww-ocm-sig \
    -K private-key.pem -k public-key.pem \
    --repo ghcr.io/sap/ocm-oci-flow \
    ghcr.io/sap/ocm-oci-flow:0.0.2
applying to version "ghcr.io/sap/ocm-oci-flow:0.0.2"...
  resource 0:  "name"="server": digest sha256:2f97e43aea52dede928ccd2e1bcd75325b157bd2d5e893e3cd179e6eb5de1488[ociArtifactDigest/v1]
successfully signed ghcr.io/sap/ocm-oci-flow:0.0.2 (digest sha256:6271f39d0d43897cb09a1ffed15b2d43adb11be6fce10367bedb3aee5e6afe88)
```

#### From Local Component

**Sign the component**:

```bash
❯ ocm sign componentversions -s ww-ocm-sig -K private-key.pem -k public-key.pem ./ocm-oci-flow
applying to version "ghcr.io/sap/ocm-oci-flow:0.0.2"...
  resource 0:  "name"="server": digest sha256:2f97e43aea52dede928ccd2e1bcd75325b157bd2d5e893e3cd179e6eb5de1488[ociArtifactDigest/v1]
successfully signed ghcr.io/sap/ocm-oci-flow:0.0.2 (digest sha256:6271f39d0d43897cb09a1ffed15b2d43adb11be6fce10367bedb3aee5e6afe88)
```

**Verify the signature:**

```bash
❯ ocm verify componentversion --signature ww-ocm-sig --public-key=public-key.pem ./ocm-oci-flow
applying to version "ghcr.io/sap/ocm-oci-flow:0.0.2"...
  resource 0:  "name"="server": digest sha256:2f97e43aea52dede928ccd2e1bcd75325b157bd2d5e893e3cd179e6eb5de1488[ociArtifactDigest/v1]
successfully verified ghcr.io/sap/ocm-oci-flow:0.0.2 (digest sha256:6271f39d0d43897cb09a1ffed15b2d43adb11be6fce10367bedb3aee5e6afe88)
```

#### Upload the signed component

```bash
❯ ocm  transfer componentarchive ./ocm-oci-flow ghcr.io/sap/ocm-oci-flow
transferring version "ghcr.io/sap/ocm-oci-flow:0.0.2"...
...adding component version...
*** push application/vnd.gardener.cloud.cnudie.component-descriptor.v2+yaml+tar sha256:39c8326c9084f6df25aca718807774f84c9580528a810de40863a36925155e7f: unknown-sha256:39c8326c9084f6df25aca718807774f84c9580528a810de40863a36925155e7f
*** push application/vnd.gardener.cloud.cnudie.component.config.v1+json sha256:a4451b90b165bdd19d271a521d707ce4a7bb91a6c49e707686fb5373913e00c2: unknown-sha256:a4451b90b165bdd19d271a521d707ce4a7bb91a6c49e707686fb5373913e00c2
*** push application/vnd.oci.image.manifest.v1+json sha256:a336ad4250ecc9fe04a89f5caeeb32d4ef6083ebecd41a6ca82f467b3df8c991: manifest-sha256:a336ad4250ecc9fe04a89f5caeeb32d4ef6083ebecd41a6ca82f467b3df8c991
pusher for ghcr.io/sap/ocm-oci-flow/component-descriptors/ghcr.io/sap/ocm-oci-flow:0.0.2
pushing 0.0.2
*** push application/vnd.oci.image.manifest.v1+json sha256:a336ad4250ecc9fe04a89f5caeeb32d4ef6083ebecd41a6ca82f467b3df8c991: manifest-sha256:a336ad4250ecc9fe04a89f5caeeb32d4ef6083ebecd41a6ca82f467b3df8c991
```

#### Verify

```bash
❯ ocm verify componentversion \
    --signature ww-ocm-sig \
    --public-key=public-key.pem \
    --repo OCIRepository::ghcr.io/sap/ocm-oci-flow \
    ghcr.io/sap/ocm-oci-flow:0.0.2
applying to version "ghcr.io/sap/ocm-oci-flow:0.0.2"...
  resource 0:  "name"="server": digest sha256:2f97e43aea52dede928ccd2e1bcd75325b157bd2d5e893e3cd179e6eb5de1488[ociArtifactDigest/v1]
successfully verified ghcr.io/sap/ocm-oci-flow:0.0.2 (digest sha256:6271f39d0d43897cb09a1ffed15b2d43adb11be6fce10367bedb3aee5e6afe88)
```
