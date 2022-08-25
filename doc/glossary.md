# Glossary

[A](#a) &nbsp; B &nbsp; [C](#c) &nbsp; [D](#d) &nbsp; [E](#e) &nbsp; F &nbsp; G &nbsp; H &nbsp; [I](#i) &nbsp; J &nbsp; K &nbsp; [L](#l) &nbsp; [M](#m) &nbsp; [N](#n) &nbsp; [O](#o) &nbsp; P &nbsp; Q &nbsp; [R](#r) &nbsp; [S](#s) &nbsp; [T](#t) &nbsp; U &nbsp; V &nbsp; W &nbsp; X &nbsp; Y &nbsp; Z

## A


#### [Access Method](specification/layer1/README.md#artefact-access)<a id="accmeth"/>
a dedicated procedure how to access the content of an [artefact](#artefact) 
described by a [component version](#compvers). It is formally represented by an
[access method type](#acctype).

#### [Access Method Operations](specification/layer2/README.md#access-method-operations)<a id="accmethops"/>
the operations an implementation of an [access method](#accmeth) has to support.

#### [Access Method Type](specification/formats/types.md#access-method-types)<a id="acctype"/>
the type of an [access specification](#accspec) determining the formal procedure
to use to access the blob content of an [artefact](#artefact).

#### [Access Specification](specification/layer1/README.md#artefact-access)<a id="accspec"/>
the specification of the technical access path to the physical blob content of
an [artefact](#artefact) described by a [component version](#compvers).

#### [Aggregation](specification/layer1/README.md#aggregation)<a id="aggregation"/>
the ability of the Open Component Model to compose [component versions](#compvers)
based on other component versions.

#### [Artefact](specification/layer1/README.md#artefacts)<a id="artefact"/>
some blob content described  by a [component version](#component-version).

#### [Artefact Digest](specification/layer1/README.md#digest-info)<a id="artdigest"/>
the (logical) digest of an [artefact](#artefact) described by a [component version](#component-version).

#### [Artefact Reference](specification/layer1/README.md#artefact-references)<a id="artref"/>
a relative or absolute reference to an [artefact](#artefact) described by a 
[component version](#compvers).

#### [Artefact Type](specification/formats/types.md#artefact-types)<a id="arttype"/>
the formal type of an [artefact](#artefact) described by a
[component version](#compvers). The type implies the logical interpretation of
the artefact blob.

## C

#### [Component](specification/layer1/README.md#components)<a id="component"/>
an abstract entity describing a dedicated usage context or
meaning for a provided piece of software.

#### [Component Descriptor](specification/layer1/README.md#component-descriptor)<a id="compdesc"/>
the formal description of a [component version](#compvers).


#### [Component Identity](specification/layer1/README.md#components)<a id="compid"/>
the globally unique identity of a [component](#component).

#### [Component Repository](specification/layer1/README.md#repositories)<a id="comprep"/>
an entity able to store and retrieve [component versions](#compvers). See also [Normalization](#norm)

#### [Component Version](specification/layer1/README.md#component-versions)<a id="compvers"/>
a dedicated version of a [component](#component) described by the Open Component Model
described by a [component descriptor](#compdesc) and retrievable from
a [component repository](#comprep).

#### [Component Version Digest](specification/layer1/README.md#signatures)<a id="compdigest"/>
the digest of a [component version](#compvers).

#### [Component Version Identity](specification/layer1/README.md#component-versions)<a id="compversid"/>
the globally unique identity of a [component version](#compvers).

#### [Component Version Reference](specification/layer1/README.md#aggregation)<a id="compref"/>
a reference to a [component versions](#compvers) in a component version to
describe an aggregation relationship..

## D

#### Digest <a id="digest"/>
see [artefact digest](#artdigest) or [component version digest](#compdigest).

## E

#### [Element Identity](specification/layer1/README.md#identities)<a id="elemid"/>
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

#### [Labels](specification/layer1/README.md#labels)<a id="labels"/>
arbitrary typed information snippets attached to [component versions](#compvers),
[artefacts](#artefacts) and [references](#compref).

## M

#### [Mapping](specification/layer2/README.md)<a id="mapping"/>
the mapping of the [elements](specification/layer1/README.md) of the
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
artefacts with attached meta-data, providing environment-specific access
path to described [artefacts](#artefact).

#### Operations <a id="ops"/>
see [repository operations](#repops), [access methods](#accmeth) and
[access method operations](#accmethops).

## R

#### Reference <a id="ref"/>
a reference to an element of the component model, see [artefact reference](#artref)
or [component version reference](#compref)

#### [Repository Operations](specification/layer2/README.md#repository-operations)<a id="repops"/>
abstract operations that have to be provided by a language binding for a
[mapping](#mapping) of the [Open Component Model](#ocm) to a dedicated storage
technology.

#### [Repository Type](specification/formats/types.md#repository-types)<a id="repoptype"/>
the type of a [mapping](#mapping) of the [Open Component Model](#ocm) specification
to a dedicated storage technology.

#### [Resource](specification/layer1/README.md#resources)<a id="resource"/>
a delivery artefact described by a [component version](#compvers). 

## S

#### [Signature](specification/layer1/README.md#signatures)<a id="signature"/>
a [component version](#compvers) may be signed by an authority, the signature as
result of such a signing process is stored along with the component version.

#### [Source](specification/layer1/README.md#sources)<a id="source"/>
an artefact described by a [component version](#compvers) containing sources
used to generate one or more of the described [resources](#resource).

## T

#### [Type](specification/formats/types.md)<a id="type"/>
a formal representation of the kind of an [extension point](#ext) of the
[Open Component Model](#ocm). See [repository type](#repotype),
[access method type](#acctype), [artefact type](#arttype) [label](#label).