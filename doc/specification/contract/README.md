# 2.3 Model Contract

The greatest value of the Open Component Model comes
with the tools interacting with the model and its content, the contract between tools and OCM.

One example of such a tool is the [transport](../../introduction/transports.md) tool provided
by the OCM CLI. It uses the access information of resources contained in a component version to copy software artifacts from one environment into another. If required it adapts the resource locations registered for the component version in the target environment.

Another example could be a deployment tool accessing a component version to determine the artifacts, which should be deployed into a target environments.

Such tools and their specification ar not part of the OCM specification. Nevertheless, they have to interact with the content described by the Open Component Model.

To do so, there must be a clear contract between the model and the way tools interact with the model.

There are two basic parts for this contract:
- All content required to deploy and install software described by a component version must be included as resources in this component version.
- All resource locations (e.g. image locations) used in a runtime environment must be taken directly or indirectly from the access information provided by the used component versions.

This is required to fulfill the promise made by the Open Component Model:

*Being able to describe closed Software Bills of Delivery enabling the transport of software from one environment into another one, and the deployment of this software in decoupled or isolated target environments.*

This has various consequences especially for deployment environments,
but basically for all tools working with the component model and even the component model itself:

- (Deployment) Descriptions for dedicated tools describing software artifacts used by these tools must be part of a component version. They have to be stored as additional resources with an appropriate own (tool/technology specific) artifact type.
- Those descriptions must use descriptive elements based on the component model to denote those artifacts. It is not possible anymore to describe explicit, absolute or global direct artifact locations.
- Even component names or versions must not be used, because they would
  impede the possibility of other tools to detect the complete set of required artifacts (for example for the transport tool)
- To avoid the need of describing always complete closed sets of artifacts in a single component version the model must be able to aggregate/include artifact sets provided by other component versions. This directly motivates the [component reference/aggregation feature](../elements/README.md#aggregation) of a component version.
- With this, a component version must include all resources, either by resources directly described by the component version or by referring to other component versions recursively describing these resources.
- The artifacts described by such a tool specific description must be resolvable in the context of the component version containing this description as artifact.
- This directly leads to the notion of [relative artifact references](../elements/README.md#artifact-references). The denotation of described artifacts is always given by a sequence of reference identities and a final resource [identity](../elements/README.md#identities). This sequence leads, starting from the initial component version, following the component references, to the component version finally containing the desired resource. This path does not contain any absolute component names, but only relative names or better identities in the context of the dedicated component versions along the access path.
- The same rules that apply to description artifacts, also apply to artifacts used as executable entity (container image or plain executable). This means, even those artifacts must not use artifact locations provided during their build/production process. (For example, a container image intended to deploy other executable elements must not use hard-wired resource locations). Instead, the deployment of such an element must be fed with configuration data describing those locations finally taken from the component version describing the deployment of this element. So, the task of a deployment tool is to extract this information from the actually used component version and provide appropriate input for the executable entity.

## Comparison with well-known environments

Let's motivate all this by comparing it with some well-known technology having similar requirements: the Filesystem and a file based build technology like *make*. A make project should consist of a self-contained set of build resources. also. As a build description must be able to describe rules on those resources.

### Filesystem based Build Tool

The filesystem is a hierarchical namespace used to address named content described by files organized in directories.

*Make* is tool executing some build steps of a source structure.
The build description is stored as a dedicated file called *Makefile*.which is typically located in the root folder of a build project.

A simple example could look like this:

```go
/
└── some
    └── project
        └── location
            ├── Makefile
            └── src
                ├── lib
                │   ├── lib.c
                │   └── lib.h
                └── main.c
```

The filesystem path `/some/project/location` contains the files belonging to the build projects, described by a *Makefile* in this directory. The sources are contained in a subdirectory `src`, which again has a deep structure.

You can produce the executable `echo` by switching to the folder `/some/project/location` and executing `make`.

How does the Makefile denote files relevant for the build steps? Let's have a look into this file.

**Makefile**:
```make
echo: gen gen/main.o gen/lib.o
        cc -o gen/echo gen/main.o gen/lib.o

gen/main.o: src/main.c src/lib/lib.h 
        cc -c src/main.c -o gen/main.o

gen/lib.o: src/lib/lib.c src/lib/lib.h
        cc -c src/lib/lib.c -o gen/lib.o

gen:
        mkdir gen

clean: 
        rm -rf gen
```

You can see, that the file resources are denoted by path names relative
to the directory containing the *Makefile*. Why is it done this way instead of using absolute path names? Using such relative path names allow to package
the complete project (for example with `cd /some/project/location; tar cvf ../echo.tar .`). You can take this archive and transport it onto another host and unpack it under some arbitrary directory (for example `cd /my/local/echo; tar xvf echo.tar`). Just executing `make` again, builds your echo command in the new location.

<div align="center"> 
<img src="make.png" alt="Structure of the make filesystem" width="800"/>
</div>

This is basically the same scenario we have to solve with the Open Component Model and tools working with provided content.

### How does it look like in the Open Component Model

The component model describes a hierarchical namespace for component versions. Component versions are stored in a component repository.  A component version describes resources like files in a filesystem folder. The component version references can be seen as counterpart to sub folders in a filesystem (better: symbolic links) and span a directed graph with a navigatable using local names of the references in the context of the containing component versions.

<div align="center"> 
<img src="resref.png" alt="Structure of OCM Resources" width="800"/>
</div>

Our make project is comparable to the content of a component version.
The substructure maps to a sequence of component references.

The *Makefile* is a description used by the tool *make* and refers to filesystem resources. A tool acting on the component model works exactly the same way. The description used to control the functionality of the tool is stored as artifact in the root component version (It uses a tool/technology specific artifact type). It describes the required resources by means of the component model by using relative artifact references following the reference sequence of aggregated component versions up to the final artifact resource.

Such a description could look like this:

**Description Resource** (artifact type `myToolDescription`):
```
version: v1
target: ...
resources:
  - name: lib-h
    path:
      - name: lib
  - name: lib-c
    path:
      - name: lib
  - name: main-c
```

It is based on a component structure looking like this:

```
COMPONENT                     NAME        VERSION IDENTITY TYPE              RELATION
└─ mandelsoft.org/demo/make               0.0.1                              
   ├─                         description 0.0.1            myToolDescription local
   ├─                         main-c      0.0.1            PlainText         local
   └─ mandelsoft.org/demo/lib lib         0.0.1                              
      ├─                      lib-c       0.0.1            PlainText         local
      └─                      lib-h       0.0.1            PlainText         local
```

A library component version `mandelsoft.org/demo/lib` contains some library resources (for sure dedicated files of an archive would never be represented as dedicated resources in a component version, this is just an example illustrating the similarities to our make scenario).

This top-level component version `mandelsoft.org/demo/make:0.0.1` describes the top-level resources as direct resources: a resource `description` for the tool specific description file (of type `myToolDescription`) and some resource `main-c`. To get access to the library resources, the top-level component aggregates the library component version by adding a component version reference to this component version. This resource and the two library resources
are described by the description file, above, using resource references relative to the component version hosting the description file, like a *Makefile* described relative file paths to denote the required resources in the directory structure. 

<div align="center"> 
<img src="ocm.png" alt="Structure of OCM Resources" width="800"/>
</div>

The tool typically does not understand such resource references, unless it is explicitly designed to work with the component model. Therefore, an adaptation
of the OCM related descriptions formats into description formats understandable by the  native tools must be done by some adapter.

The process of adapting (deployment) descriptions to reflect resource locations valid in a dedicated target environment based on information provided by a component version is called *Localization* and must always be done, when dealing with content delivered via component versions.

## Real life example

As native technology we use the [helm deployment system](https://helm.sh/) for Kubernetes.

A helm chart describes Kubernetes resources, which are templated using some values.
provided when deploying a chart.

Typically, a helm chart may contain container image references used for the described pods. This violates the above contract: the location of resources must be taken from the component version describing the deployment description resource (the helm chart).

### Simple Deployments

Because of this kind of required *image localization*, all images in a chart must be templated to be able to specify the concrete values by the deployment configuration.

A component version used to deliver a helm chart therefore requires several resources:
- all the images required for the helm chart
- the helm chart
- a helm specific description file relating the helm chart resource with all the image resources. It describes which value names should be fed with which image location taken from the component version containing this description.

The OCM deploy adapter known the format of this description resource and merge
a user provider configuration file with the described image location properties.
The resulting helm values file can then be passed to the native helm deployment tool to deploy the application.

<div align="center"> 
<img src="ocm-helm-simple.png" alt="OCM and Helm Deployments" width="800"/>
</div>

### Indirect Deployments

If a used image itself contains code used to deploy pods to a Kubernetes cluster (for example an operator managing some kind of service instances), these image locations must also be taken from the actual component version. This requires an additional indirection. The executable of the image must take some argument to pass the locations, for example by passing a config file. This must (potentially additionally) be provided by the helm chart and templated by additional image location properties, which must be described in the description resource and fed by the adapter.

<div align="center"> 
<img src="ocm-helm-indirect.png" alt="OCM and Helm Deployments with indirect Deployments" width="800"/>
</div>