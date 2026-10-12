# Git — Git Commit hosted in a Git Repository

## Synopsis

```text
type: Git[/VERSION]
[ATTRIBUTES]
```

Legacy type name `git` is supported as a backward-compatible alias.

## Description

Access to a commit in a Git repository.

## Supported Media Types

- `application/x-tgz`:   The artifact content is provided as g-zipped tar archive

## Specification Version

The following versions are supported

### v1

Attributes:

- **`repository`** *string*

  Repository URL: an `http(s)://`, `ssh://` or `git://` URL, the form `user@host:path`,
  or a local repository as `file:///path` or plain path.

- **`ref`** (optional) *string*

  Branch, tag or full ref name used to get the commit from. A bare name resolves to a
  branch first and then to a tag. Either `ref` or `commit` must be set.

- **`commit`** (optional) *string*

  The full 40-character sha/id of the git commit. It takes precedence over `ref`.
