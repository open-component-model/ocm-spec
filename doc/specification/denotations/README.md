# 2.5 Denotation Schemes

A dedicated language binding typically provides structured elements
to describe the specification of an OCM [repository](../elements/README.md#repositories) or
a [component version](../elements/README.md#component-versions).

Additionally, tools and command line clients may support an appropriate
textual notation to denote elements to deal with.

This part of the specification describes a denotation scheme for
repositories and component versions that SHOULD always be supported.

## Repositories

Regardless of their mapping specification any OCM repository can be
described by a single string representation of the [repository 
specification](../formats/formats.md#repository-specifications).

It is composed by the [repository type](../formats/types.md#repository-types)
and the specificatio part. Here, for some attributes, there is a special
handling an repository type can make use of (for example a simplified 
votatio just using one prominent attribute). In general
all specifications with all possible non-binding-specific attributes can be 
expressed by using a JSON notation.

<center>
    <pre>[+][&lt;type>::][&lt;scheme>://]&lt;domain>[:&lt;port>][/&lt;repository prefix>]</pre>
        or
    <pre>[+][&lt;type>::]&lt;json repo spec></pre>
        or
    <pre>[+][&lt;type>::][./]&lt;file path></pre>
</center>

The optional leading `+` indicates that the repository might be created if 
it does not exist. This is basically useful, when using filesystem-based
representations.

## Component Versions

Component versions have an location-agnostic identity
and they can be located in a dedicated  OCM repository.
Both kinds of identities can be expresses by sole string representation
suitable for the use of command line tools, also.

### Plain Component Versions

The identity of component versions can be described as string representation
by appending the version name to the component identity, separated by 
a colon (`:`):

<center>
    <pre>&lt;component id>:&lt;version name></pre>
</center>

### Component Versions in a Repository

To describe a located component or component version in a dedicated repository
the component/componenr version notation is appended to the repository notation,
sseparated by a double-slash (`//`):

<center>
    <pre>[+][&lt;type>::][./][&lt;file path>//&lt;component id>[:&lt;version>]</pre>
        or
    <pre>[+][&lt;type>::]&lt;domain>[:&lt;port>][/&lt;repository prefix>]//&lt;component id>[:&lt;version]</pre>
        or
    <pre>[&lt;type>::][&lt;json repo spec>//]&lt;component id>[:&lt;version>]</pre>

</center>
