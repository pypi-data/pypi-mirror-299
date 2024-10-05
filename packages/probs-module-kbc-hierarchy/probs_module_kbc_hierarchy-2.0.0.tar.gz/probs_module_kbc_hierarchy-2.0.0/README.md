# PRObs module: KBC hierarchy

This module contains the scripts for the "data enhancement", inferring new aggregated Observations from the existing Observations.

These scripts are compatible with [RDFox](https://www.oxfordsemantic.tech) version 7.

## Running the RDFox scripts

This module reads the RDF file (`probs_original_data`), runs rules to infer new Observations based on process/object composition/equivalence, and saves them into RDF (`probs_enhanced_data`).

To run the module:

```sh
RDFox sandbox %root% scripts/kbc-hierarchy/master [<OPTIONS>]
```

where `%root%` is the path to this folder.

Optional named arguments can be given in any order:

- `stats {enabled | disabled}`
  - enable additional performance stats
  - default value: `disabled`
- `variant %variant-name%`
  - load variant of scripts from named subdirectory
  - default value: `equivalence_composition`

The enhanced data will be written to `data/probs_enhanced_data`.

## Using probs-runner

Using [probs-runner](https://github.com/probs-lab/probs-runner), this module can be run using the `probs_kbc_hierarchy` function.
