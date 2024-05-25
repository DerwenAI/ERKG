
import os
import sys

from icecream import ic
import dotenv

# see answer by @gino-mempin
# https://stackoverflow.com/questions/78105511/importerror-cannot-import-name-ollama-from-llama-index-llms-unknown-locati
from llama_index.legacy.llms.ollama import CompletionResponse, Ollama

from llama_index.legacy.data_structs.data_structs import KG
from llama_index.legacy.graph_stores.neo4j import Neo4jGraphStore
from llama_index.legacy.indices.knowledge_graph.base import KnowledgeGraphIndex
from llama_index.legacy.query_engine import RetrieverQueryEngine
from llama_index.legacy.retrievers import KGTableRetriever
from llama_index.legacy.service_context import ServiceContext
from llama_index.legacy.storage.storage_context import StorageContext


if __name__ == "__main__":
    # load Neo4j credentials and create a storage context
    dotenv.load_dotenv(dotenv.find_dotenv())

    bolt_uri: str = os.environ.get("NEO4J_BOLT")
    database: str = os.environ.get("NEO4J_DBMS")
    username: str = os.environ.get("NEO4J_USER")
    password: str = os.environ.get("NEO4J_PASS")

    graph_store: Neo4jGraphStore = Neo4jGraphStore(
        url = bolt_uri,
        database = database,
        username = username,
        password = password,
    )

    storage_context: StorageContext = StorageContext.from_defaults(
        graph_store = graph_store
    )


    # load a local model and create a service context
    llm: Ollama = Ollama(
        model = "llama3",
        base_url = "http://localhost:11434",
        request_timeout = 60.0,
    )

    service_context: ServiceContext = ServiceContext.from_defaults(
        llm = llm,
        embed_model = "local:BAAI/bge-small-en",
    )

    # run a test prompt, just for kix
    test_prompt: str = "How many licks to get to the center of a tootsie pop? Answer yes or no only."
    response: CompletionResponse = llm.complete(test_prompt)
    ic(response.text)


    # set up a KG index
    kg_index: KnowledgeGraphIndex = KnowledgeGraphIndex(
        index_struct = KG(index_id = "vector"),
        service_context = service_context,
        storage_context = storage_context,
    )

    graph_rag_retriever: KGTableRetriever = KGTableRetriever(
        index = kg_index,
        retriever_mode = "keyword",
    )

    kg_rag_query_engine: RetrieverQueryEngine = RetrieverQueryEngine.from_args(
        retriever = graph_rag_retriever,
        service_context = service_context,
    )

    #sys.exit(0)
    #print(type(kg_index))
    response_graph_rag = kg_rag_query_engine.query("Tell me about Peter Quill.")
    ic(response_graph_rag)
    #display(Markdown(f"<b>{response_graph_rag}</b>"))
