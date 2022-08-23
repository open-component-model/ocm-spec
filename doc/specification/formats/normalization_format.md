# Base Format for Normalization
The OCM component model allows for signing component descriptors. Signing is done using a text based format. Usually component descriptors are stored as yaml files. The signing ensures that a component has not been tampered with since ist was signed. As yaml is a text based format the signing should be robust against various minor changes not effecting the integrity:

* formatting issue (e.g. different indent depth)
* comments
* HTML escaping
* ...

Furthermore the OCM supports transportation of artifacts between repositories. Scenarios should be supported where artifacts are fetched from a different repository compared to the one it was signed from. This implies changing URLs in the component descriptor.

These two requirements result in the definition of a normalization format and procedure.

As a first step the component descriptor is converted to JSON and all line breaks are removed.