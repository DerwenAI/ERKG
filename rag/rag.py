
import sys

#from llama_index.callbacks.global_handlers import set_global_handler
from llama_index.core import set_global_handler

from llama_index import ServiceContext 
from llama_index.llms import Ollama

llm = Ollama(
    model = "mistral",
    base_url = "http://localhost:11434",
)

service_context = ServiceContext.from_defaults(
    llm = llm,
    embed_model = "local:BAAI/bge-small-en",
)
