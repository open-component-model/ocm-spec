# Glossary

[A](#a) &nbsp; B &nbsp; [C](#c) &nbsp; [D](#d) &nbsp; [E](#e) &nbsp; F &nbsp; G &nbsp; H &nbsp; [I](#i) &nbsp; J &nbsp; K &nbsp; [L](#l) &nbsp; [M](#m) &nbsp; [N](#n) &nbsp; [O](#o) &nbsp; P &nbsp; Q &nbsp; [R](#r) &nbsp; [S](#s) &nbsp; [T](#t) &nbsp; U &nbsp; V &nbsp; W &nbsp; X &nbsp; Y &nbsp; Z

## A


#### [Access Method](specification/elements/README.md#artifact-access)<a id="accmeth"/>
a dedicated procedure how to access the content of an [artifact](#artifact) 
described by a [component version](#compvers). It is formally represented by an
[access method type](#acctype).

#### [Access Method Operations](specification/operations/README.md#access-method-operations)<a id="accmethops"/>
the operations an implementation of an [access method](#accmeth) has to support.

#### [Access Method Type](specification/formats/types.md#access-method-types)<a id="acctype"/>
the type of an [access specification](#accspec) determining the formal procedure
to use to access the blob content of an [artifact](#artifact).

#### [Access Specification](specification/elements/README.md#artifact-access)<a id="accspec"/>
the specification of the technical access path to the physical blob content of
an [artifact](#artifact) described by a [component version](#compvers).

#### [Aggregation](specification/elements/README.md#aggregation)<a id="aggregation"/>
the ability of the Open Component Model to compose [component versions](#compvers)
based on other component versions.

#### [Artifact](specification/elements/README.md#artifacts)<a id="artifact"/>
some blob content described  by a [component version](#component-version).

#### [Artifact Digest](specification/elements/README.md#digest-info)<a id="artdigest"/>
the (logical) digest of an [artifact](#artifact) described by a [component version](#component-version).

#### [Artifact Reference](specification/elements/README.md#artifact-references)<a id="artref"/>
a relative or absolute reference to an [artifact](#artifact) described by a 
[component version](#compvers).

#### [Artifact Type](specification/formats/types.md#artifact-types)<a id="arttype"/>
the formal type of an [artifact](#artifact) described by a
[component version](#compvers). The type implies the logical interpretation of
the artifact blob.

## C

#### [Component](specification/elements/README.md#components)<a id="component"/>
an abstract entity describing a dedicated usage context or
meaning for a provided piece of software.

#### [Component Descriptor](specification/elements/README.md#component-descriptor)<a id="compdesc"/>
the formal description of a [component version](#compvers).


#### [Component Identity](specification/elements/README.md#components)<a id="compid"/>
the globally unique identity of a [component](#component).

#### [Component Repository](specification/elements/README.md#repositories)<a id="comprep"/>
an entity able to store and retrieve [component versions](#compvers). See also [Normalization](#norm)

#### [Component Version](specification/elements/README.md#component-versions)<a id="compvers"/>
a dedicated version of a [component](#component) described by the Open Component Model
described by a [component descriptor](#compdesc) and retrievable from
a [component repository](#comprep).

#### [Component Version Digest](specification/elements/README.md#signatures)<a id="compdigest"/>
the digest of a [component version](#compvers).

#### [Component Version Identity](specification/elements/README.md#component-versions)<a id="compversid"/>
the globally unique identity of a [component version](#compvers).

#### [Component Version Reference](specification/elements/README.md#aggregation)<a id="compref"/>
a reference to a [component versions](#compvers) in a component version to
describe an aggregation relationship..

## D

#### [Denotation](specification/denotations/README.md)<a id="denotation"/>
the possibility to describe identities of [components](#component), 
[component versions](#compvers),
[repositories](#comprep) in form of a sole string representation.


#### Digest <a id="digest"/>
see [artifact digest](#artdigest) or [component version digest](#compdigest).

## E

#### [Element Identity](specification/elements/README.md#identities)<a id="elemid"/>
the local identity of an element described by a [component version](#compvers).
There are three classes of identities: [resource](#resource) identities, [source](#source) identities and 
[reference](#compref) identities.

#### [Extension Point](specification/extensionpoints/README.md)<a id="ext"/>
parts of the [OCM](#ocm) specification, which may be extended by arbitrary 
variations. The specification just defines the meaning, syntax and or functional
behaviour of such elements.

## I

#### Identity<a id="identity"/>
see [element identity](#elemid), [component identity](#compid), [component version identity](#compversid)

## L

#### [Labels](specification/elements/README.md#labels)<a id="labels"/>
arbitrary typed information snippets attached to [component versions](#compvers),
[artifacts](#artifacts) and [references](#compref).

## M

#### [Mapping](specification/operations/README.md)<a id="mapping"/>
the mapping of the [elements](specification/elements/README.md) of the
[Open Component Model)](#ocm) onto a dedicated storage backend technology
described by a [repository type](#repotype).

## N

#### [Normalization](specification/formats/normalization_format.md)<a id="norm"/>
the transformation of a technical blob depending on its type into a
serialization-agnostic format, which can be used to calculate an immutable
digest for signing purposes along a transportation path.

## O

#### [Open Component Model](../README.md)<a id="ocm"/>
a technology- and location-agnostic description model for software delivery
artifacts with attached meta-data, providing environment-specific access
path to described [artifacts](#artifact).

#### Operations <a id="ops"/>
see [repository operations](#repops), [access methods](#accmeth) and
[access method operations](#accmethops).

## R

#### Reference <a id="ref"/>
a reference to an element of the component model, see [artifact reference](#artref)
or [component version reference](#compref)

#### [Repository Operations](specification/operations/README.md#repository-operations)<a id="repops"/>
abstract operations that have to be provided by a language binding for a
[mapping](#mapping) of the [Open Component Model](#ocm) to a dedicated storage
technology.

#### [Repository Type](specification/formats/types.md#repository-types)<a id="repoptype"/>
the type of a [mapping](#mapping) of the [Open Component Model](#ocm) specification
to a dedicated storage technology.

#### [Resource](specification/elements/README.md#resources)<a id="resource"/>
a delivery artifact described by a [component version](#compvers). 

## S

#### [Signature](specification/elements/README.md#signatures)<a id="signature"/>
a [component version](#compvers) may be signed by an authority, the signature as
result of such a signing process is stored along with the component version.

#### [Source](specification/elements/README.md#sources)<a id="source"/>
an artifact described by a [component version](#compvers) containing sources
used to generate one or more of the described [resources](#resource).

#### Specification Format
a format definition for the specification of attributes for
dedicated variants of some [extension points](#ext). See [access methods](#accmeth),
[repository types](#repotype), and [labels](#label).

## T

#### [Type](specification/formats/types.md)<a id="type"/>
a formal representation of the kind of an [extension point](#ext) of the
[Open Component Model](#ocm). See [repository type](#repotype),
[access method type](#acctype), [artifact type](#arttype) [label](#label).