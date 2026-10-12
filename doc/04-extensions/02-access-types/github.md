# GitHub — Git Commit hosted by GitHub

## Synopsis

```text
type: GitHub[/VERSION]
```

Legacy type names `gitHub` and `github` are supported as backward-compatible aliases.

This access type is deprecated, use [`Git`](git.md) instead.

## Description

Access to a commit in a Git repository.

## Supported Media Types

- `application/x-tgz`:   The artifact content is provided as g-zipped tar archive

## Specification Version

The following versions are supported

### v1

Attributes:

- **`repoUrl`**  *string*

  Repository URL with or without scheme.

- **`ref`** (optional) *string*

  Original ref used to get the commit from

- **`commit`** *string*

  The sha/id of the git commit
