# BioCypher - TUM AI CKG Preprocessing Pipeline
This repository contains the preprocessing pipeline for the TUM AI CKG.
Currently, it us used to access the CKG including patient information and write
subject (case) and phenotype (phenotypic feature) nodes as well as
subject-phenotype relationships to CSV files (Biolink model names in brackets).

## Installation
Requires [Poetry](https://python-poetry.org/).

```{code-block} bash
git clone https://github.com/saezlab/tum-bc.git
cd tum-bc
poetry install
```

## Usage
From this environment just created by Poetry (which should already be
activated), you can run the pipeline with the following command:

```{code-block} bash
python script.py
```

Should the environment not be active, activate it using `poetry shell`.

The adapter needs to connect to a running instance of the CKG Neo4j graph. The
authentication for the connection to Neo4j can be configured in the
configuration file (`config/neo4j_config.yaml`) or directly in the `adapter.py`
file (in the "read driver" instantiation). If everything goes alright, the
adapter will write six CSV files to the a subfolder (datetime) of the
`biocypher-out` directory. Three of these files contain the headers while the
other three contain the data.

## Troubleshooting
If running CKG on a Neo4j store version > 4.0, you might need to set the
`multi_db` parameter to `True` in the `adapter.py` file (in the "read driver"
instantiation).
