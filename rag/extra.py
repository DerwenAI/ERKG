
sys.exit(0)


#import llama_index
from IPython.display import Markdown, display
from llama_index.data_structs.data_structs import KG
from llama_index.graph_stores import Neo4jGraphStore
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.retrievers import KGTableRetriever
from llama_index.storage.storage_context import StorageContext



graph_store = Neo4jGraphStore(
    username = "neo4j",
    password = "password",
    url = "bolt://localhost:7687",
    database="neo4j",
)

storage_context = StorageContext.from_defaults(graph_store=graph_store)

kg_index = llama_index.KnowledgeGraphIndex(
    index_struct = KG(index_id="vector"),
    service_context = service_context,
    storage_context = storage_context,
)

graph_rag_retriever = KGTableRetriever(
    index = kg_index,
    retriever_mode = "keyword",
)

kg_rag_query_engine = RetrieverQueryEngine.from_args(
    retriever=graph_rag_retriever,
    service_context = service_context,
)

response_graph_rag = kg_rag_query_engine.query("Tell me about Peter Quill.")
display(Markdown(f"<b>{response_graph_rag}</b>"))
