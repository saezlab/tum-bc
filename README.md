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

The adapter needs to connect to a running instance of the CKG Neo4j graph. The
authentication for the connection to Neo4j can be configured in the
`adapter.py` file (in the "read driver" instantiation) or by passing a
configuration file.