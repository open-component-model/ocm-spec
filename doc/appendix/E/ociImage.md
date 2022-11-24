# `ociImage` &#8212; OCI Image or Image Index

An OCI artifact that contains an OCI container image.
The content is intended to be used as container image.

A general [ociArtifact](ociArtifact.md) may describe
any kind of content, depending on the media type of
its config blob (see also [`helmChart`](helmChart.md)).

`ociImage` is a dedicated variant for the container
image media types.

## Format Variants

As special case for a general `ociArtifact` is uses
the [`ociArtifact` blob format](ociArtifact.md#format-variants).

## Special Support

As special case for a general `ociArtifact` is uses
the [`ociArtifact` special support](ociArtifact.md#special-support).
