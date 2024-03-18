# senzing_neo4j

Demonstrate an integration of Senzing and Neo4j, using _entity resolution_
in Senzing to resolve the business names and addresses for three datasets,
then construct a _knowledge graph_ in Neo4j from the results.


## Set up environment

```bash
python3.11 -m venv venv
source venv/bin/activate
python3 -m pip install -U pip wheel setuptools
python3 -m pip install -r requirements.txt 
```

## Run demo

```bash
./venv/bin/jupyter lab
```

Then open the `demo.ipynb` notebook.
