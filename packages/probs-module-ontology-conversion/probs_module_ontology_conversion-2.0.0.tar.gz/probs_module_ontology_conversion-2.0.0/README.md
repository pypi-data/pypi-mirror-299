# PRObs ontology conversion module

This module contains scripts for converting an ontology to Datalog rules and bundling additional required facts together.

These scripts are compatible with [RDFox](https://www.oxfordsemantic.tech) version 7.

## Running the RDFox scripts

This module reads the ontology definitions and data, and extracts the equivalent Datalog rules.  The data is read from a file called `data/ontology.nt`.  The Datalog rules are written to a file called `data/probs_ontology_rules.dlog`.

To run the module:

```sh
RDFox sandbox <root> scripts/ontology-conversion/master
```

where `<root>` is the path to this folder.

## Using probs-runner

Using [probs-runner](https://github.com/probs-lab/probs-runner), this module can be run using the `probs_convert_ontology` function.

## Custom builds of the ontology including additional data / external ontologies

We build a version of the PRObs ontology bundled with the core external ontologies (PROV, QUDT) that are used with it, for convenience in loading into tools such as RDFox.

If you want to use additional ontologies or data (e.g., details of specific time periods or regions where your data is measured), you may find it useful to create a custom build by modifying the ontologies in the `conversion` subfolder.

See [conversion/README.md](conversion/README.md) for more details.
