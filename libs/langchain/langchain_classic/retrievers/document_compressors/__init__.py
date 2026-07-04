import importlib
from typing import Any

from langchain_classic.retrievers.document_compressors.base import (
    DocumentCompressorPipeline,
)
from langchain_classic.retrievers.document_compressors.chain_extract import (
    LLMChainExtractor,
)
from langchain_classic.retrievers.document_compressors.chain_filter import (
    LLMChainFilter,
)
from langchain_classic.retrievers.document_compressors.cohere_rerank import CohereRerank
from langchain_classic.retrievers.document_compressors.cross_encoder_rerank import (
    CrossEncoderReranker,
)
from langchain_classic.retrievers.document_compressors.embeddings_filter import (
    EmbeddingsFilter,
)
from langchain_classic.retrievers.document_compressors.listwise_rerank import (
    LLMListwiseRerank,
)

_module_lookup = {
    "FlashrankRerank": "langchain_community.document_compressors.flashrank_rerank",
}


_ALLOWED_MODULE_PREFIX = "langchain_community.document_compressors."


def __getattr__(name: str) -> Any:
    if name in _module_lookup:
        module_path = _module_lookup[name]
        if not module_path.startswith(_ALLOWED_MODULE_PREFIX):
            msg = f"Invalid module path: {module_path}"
            raise ValueError(msg)
        module = importlib.import_module(module_path)
        return getattr(module, name)
    msg = f"module {__name__} has no attribute {name}"
    raise AttributeError(msg)


__all__ = [
    "CohereRerank",
    "CrossEncoderReranker",
    "DocumentCompressorPipeline",
    "EmbeddingsFilter",
    "FlashrankRerank",
    "LLMChainExtractor",
    "LLMChainFilter",
    "LLMListwiseRerank",
]
