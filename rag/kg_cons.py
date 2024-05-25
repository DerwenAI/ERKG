from llama_index import ServiceContext, KnowledgeGraphIndex
from llama_index import download_loader
from llama_index.graph_stores import Neo4jGraphStore
from llama_index.llms import Ollama
from llama_index.storage.storage_context import StorageContext

llm = Ollama(
    model = "mistral",
    base_url = "http://localhost:11434",
)

service_context = ServiceContext.from_defaults(
    llm = llm,
    embed_model = "local:BAAI/bge-small-en",
)

graph_store = Neo4jGraphStore(
    username = "neo4j",
    password = "password",
    url = "bolt://localhost:7687",
    database = "neo4j",
)

storage_context = StorageContext.from_defaults(graph_store=graph_store)

loader = download_loader("WikipediaReader")()

documents = loader.load_data(
    pages = ["Guardians of the Galaxy Vol. 3"],
    auto_suggest = False,
)

kg_index = KnowledgeGraphIndex.from_documents(
    documents,
    storage_context = storage_context,
    service_context = service_context,
    max_triplets_per_chunk = 5,
    include_embeddings = False,
    kg_triplet_extract_fn = None,
    kg_triple_extract_template = None,
)
