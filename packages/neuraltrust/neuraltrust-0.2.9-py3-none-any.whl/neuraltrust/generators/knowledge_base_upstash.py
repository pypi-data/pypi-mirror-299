import os
from typing import Dict, Optional, Sequence, List, Union

import logging
import uuid

import numpy as np
import pandas as pd
from sklearn.cluster import HDBSCAN
from upstash_vector import Index
from upstash_vector.types import RangeResult, QueryResult

from .base_knowledge_base import BaseKnowledgeBase
from ..llm.client import ChatMessage, LLMClient, get_judge_client
from ..llm.embeddings import get_default_embedding
from ..llm.embeddings.base import BaseEmbedding
from ..errors.exceptions import ImportError
from ..utils.language_detection import detect_lang
import upstash_vector

try:
    import umap
except ImportError as err:
    raise ImportError(missing_package="umap") from err

logger = logging.getLogger("neuraltrust.generators")

LANGDETECT_MAX_TEXT_LENGTH = 300
LANGDETECT_DOCUMENTS = 10

TOPIC_SUMMARIZATION_PROMPT = """Your task is to define the topic which best represents a set of documents.

Your are given below a list of documents and you must extract the topic best representing ALL contents.
- The topic name should be between 1 to 5 words
- Provide the topic in this language: {language}

Make sure to only return the topic name between quotes, and nothing else.

For example, given these documents:

<documents>
Camembert is a moist, soft, creamy, surface-ripened cow's milk cheese.
----------
Bleu d'Auvergne is a French blue cheese, named for its place of origin in the Auvergne region.
----------
Roquefort is a sheep milk cheese from the south of France.
</documents>

The topic is:
"French Cheese"

Now it's your turn. Here is the list of documents:

<documents>
{topics_elements}
</documents>

The topic is:
"""


class Document:
    """A class to wrap the elements of the knowledge base into a unified format."""

    def __init__(
            self,
            id_vector: str,
            metadata: Dict[str, str],
            vector: List[float]
    ):
        self.content = metadata.get('text', '')
        self.filename = metadata.get('url', '')
        self.id = id_vector
        self.embeddings = vector
        self.reduced_embeddings = None
        self.topic_id = None


class KnowledgeBaseUpstash(BaseKnowledgeBase):
    def __init__(
            self,
            url_upstash: str = None,
            token: str = None,
            seed: int = None,
            llm_client: Optional[LLMClient] = None,
            seed_topic: str = None,
            seed_topic_samples: int = 100
    ) -> None:

        if not url_upstash:
            url_upstash = os.getenv("UPSTASH_URL")

        if not token:
            token = os.getenv("UPSTASH_TOKEN")

        self.index = Index(url=url_upstash, token=token)
        print("Created index connector")

        self._embedding_model = get_default_embedding()
        self._documents = self.load_data(seed_topic=seed_topic, seed_topic_samples=seed_topic_samples)
        self._documents = [doc for doc in self._documents if doc.content.strip() != ""]

        self._rng = np.random.default_rng(seed=seed)
        self._llm_client = llm_client or get_judge_client()

        # # Estimate the minimum number of documents to form a topic
        self._min_topic_size = round(2 + np.log(len(self._documents)))

        self._embeddings_inst = np.array([doc.embeddings for doc in self._documents])
        self._topics_inst = None
        self._index_inst = None
        self._reduced_embeddings_inst = self.reduce_embeddings()

        # # Detect language of the documents, use only the first characters of a few documents to speed up the process
        document_languages = [
            detect_lang(doc.content[:LANGDETECT_MAX_TEXT_LENGTH])
            for doc in self._rng.choice(self._documents, size=LANGDETECT_DOCUMENTS)
        ]
        languages, occurences = np.unique(
            ["en" if (pd.isna(lang) or lang == "unknown") else lang for lang in document_languages], return_counts=True
        )
        self._language = languages[np.argmax(occurences)]

        self._documents_index = {doc.id: doc for doc in self._documents}

    def _get_documents(self, res: Union[RangeResult, QueryResult]) -> List[Document]:
        data = []
        vectors = res.vectors if isinstance(res, RangeResult) else res
        for vector_info in vectors:
            doc = Document(id_vector=vector_info.id,
                           metadata=vector_info.metadata,
                           vector=vector_info.vector)
            data.append(doc)
        return data

    def reduce_embeddings(self):
        reducer = umap.UMAP(
            n_neighbors=50,
            min_dist=0.5,
            n_components=2,
            random_state=1234,
            n_jobs=1,
        )
        reduced_vectors = reducer.fit_transform(self._embeddings_inst)
        for doc, reduced_vector in zip(self._documents, reduced_vectors):
            doc.reduced_embeddings = reduced_vector

        return reduced_vectors

    def load_data(self, seed_topic: str = None, seed_topic_samples: int = 10) -> List[Document]:
        print("Retrieving documents ...")
        if seed_topic is None:
            return self._load_all_data()
        else:
            return self._load_data_with_seed_topic(seed_topic, seed_topic_samples)

    def _load_all_data(self) -> List[Document]:
        res = self.index.range(cursor="", limit=5, include_vectors=True, include_metadata=True)
        data = self._get_documents(res)

        while res.next_cursor != "":
            res = self.index.range(cursor=res.next_cursor, limit=10, include_vectors=True, include_metadata=True)
            docs = self._get_documents(res)
            data.extend(docs)

        return data

    def _load_data_with_seed_topic(self, seed_topic: str, seed_topic_samples: int) -> List[Document]:
        seed_embedding = self._embedding_model.embed(seed_topic)
        # Ensure the embedding is a flat list of floats
        seed_embedding_list = seed_embedding.flatten().tolist() if isinstance(seed_embedding, np.ndarray) else seed_embedding
        try:
            res = self.index.query(
                vector=seed_embedding_list,
                top_k=seed_topic_samples,
                include_metadata=True,
                include_vectors=True,
                filter="url GLOB '*/documentacion/*'"
            )
        except upstash_vector.errors.UpstashError as e:
            print(f"Error querying Upstash: {e}")
            print(f"Full embedding: {seed_embedding_list}")
            raise
        
        return self._get_documents(res)

    @property
    def language(self):
        return self._language

    @property
    def _embeddings(self):
        return self._embeddings_inst

    @property
    def _reduced_embeddings(self):
        return self._reduced_embeddings_inst

    @property
    def _dimension(self):
        return self._embeddings[0].shape[0]

    def get_savable_data(self):
        return {
            "columns": self._columns,
            "min_topic_size": self._min_topic_size,
            "topics": {int(k): topic for k, topic in self.topics.items()},
            "documents_topics": [int(doc.topic_id) for doc in self._documents],
        }

    @property
    def _index(self):
        if self._index_inst is None:
            try:
                from faiss import IndexFlatL2
            except ImportError as err:
                raise ImportError(missing_package="faiss") from err

            self._index_inst = IndexFlatL2(self._dimension)
            self._index_inst.add(self._embeddings)
        return self._index_inst

    @property
    def topics(self):
        if self._topics_inst is None:
            self._topics_inst = self._find_topics()
        return self._topics_inst

    def _find_topics(self):
        logger.info("Finding topics in the knowledge base.")
        hdbscan = HDBSCAN(
            min_cluster_size=self._min_topic_size,
            min_samples=3,
            metric="euclidean",
            cluster_selection_epsilon=0.0,
        )
        clustering = hdbscan.fit(self._reduced_embeddings)

        for i, doc in enumerate(self._documents):
            doc.topic_id = clustering.labels_[i]

        topics_ids = set(clustering.labels_)
        topics = {
            idx: self._get_topic_name([self._documents[doc_id] for doc_id in np.nonzero(clustering.labels_ == idx)[0]])
            for idx in topics_ids
            if idx != -1
        }
        topics[-1] = "Others"

        logger.info(f"Found {len(topics)} topics in the knowledge base.")
        return topics

    def _get_topic_name(self, topic_documents):
        logger.debug("Create topic name from topic documents")
        self._rng.shuffle(topic_documents)
        topics_str = "\n\n".join(["----------" + doc.content[:500] for doc in topic_documents[:10]])

        # prevent context window overflow
        topics_str = topics_str[: 3 * 8192]
        prompt = TOPIC_SUMMARIZATION_PROMPT.format(language=self._language, topics_elements=topics_str)

        raw_output = self._llm_client.complete([ChatMessage(role="user", content=prompt)], temperature=0.0).content

        return raw_output.strip().strip('"')

    def get_random_document(self):
        return self._rng.choice(self._documents)

    def get_neighbors(self, seed_document: Document, n_neighbors: int = 4, similarity_threshold: float = 0.2):
        seed_embedding = seed_document.embeddings

        relevant_documents = [
            doc
            for (doc, score) in self.vector_similarity_search_with_score(seed_embedding, k=n_neighbors)
            if score < similarity_threshold
        ]

        return relevant_documents

    def similarity_search_with_score(self, query: str, k: int) -> Sequence:
        query_emb = np.array(self._embedding_model.embed(query), dtype="float32")
        return self.vector_similarity_search_with_score(query_emb, k)

    def vector_similarity_search_with_score(self, query_emb: np.ndarray, k: int) -> Sequence:
        query_emb = np.atleast_2d(query_emb)
        distances, indices = self._index.search(query_emb, k)
        return [(self._documents[i], d) for d, i in zip(distances[0], indices[0])]

    def __len__(self):
        return len(self._documents)

    def __getitem__(self, doc_id: str):
        return self._documents_index[doc_id]
