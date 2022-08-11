# Transfer Component Behind Fenced Network

1. Create resources
1. Create sources
1. Create a component archive
1. Prepare for transfer
1. Download resources
1. Sign it
1. Create a transport archive
1. Transfer the archive, verify

Advanced scenarios will include templating from the environment.

## Resources

```yaml
name: server
version: 0.0.1
type: ociImage
relation: external
access:
  type: ociRegistry
  imageReference: ghcr.io/yitsushi/hello-world:1.0.7
```

## Sources

No configured sources.

## Flow

### Create Skeleton

```bash
❯ ocm create componentarchive ghcr.io/sap/ocm-ta-flow 0.0.1 sap ocm-ta-flow-ca
```

### Add resources

Resources yaml:

```yaml
name: server
version: 0.0.1
type: ociImage
relation: external
access:
  type: ociRegistry
  imageReference: ghcr.io/yitsushi/hello-world:1.0.7
```

```bash
❯ ocm add resources ocm-ta-flow-ca resources.yaml
processing resources.yaml...
  processing document 1...
    processing index 0
found 1 resources
```

### Sign

Generate a public and private key:

```bash
❯ openssl genpkey -algorithm RSA -out ./private-key.pem
❯ openssl rsa -in ./private-key.pem -pubout > public-key.pem
```

Sign:

```bash
❯ ocm sign componentversions ocm-ta-flow-ca \
    -s ww-ocm-sig -K private-key.pem -k public-key.pem
applying to version "ghcr.io/sap/ocm-ta-flow:0.0.1"...
  resource 0:  "name"="server": digest sha256:2f97e43aea52dede928ccd2e1bcd75325b157bd2d5e893e3cd179e6eb5de1488[ociArtifactDigest/v1]
successfully signed ghcr.io/sap/ocm-ta-flow:0.0.1 (digest sha256:a990e44fc567e8668796a1ef343922ce88febb1fc6742518cd0bd12b89faa316)
```

### Prepare for transport

Create a transport archive skeleton:

```bash
❯ ocm create transportarchive --type tgz ocm-ta-flow-ca-ta.tar.gz
```

Transport the componentarchive:

```bash
❯ ocm transfer componentarchive ocm-ta-flow-ca ./ocm-ta-flow-ca-ta.tar.gz
```

After that we have this directory structure:

```bash
❯ tree
.
├── ocm-ta-flow-ca
│   ├── blobs
│   └── component-descriptor.yaml
├── ocm-ta-flow-ca-ta.tar.gz
├── private-key.pem
├── public-key.pem
└── resources.yaml


❯ tar ztf ocm-ta-flow-ca-ta.tar.gz | tree --fromfile .
.
├── artefact-index.json
└── blobs
    ├── sha256.46f15984e3f2c7d779199e2e649d24d9ad8357404a6195ca73733097c622b5eb
    ├── sha256.f338df813e8b19652565a4a31407fae7a5a52fb162a6e867c2caab53d77c02cb
    └── sha256.fe7e84c6587a1a22e05473fa2e215a0e20d21ecc6307106a6d7c5dac1934d048
```

### Download Resources

If only one resource is defined, we can use this format:
```bash
❯ ocm download resources ./ocm-ta-flow-ca -O hello-world.tar.gz
```

If more then one, or nested, then the `-O` flag has a different behavior and
will create a directory:

```bash
❯ ocm download resources ./ocm-ta-flow-ca -O ocm-ta-flow-ca-resources
```

We can verify the content:

```bash
❯ tar ztf hello-world.tar.gz
artefact-descriptor.json
blobs
blobs/sha256.2f97e43aea52dede928ccd2e1bcd75325b157bd2d5e893e3cd179e6eb5de1488
blobs/sha256.5305f40ab0c9c75856e5ffe193f47253e53696305f0da5ec44dacadec342328d
blobs/sha256.92360c1eaf0032a860dddb1e3cdc16b27bdfec509c23de434dbe53d3d35bed9d
blobs/sha256.df9b9388f04ad6279a7410b85cedfdcb2208c0a003da7ab5613af71079148139
```

#### Add artefact to the component transfer archive

```bash
❯ ocm oci artefacts transfer ./hello-world.tar.gz ./ocm-ta-flow-ca-ta.tar.gz
copying :1.0.7 to :1.0.7...
copied 1 from 1 artefact(s)
```

### Transfer

Once the artifact is copied, we can use OCM to verify its signature, and extract
it.

#### Verify

```bash
❯ tree
.
├── ocm-ta-flow-ca-ta.tar.gz
└── public-key.pem
```

We can verify the signing key with:

```bash
❯ ocm verify componentversion --signature ww-ocm-sig --public-key=public-key.pem  ./ocm-ta-flow-ca-ta.tar.gz
applying to version "ghcr.io/sap/ocm-ta-flow:0.0.1"...
  resource 0:  "name"="server": digest sha256:2f97e43aea52dede928ccd2e1bcd75325b157bd2d5e893e3cd179e6eb5de1488[ociArtifactDigest/v1]
successfully verified ghcr.io/sap/ocm-ta-flow:0.0.1 (digest sha256:a990e44fc567e8668796a1ef343922ce88febb1fc6742518cd0bd12b89faa316)
```
