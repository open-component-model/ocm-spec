# Glossary

[A](#a) &nbsp; B &nbsp; [C](#c) &nbsp; [D](#d) &nbsp; [E](#e) &nbsp; F &nbsp; [G](#g) &nbsp; [H](#h) &nbsp; [I](#i) &nbsp; J &nbsp; K &nbsp; [L](#l) &nbsp; [M](#m) &nbsp; [N](#n) &nbsp; [O](#o) &nbsp; [P](#p) &nbsp; Q &nbsp; [R](#r) &nbsp; [S](#s) &nbsp; [T](#t) &nbsp; U &nbsp; V &nbsp; W &nbsp; X &nbsp; Y &nbsp; Z

## A


#### [Access Method](01-model/02-elements.md#access-specification)<a id="accmeth"/>
defines how to access the content of an [artifact](#artifact)

#### [Access Method Operations](03-operations/01-operations.md#access-method-operations)<a id="accmethops"/>
the operations an implementation of an [access method](#accmeth) has to support.

#### [Access Method Type](01-model/02-elements.md/#access-types)<a id="acctype"/>
the type of an [access specification](#accspec) determining the formal procedure
to use to access the blob content of an [artifact](#artifact).

#### [Access Specification](01-model/02-elements.md#access-specification)<a id="accspec"/>
the specification of the technical access path to the physical blob content of
an [artifact](#artifact.

#### [Aggregation](02-processing/01-references.md)<a id="aggregation"/>
the ability of the Open Component Model to compose component versions
based on other component versions.

#### [Artifact](01-model/02-elements.md#artifacts)<a id="artifact"/>
some blob content described  by a [component version](#component-version).

#### [Artifact Digest](02-processing/04-digest.md#artifact-digest)<a id="artdigest"/>
the (logical) digest of an [artifact](#artifact).

#### [Artifact Normalization](02-processing/04-digest.md#normalization)<a id="artnorm"/>
the transformation of a technical blob content of an [artifact](#artifact) depending
on its type into a serialization-agnostic digest.

#### [Artifact Reference](02-processing/01-references#referencing)<a id="artref"/>
a relative or absolute reference to an [artifact](#artifact) described by a
[component version](#compvers).

#### [Artifact Type](01-model/02-elements.md#artifact-types)<a id="arttype"/>
the formal type of an [artifact](#artifact) described by a
[component version](#compvers). The type implies the logical interpretation of
the artifact blob.

## C

#### [Component](01-model/01-model.md#components-and-component-versions)<a id="component"/>
an abstract entity describing a dedicated usage context or
meaning for a provided piece of software.

#### [Component Descriptor](01-model/01-model.md#components-and-component-versions)<a id="compdesc"/>
the formal description of a [component version](#compvers).

#### [Component Descriptor Normalization](02-processing/04-digest.md#normalization)<a id="compdescnorm"/>
the mapping of the elements of a [component descriptor](#compdesc) into an
immutable format containg only signature relevant information used to calculate a digest.

#### [Component Identity](01-model/03-elements-sub.md#identifiers)<a id="compid"/>
the globally unique identity of a [component](#component).

#### [Component Repository](01-model/01-model.md#component-repositories)<a id="comprep"/>
an entity able to store and retrieve [component versions](#compvers). See also [Normalization](#norm)

#### [Component Version](01-model/01-model.md#components-and-component-versions)<a id="compvers"/>
a dedicated version of a [component](#component) described by the Open Component Model
described by a [component descriptor](#compdesc) and retrievable from
a [component repository](#comprep).

#### [Component Version Digest](02-processing/04-digest.md#artifact-digest)<a id="compdigest"/>
the digest of a [component version](#compvers).

#### [Component Version Identity](01-model/01-model.md#components-and-component-versions)<a id="compversid"/>
the globally unique identity of a [component version](#compvers).

#### [Component Version Reference](02-processing/01-references.md#referencing)<a id="compref"/>
a reference to a [component versions](#compvers) in a component version to
describe an aggregation relationship..

## D

#### Digest <a id="digest"/>
see [artifact digest](#artdigest) or [component version digest](#compdigest).

## E

#### [Extension Point](./03-persistence/01-operations.md#abstract-operations-defined-by-the-open-component-model)<a id="ext"/>
parts of the [OCM](#ocm) specification, which may be extended by arbitrary
variations. The specification just defines the meaning, syntax and or functional
behaviour of such elements.

#### [Extra Identity](./01-model/03-elements-sub.md#identifiers)<a id="extraid"/>
additional parts of the identity of an [element](#elemid) of a [component version](#compvers).

## G

#### [`gitHub`](./04-extensions/02-access-types/github.md)<a id="github"/>
[access method](#accmeth) used to access Git commits in a GitHub repository.

## H

#### [`helm`](./04-extensions/02-access-types/helm.md)<a id="helm"/>
[access method](#accmeth) used to access [Helm Charts](#helmchart) in a Helm repository.

#### Helm Chart<a id="helmchart"/>
A set of files describing the deplyoment of a Kubernetes application using
the [Helm](https://helm.sh/) deployment mechanism.

see [element identity](#elemid), [component identity](#compid), [component version identity](#compversid)

## I

#### Identity<a id="identity"/>
see [element identity](#elemid), [component identity](#compid), [component version identity](#compversid)

## L

#### [Labels](01-model/03-elements-sub.md#labels)<a id="labels"/>
arbitrary typed information snippets attached to [component versions](#compvers),
[artifacts](#artifacts) and [references](#compref).

#### [`localBlob`](./04-extensions/02-access-types/localblob.md)<a id="localblob"/>
[access method](#accmeth) used to access blobs stored along with a component version.

#### [Localization](./05-guidelines/02-contract.md#example-helm-deployment)<a id="localization"/>
the process of adapting content delivered as [artifacts](#artifacts) in a [component versions](#compvers) to a local repository landscape in a target environment.

## M

#### [Mapping](./03-persistence/02-mappings.md#mappings-for-ocm-persistence)<a id="mapping"/>
the mapping of the [elements](01-model/02-elements.md) of the Open Component Model onto a storage technology described by a [repository type](#repotype).

#### [Model-Tool Contract](./05-guidelines/02-contract.md)<a id="contract"/>
The agreement between the Open Component Model and tools working with content
provided by [component versions](#compvers), which regulates the cooperation
between both.

## N

#### [Normalization](02-processing/04-digest.md#normalization)<a id="norm"/>
the transformation which can be used to calculate an immutable digest for signing purposes along a transportation path. There are two normalization procedures, [artifact normalization](#artnorm) and
[component descriptor normalization](#compdescnorm).

#### [`npm`](./04-extensions/02-access-types/npm.md)<a id="npm"/>
[access method](#accmeth) used to access NodeJS packages in an NPM repository.

## O

#### [`ociArtifact`](./04-extensions/02-access-types/ociartifact.md)<a id="ociartifact"/>
[access method](#accmeth) used to access OCI artifacts stored in an OCI registry.

#### [`ociBlob`](./04-extensions/02-access-types/ociblob.md)<a id="ociblob"/>
[access method](#accmeth) used to access blobs stored in an OCI registry.

#### [Open Component Model](../README.md)<a id="ocm"/>
a technology- and location-agnostic description model for software delivery
artifacts with attached meta-data, providing environment-specific access
path to described [artifacts](#artifact).

#### Operations <a id="ops"/>
see [repository operations](#repops), [access methods](#accmeth) and
[access method operations](#accmethops).

## P

### [Platform Convention](01-model/06-conventions.md#operating-system-and-cpu-architecture)) <a id="osarch"/>
Using extra identities to express the assignment of an [artifact](#artifact) to a dedicated
execution platform.

## R

#### Reference <a id="ref"/>
a reference to an element of the component model, see [artifact reference](#artref)
or [component version reference](#compref)

#### [Relative Resource Refererences](02-processing/01-references.md#relative-artifact-references)<a id="relrefs"/>
a reference to an [artifact](#artifact) described by a [component version](#compvers) relative to
a given component version exploiting the [aggregation feature](#aggregation) of the Open Component
Model. It is part of the [model-tool contract](#contract).

#### [Repository Operations](03-persistence/0-operations.md)<a id="repops"/>
abstract operations that have to be provided by a language binding for a
[mapping](#mapping) of the [Open Component Model](#ocm) to a dedicated storage
technology.

#### [Repository Type](./04-persistence/01-mappings.md#mappings-for-ocm-persistence)<a id="repoptype"/>
the type of a [mapping](#mapping) of the [Open Component Model](#ocm) specification
to a storage technology.

#### [Resource](01-model/02-elements-toplevel.md#resources)<a id="resource"/>
a delivery artifact described by a [component version](#compvers).

## S

#### [Signature](02-processing/03-signing.md#signing)<a id="signature"/>
a [component version](#compvers) may be signed by an authority, the signature as
result of such a signing process is stored along with the component version.

#### [Source](01-model/02-elements-toplevel.md#sources)<a id="source"/>
an artifact described by a [component version](#compvers) containing sources
used to generate one or more of the described [resources](#resource).

#### Specification Format
a format definition for the specification of attributes for
dedicated variants of some [extension points](#ext). See [access methods](#accmeth),
[repository types](#repotype), and [labels](#label).

#### [`s3`](./04-extensions/02-access-types/s3.md)<a id="s3"/>
[access method](#accmeth) used to access blobs in an S3 repository, a [mapping](#mapping) to store content in an S3 repository

## T

#### [Transport](02-guidelines/01-transport.md)<a id="transport"/>
the operation on [component versions](#compvers) transferring content from
one OCM repository into another one.

#### Type<a id="type"/>
a formal representation of the kind of an [extension point](#ext) of the
[Open Component Model](#ocm). See [repository type](#repotype),
[access method type](#acctype), [artifact type](#arttype) [label](#label).
