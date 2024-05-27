KG+RAG examples,
to extend <https://neo4j.com/developer-blog/entity-resolved-knowledge-graphs/#neo4j>


## LlamaIndex

Download `ollama` and launch: <https://github.com/ollama/ollama>

```bash
ollama run llama3
```

Set up the Python environment:

``bash
python3.11 -m venv venv
source venv/bin/activate
python3.11 -m pip install -U pip wheel setuptools
python3.11 -m pip install -r requirements.txt
```

Then make sure you have the `nltk` corpora loaded:

```bash
python3 load_nltk.py
```

To parse/load a KG based on the Wikipedia example, run:

```bash
python3 llama_rag.py
```
