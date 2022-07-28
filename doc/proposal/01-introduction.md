# Introduction

The definition, structure and management of software in larger enterprises often builds upon tools and processes, which
largely originate from former on-premise thinking and monolithic architectures. Development teams responsible for
solutions or services have built specific, often point-2-point integrations with CI/CD systems, compliance tools,
reporting dashboards or delivery processes in the past. Larger development teams might have even built their own
toolsets specifically for their products, including those needed for compliance handling and delivery automation.
These concepts, process integrations and resulting tools are often still in use today, even though everyone knows:
They don't fit into today's cloud world.

The result is a fragmented set of homegrown specific tools across products, solutions and services, affecting an 
enterprises' ability to deliver software consistently and compliant to its own or customer operated target environments.
These specific, overly complex and thus hard to understand CI/CD pipelines, and the inability to instantly
provide a holistic aggregated view of currently running technical artifacts for each and every production environment
(including both cloud and on-premise), result in the overall management of software at scale becoming tedious, error-prone 
and ineffective.

## Why is this a huge problem?

Most prominently, with the general unalignment of how software is defined and managed throughout the whole company,
it is not possible without additional overhead (like setting up even more processes and tools on top) to manage
the complete lifecycle of all solutions, services or individual deployment artifacts running in any
given landscape. Even worse, when trying to set up new landscapes, it becomes a nightmare to successfully orchestrate, 
deploy and configure the needed software components in the new environments.

As long as individual development teams within a company continue to use their own tools and processes to manage the
lifecycle of the software they are responsible for, this unsatisfying (and finally TCD and TCO affecting) situation can
not improve and will only get worse over time.

## How can this improve?
The major problem at hand here is the absence of one aligned software component model, consistently used across the
enterprise, to manage compliant software components and their technical artifacts. Such
a model would help not only with streamlined deployments to public and private cloud environments, but also in various
other areas of lifecycle management like compliance processes and reporting. This software component model must describe 
all technical artifacts of a software product, and establish an ID for each component, which should then be used across 
all lifecycle management tasks.

Here, it is also crucial to understand that setting up local environments often requires the use of local artifacts. 
This is especially true for resticted or private clouds, in which it is usually not possible to access artifacts from 
their original source location (due to resticted internet access), leading to the fact that artifacts need to be 
transported into these environments. This local deployment scenario requires that software components must clearly 
separate their ID from the location of their technical artifacts, so that this techical location may change, without 
changing the ID.

At its heart, the model has to be technology-agnostic, so that not only modern containerized cloud,
but also legacy software is supported, out-of-the-box. It simply has to be acknowledged that companies are not able to
just drop everything that has been used in the past and solely use new cloud native workloads. This fact makes it
crucial to establish a common component model, which is able to handle both cloud native and legacy software, for which
it needs to be fully agnostic about the technology used.

Additionally, the model needs to be easily extensible. No one is able to
predict the future, apart from the fact that things will always change, especially in the area of IT. Being able to
adapt to future trends, without constantly affecting the processes and tools responsible for the core of the lifecycle
management of software, is a must.

**Todo: Describe why existing component models could not be used, why is our model better**
**Todo: Add image**

## Scope

Operating software installations/products, both for cloud and on-premises, covers many aspects:

- How, when and where are the technical artifacts created?
- How are technical artifacts stored and accessed?
- Which technical artifacts are to be deployed?
- How is the configuration managed?
- How and when are compliant checks, scanning etc. executed?
- When are technical artifacts deployed?
- Where and how are those artifacts deployed?
- Which other software installations are required and how are they deployed and accessed?
- etc.

The overall problem domain has a complexity that make it challenging to be solved as a whole.
However, the problem domain can be divided into two disjoint phases:

- production of technical artifacts
- deployment and lifecycle management of technical artifacts

The produced artifacts must be stored somewhere such that they can be accessed and collected for the deployment.
The OCM defines a standard to describe which technical artifacts belong to a software installation and how to
access them which could be used at the interface between production and the deployment/lifecycle management phase.

The OCM provides a common standard  for
- compliance checks
- security scanning
- code signing
- transport
- deployment or 
- other lifecycle-management aspects.

In that sense, the OCM provides the basis to
- exchange information about software in a controlled manner by defining a location- and technology-agnostic reference 
framework to identify software artifacts
- enable access to local technical artifacts via these IDs

If software installations are described using the OCM, e.g. a scanning tool could use this to collect all technical
artifacts it needs to check. If the technical resources of different software installations are described with different
formalisms, such tools must provide interfaces and implementations for all if them and data exchange becomes a nightmare.

This problem becomes even harder if a software installation is build of different parts/components, each described with
another formalism. OCM allows a uniform definition of such compositions such that one consistent description of 
a software installation is available.

The OCM does not make any assumptions about the (**Todo: Is this really the case?**)

- kinds of technical artifacts (e.g. docker images, helm chart, binaries etc., git sources)
- technology how to store and access technical artifacts (e.g. as OCI artifacts in an OCI registry)

OCM is a technology-agnostic specification and allows implementations to define exactly those technical aspects
as an extension of the basic model.

**ToDo: Reference to our OCI based realization**


