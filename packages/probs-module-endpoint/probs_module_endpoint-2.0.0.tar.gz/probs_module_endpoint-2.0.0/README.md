# PRObs endpoint module

This module contains scripts rules for reasoning.

These scripts are compatible with [RDFox](https://www.oxfordsemantic.tech) version 7.

## Running the RDFox scripts

The scripts read the RDF file with the data (by default, `data/probs_original_data` and `data/probs_enhanced_data`), adds the reasoning rules, and opens the SPARQL endpoint.

How to execute it:

```sh
RDFox sandbox <root> scripts/endpoint/master [endpoint.port <port>]
```

where `<root>` is the path to this folder, and `<port>` is optionally the port for the endpoint to listen on.

Then go to [`http://localhost:12110/console/default`](http://localhost:12110/console/default) to run your SPARQL queries.

The scripts `load_data` and `load_rules` can be customised to load data and rules from different files.

## Using probs-runner

Using [probs-runner](https://github.com/probs-lab/probs-runner), this module can be run using the `probs_endpoint` function.
