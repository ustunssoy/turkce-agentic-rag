import os
from pathlib import Path
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EVALUATION_DATA_DIR = DATA_DIR / "evaluation"
FAISS_INDEX_DIR = DATA_DIR / "faiss_index"

# Ensure directories exist
for directory in [DATA_DIR, PROCESSED_DATA_DIR, EVALUATION_DATA_DIR, FAISS_INDEX_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


class Settings(BaseModel):
    # Project Info
    project_name: str = "Turkce-Agentic-RAG"
    version: str = "1.0.0"
    repo_url: str = "https://github.com/ustunssoy/turkce-agentic-rag"

    # Dataset Settings
    corpus_size: int = 2500
    corpus_path: Path = PROCESSED_DATA_DIR / "mevzuat_corpus_2500.json"
    benchmark_queries_path: Path = PROCESSED_DATA_DIR / "benchmark_queries.json"

    # LLM Settings
    openai_api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    llm_model: str = Field(default_factory=lambda: os.getenv("LLM_MODEL", "gpt-4o-mini"))
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.0"))

    # Embeddings & Reranker
    embedding_model_name: str = os.getenv(
        "EMBEDDING_MODEL_NAME", "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    )
    reranker_model_name: str = os.getenv("RERANKER_MODEL_NAME", "BAAI/bge-reranker-base")
    faiss_index_path: Path = FAISS_INDEX_DIR / "mevzuat_faiss.index"

    # Hybrid Retrieval Parameters
    top_k_bm25: int = int(os.getenv("TOP_K_BM25", "15"))
    top_k_dense: int = int(os.getenv("TOP_K_DENSE", "15"))
    top_k_final: int = int(os.getenv("TOP_K_FINAL", "5"))
    rrf_k: int = int(os.getenv("RRF_K", "60"))
    dense_weight: float = float(os.getenv("DENSE_WEIGHT", "0.6"))
    bm25_weight: float = float(os.getenv("BM25_WEIGHT", "0.4"))

    # Agent Loop Parameters
    max_rewrites: int = int(os.getenv("MAX_REWRITES", "2"))
    sufficiency_threshold: float = float(os.getenv("SUFFICIENCY_THRESHOLD", "0.65"))

    # Evaluation Output
    recall_report_path: Path = EVALUATION_DATA_DIR / "recall_benchmark_results.json"
    ragas_report_path: Path = EVALUATION_DATA_DIR / "ragas_evaluation_report.json"
    error_analysis_path: Path = EVALUATION_DATA_DIR / "error_analysis_report.json"

    # Server Settings
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))


settings = Settings()
