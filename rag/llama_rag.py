#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PoC for KG+RAG using `llama-index`, `ollama`, `neo4j`, and "llama3"

Based on:

  * <https://guitton.co/posts/graphs-and-language>
  * <https://docs.llamaindex.ai/en/stable/examples/index_structs/knowledge_graph/Neo4jKGIndexDemo/>

NB: this code uses `llama-index` v0.10.x under the "legacy" branch --
Which ATM seems most stable? See answer by @gino-mempin
<https://stackoverflow.com/questions/78105511/importerror-cannot-import-name-ollama-from-llama-index-llms-unknown-locati>
"""

import os
import sys  # pylint: disable=W0611
import traceback
import typing

from icecream import ic  # pylint: disable=E0401
from pyinstrument import Profiler  # pylint: disable=E0401
import dotenv

from llama_index.legacy.core.response.schema import Response
from llama_index.legacy.data_structs.data_structs import KG
from llama_index.legacy.graph_stores.neo4j import Neo4jGraphStore
from llama_index.legacy.indices.knowledge_graph.base import KnowledgeGraphIndex
from llama_index.legacy.llms.ollama import CompletionResponse, Ollama
from llama_index.legacy.query_engine import RetrieverQueryEngine
from llama_index.legacy.readers.wikipedia import WikipediaReader
from llama_index.legacy.retrievers import KGTableRetriever
from llama_index.legacy.service_context import ServiceContext
from llama_index.legacy.storage.storage_context import StorageContext


def init_service (
    *,
    model: str = "llama3",
    base_url: str = "http://localhost:11434",
    embed_model: str = "local:BAAI/bge-small-en",
    ) -> ServiceContext:
    """
Load a local model using `ollama` orchestration.
Then initialize and return a service context.
    """
    llm: Ollama = Ollama(
        model = model,
        base_url = base_url,
        #request_timeout = 60.0,
    )

    return ServiceContext.from_defaults(
        llm = llm,
        embed_model = embed_model,
    )


def connect_neo4j (
    ) -> StorageContext:
    """
Load the Neo4j credentials.
Then create and return a storage context.
    """
    try:
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

        return StorageContext.from_defaults(
            graph_store = graph_store
        )
    except Exception as ex:  # pylint: disable=W0718
        ic(ex)
        traceback.print_exc()


def build_engine (
    service_context: ServiceContext,
    *,
    documents: typing.Optional[ list ] = None,
    response_mode: str = "compact",
    ) -> RetrieverQueryEngine:
    """
Build a KG index, using either:

  * newly constructed KG from documents, stored in a graph DB
  * previously constructed KG, retrieved from a graph DB

Then build and return a query engine based on it.
    """
    if documents is not None:
        kg_index: KnowledgeGraphIndex = KnowledgeGraphIndex.from_documents(
            documents,
            storage_context = connect_neo4j(),
            service_context = service_context,
            max_triplets_per_chunk = 5,
            include_embeddings = False,
            kg_triplet_extract_fn = None,
            kg_triple_extract_template = None,
        )
    else:
        kg_index = KnowledgeGraphIndex(
            index_struct = KG(index_id = "vector"),
            storage_context = connect_neo4j(),
            service_context = service_context,
        )

    return RetrieverQueryEngine.from_args(
        retriever = KGTableRetriever(
            index = kg_index,
            retriever_mode = "keyword",  # "hybrid"
        ),
        service_context = service_context,
        response_mode = response_mode,
    )


if __name__ == "__main__":
    profiler: Profiler = Profiler()
    profiler.start()

    service_context: ServiceContext = init_service()

    ######################################################################
    # load data from Wikipedia docs to build a KG
    # then build a query engine from triples retrieval

    documents: list = WikipediaReader().load_data(
        pages = ["Guardians of the Galaxy Vol. 3"],
        auto_suggest = False,
    )


    ## NOTE: uncomment the `documents` parameter to build a KG
    ## then comment the parameter to reuse the built KG
    query_engine: RetrieverQueryEngine = build_engine(
        service_context,
        documents = documents,
        response_mode = "refine",  # "compact"
    )


    ######################################################################
    # run queries

    test_prompt: str = "Tell me about Peter Quill."

    if False:  # True
        # run a test prompt without RAG, just for kix
        response: CompletionResponse = llm.complete(test_prompt)
        ic(response.text)

    response: response = query_engine.query(test_prompt)
    ic(response)


    ######################################################################
    # report performance profiling

    profiler.stop()
    profiler.print()
