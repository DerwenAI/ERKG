# senzing_neo4j

Demonstrate integration of Senzing and Neo4j: use _entity resolution_
in Senzing to resolve duplicate business names and addresses in the
Las Vegas metropolitan area from three datasets.
Then construct a _knowledge graph_ in Neo4j from these results.


## Set up environment

```bash
python3.11 -m venv venv
source venv/bin/activate
python3 -m pip install -U pip wheel setuptools
python3 -m pip install -r requirements.txt 
```

## Run demo

See the tutorial in `article/draft.md` and launch Jupyter:

```bash
./venv/bin/jupyter lab
```

Then open the notebooks:

  1. `examples/datasets.ipynb`
  2. `examples/graph.ipynb`
