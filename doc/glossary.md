# Glossary

[A](#a) &nbsp; B &nbsp; [C](#c) &nbsp; [D](#d) &nbsp; [E](#e) &nbsp; F &nbsp; G &nbsp; H &nbsp; [I](#i) &nbsp; J &nbsp; K &nbsp; [L](#l) &nbsp; M &nbsp; [N](#n) &nbsp; [O](#o) &nbsp; P &nbsp; Q &nbsp; [R](#r) &nbsp; [S](#s) &nbsp; T &nbsp; U &nbsp; V &nbsp; W &nbsp; X &nbsp; Y &nbsp; Z

## A

#### [Artefact](specification/layer1/README.md#artefacts)<a id="artefact"/>
some blob content described  by a [component version](#component-version).

#### [Artefact Digest](specification/layer1/README.md#digest-info)<a id="artdigest"/>
the (logical) digest of an [artefact](#artefact) described by a [component version](#component-version).

#### [Artefact Reference](specification/layer1/README.md#artefact-references)<a id="artspec"/>
a relative or absolute reference to an [artefact](#artefact) described by a 
[Component Version](#compvers).

#### [Access Specification](specification/layer1/README.md#artefact-access)<a id="accessspec"/>
the specification for the technical access path to the physical content of an
[artefact](#artefact) described as part of a [Component Version](#compvers).

#### [Aggregation](specification/layer1/README.md#aggregation)<a id="aggregation"/>
the ability of the Open Component Model to compose [component versions](#compvers)
based on other component versions.

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

#### [Digest]<a id="digest"/>
see [artefact digest](#cartdigest) or [component version digest](#compdigest).

## E

#### [Element Identity](specification/layer1/README.md#identities)<a id="elemid"/>
the local identity of an element described by a [component version](#compvers).
There are three classes of identities: [resource](#resource) identities, [source](#source) identities and 
[reference](#compref) identities.

## I

#### Identity<a id="identity"/>
see [element identity](#elemid), [component identity](#compid), [component version identity](#compversid)

## L

#### [Labels](specification/layer1/README.md#labels)<a id="labels"/>
arbitrary typed information snippets attached to [component versions](#compvers),
[artefacts](#artefacts) and [references](#compref).

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

## R

#### Reference <a id="ref"/>
a reference to an element of the component model, see [artefact reference](#artref)
or [component version reference](#compref)

#### [Resource](specification/layer1/README.md#resources)<a id="resource"/>
a delivery artefact described by a [component version](#compvers). 

## S

#### [Signature](specification/layer1/README.md#signatures)<a id="signature"/>
a [component version](#compvers) may be signed by an authority, the signature as
result of such a signing process is stored along with the component version.

#### [Source](specification/layer1/README.md#sources)<a id="source"/>
an artefact described by a [component version](#compvers) containing sources
used to generate one or more of the described [resources](#resource).