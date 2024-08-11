Set up the Python environment:

```bash
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install -U pip wheel
python3 -m pip install -r requirements.txt
```


Prepare the data subset:

  1. Download from <https://www.opensanctions.org/docs/bulk/senzing/>
  2. Extract subsets for London, excluding Open Ownership (too large for demo)

```bash
mkdir -p subset
grep -i london default.json > subset/default.json
grep -i london sanctions.json > subset/sanctions.json
grep -i london gleif.json > subset/gleif.json
```


Run the Jupyterlab notebooks:

```bash
./venv/bin/jupyter-lab
```


