## Custom builds of the ontology including additional data / external ontologies

To create a converted/bundled ontology, ready for use with the PRObs system scripts (e.g. `kbc-completion` and `endpoint`):

- Convert the ontology to Datalog rules: `python convert_ontology.py [PATH TO ontology.nt]`

- The converted files are in `conversion/data/probs.ttl` and `conversion/data/probs_ontology_rules.dlog`

To release a new version of the converted/bundled ontology as a module for use with probs-runner:

- Edit package version/metadata in `pyproject.toml`.

- Build the package: `python -m build`

- Publish the package to PyPI: `twine upload dist/probs_module_ontology-[...]`
