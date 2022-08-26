# `gitHub` and `github`  &#8212; Accessing Git Commits on GitHub


### Synopsis

```
type: gitHub/v1
```

Provided blobs use the following media type for: `application/x-tgz`

The artefact content is provided as gnu-zipped tar archive

### Description

This method implements the access of the content of a git commit stored in a
GitHub repository.

### Specification Versions

Supported specification version is `v1`

#### Version `v1`

The type specific specification fields are:

- **`repoUrl`**  *string*

  Repository URL with or without scheme.

- **`ref`** (optional) *string*

  Original ref used to get the commit from

- **`commit`** *string*

  The sha/id of the git commit


