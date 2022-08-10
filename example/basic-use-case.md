# Basic OCM flow

This is a proposition for a basic OCM flow.

1. Create resources
1. Create sources
1. Create a component archive
1. Download images ( optional )
1. Prepare for transfer
1. Create a transport archive
1. Sign it
1. Transfer the archive, verify, and extract

Advanced scenarios will include templating from the environment.

## Resources

```yaml
name: 'server'
version: '0.0.1'
type: 'ociImage'
relation: 'external'
access:
  type: 'ociRegistry'
  imageReference: 'docker.io/sap/ocm:example-0.0.1'
```

## Sources

No configured sources.

## Flow

### Create Skeleton

```bash
❯ ocm create componentarchive github.com/sap/ocm-basic-flow 0.0.1 sap ocm-basic-flow-ca
```

### Add resources

Resources yaml:

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
❯ ocm add resources ocm-basic-flow-ca resources.yaml
```

### Sign

Generate a public and private key:

```bash
❯ openssl genpkey -algorithm RSA -out ./private-key.pem
❯ openssl rsa -in ./private-key.pem -pubout > public-key.pem
```

Sign:

```bash
❯ ocm sign componentversions ocm-basic-flow-ca -s sap-ocm-sig -K private-key.pem -k public-key.pem
```

### Prepare for transport

Create a transport archive skeleton:

```bash
❯ ocm create transportarchive --type tgz ocm-basic-flow-ca-ta.tar.gz
```

Transport the componentarchive:

```bash
❯ ocm transfer componentarchive ocm-basic-flow-ca ./ocm-basic-flow-ca-ta.tar.gz
```

After that we have this directory structure:

```bash
❯ tree
.
├── README.md
├── component-descriptor.yaml
├── ocm-basic-flow-ca
│   ├── blobs
│   └── component-descriptor.yaml
├── ocm-basic-flow-ca-ta.tar.gz
│   ├── artefact-index.json
│   └── blobs
│       ├── sha256.45e384407fa87ef14c9880809ec9dd0e20a281b94a064671b9ea4c68e8dbdedf
│       ├── sha256.6b323881f7a2b2355cee564f70d5d9312878a86022911598247c0fbc85732991
│       └── sha256.80a6b7b967519091ea57a644af4a560cd918c68c029c19b9e2eabc0a661564e2
├── private-key.pem
├── public-key.pem
├── resources.yaml
└── sources.yaml


❯ tar ztf ocm-basic-flow-ca-ta.tar.gz | tree --fromfile .
.
├── artefact-index.json
└── blobs
    ├── sha256.45e384407fa87ef14c9880809ec9dd0e20a281b94a064671b9ea4c68e8dbdedf
    ├── sha256.6b323881f7a2b2355cee564f70d5d9312878a86022911598247c0fbc85732991
    └── sha256.80a6b7b967519091ea57a644af4a560cd918c68c029c19b9e2eabc0a661564e2
```

### Transfer

Once the artifact is copied, we can use OCM to verify its signature, and extract
it.

#### Verify

```bash
❯ tree
.
├── ocm-basic-flow-ca-ta.tar.gz
└── public-key.pem
```

We can verify the signing key with:

```bash
❯ ocm verify componentversion --signature sap-sig --public-key=public-key.pem ./ocm-basic-flow-ca-ta.tar.gz
applying to version "github.com/sap/ocm-basic-flow:0.0.1"...
  resource 0:  "name"="server": digest sha256:48f1d4bb271689c642a9590c8605ac8c70f0a1cae35a7dba809530f9399d6a5c[ociArtifactDigest/v1]
successfully verified github.com/sap/ocm-basic-flow:0.0.1 (digest sha256:afd21ac4d3a96b5c921143dd31abc1eb30e89e9919edffa11d21b336afdd218d)
```

#### Extract

```bash
❯ ocm transfer commontransportarchive ocm-basic-flow-ca-ta.tar.gz ./ocm-basic-flow-ca-new
transferring component "github.com/sap/ocm-basic-flow"...
  transferring version "github.com/sap/ocm-basic-flow:0.0.1"...
    version "github.com/sap/ocm-basic-flow:0.0.1" already present -> skip transport

❯ tree ./ocm-basic-flow-ca-new
./ocm-basic-flow-ca-new
├── artefact-index.json
└── blobs
    ├── sha256.45e384407fa87ef14c9880809ec9dd0e20a281b94a064671b9ea4c68e8dbdedf
    ├── sha256.6b323881f7a2b2355cee564f70d5d9312878a86022911598247c0fbc85732991
    └── sha256.80a6b7b967519091ea57a644af4a560cd918c68c029c19b9e2eabc0a661564e2
```
