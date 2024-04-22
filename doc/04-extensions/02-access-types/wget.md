# wget — Blob hosted on an HTTP server

## Synopsis

```text
type: wget[/VERSION]
[ATTRIBUTES]
```

## Description

Access to a blob stored on an HTTP server.

## Supported Media Types

The provided media type is taken from the specification attribute `mediaType`.

## Specification Version

The following versions are supported

### v1

Attributes:

- **`url`** *string*

  The url describes from which http server endpoint the resource is downloaded

- **`mediaType`** (optional) *string*

  The media type of the blob used to store the resource. It may add
  format information like `+tar` or `+gzip`.

- **`header`** (optional) *map\[string\][]string*

  The header describes the http headers to be set in the http request to the server.

- **`verb`** (optional) *string*

  The verb describes the http verb (also known as http request method) for the http
  request.

- **`body`** (optional) *[]byte*

  The body describes the http body to be included in the request.

- **`noredirect`** (optional) *bool*

  The noredirect describes whether http redirects should be disabled.
