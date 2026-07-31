"""
Evaluation Module for Graph-RAG Pipeline.
Computes RAGAS metrics (Faithfulness, Answer Relevance, Context Precision, Context Recall)
and custom Graph-Specific metrics (Text-to-Cypher Execution).
"""
import json
from loguru import logger

# Import Ragas and Langchain components
try:
    from ragas import evaluate
    from ragas.metrics import (
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    )
    from langchain_groq import ChatGroq
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from datasets import Dataset
except ImportError as e:
    logger.error(f"Evaluation dependencies missing: {e}. Please run: pip install ragas datasets")
    raise

import leaseguard.config as cfg
from leaseguard.intelligence.graph_rag import GraphRAG

class LeaseEvaluator:
    """Evaluates the Graph-RAG pipeline."""
    
    def __init__(self, graph_rag: GraphRAG | None = None):
        self.graph_rag = graph_rag or GraphRAG()
        self._init_ragas_llm()

    def _init_ragas_llm(self):
        """Configure RAGAS to use the free Groq LLM instead of OpenAI."""
        logger.info("Initializing Ragas with ChatGroq (llama-3.1-70b-versatile)")
        
        # We use a known fast/capable model for judging
        self.eval_llm = ChatGroq(
            model_name="llama-3.1-70b-versatile",
            temperature=0,
            api_key=cfg.GROQ_API_KEY
        )
        self.eval_embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        # In Ragas 0.2+, we wrap the langchain LLM and Embeddings
        # but we can try to duck-type it directly if the wrapper isn't strictly required
        # For compatibility, we'll try applying them directly to the metrics.
        for metric in [faithfulness, answer_relevancy, context_precision, context_recall]:
            try:
                from ragas.llms import LangchainLLMWrapper
                from ragas.embeddings import LangchainEmbeddingsWrapper
                metric.llm = LangchainLLMWrapper(self.eval_llm)
                if hasattr(metric, 'embeddings'):
                    metric.embeddings = LangchainEmbeddingsWrapper(self.eval_embeddings)
            except ImportError:
                # Fallback for Ragas 0.1.x
                metric.llm = self.eval_llm
                if hasattr(metric, 'embeddings'):
                    metric.embeddings = self.eval_embeddings

    def evaluate_graph_rag(self, test_cases: list[dict]) -> dict:
        """
        Evaluate standard Ragas metrics for Q&A.
        
        test_cases format:
        [
            {"question": "...", "ground_truth": "..."},
            ...
        ]
        """
        data = {
            "question": [],
            "answer": [],
            "contexts": [],
            "ground_truth": []
        }
        
        logger.info(f"Running Graph-RAG pipeline on {len(test_cases)} test cases...")
        
        for case in test_cases:
            question = case["question"]
            logger.info(f"Q: {question}")
            
            result = self.graph_rag.answer(question)
            
            # Format graph context as JSON string, combine with document chunks
            graph_ctx_str = json.dumps(result["graph_context"], default=str)
            doc_ctx_list = [chunk["text"] for chunk in result["doc_context"]]
            
            # Ragas expects contexts to be a list of strings
            combined_contexts = [graph_ctx_str] + doc_ctx_list
            
            data["question"].append(question)
            data["answer"].append(result["answer"])
            data["contexts"].append(combined_contexts)
            data["ground_truth"].append(case["ground_truth"])
            
        dataset = Dataset.from_dict(data)
        
        logger.info("Computing RAGAS metrics...")
        # Run Ragas evaluation
        ragas_result = evaluate(
            dataset,
            metrics=[
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall,
            ],
        )
        return ragas_result

    def evaluate_cypher_accuracy(self, questions: list[str]) -> dict:
        """
        Graph-Specific Metric: Text-to-Cypher execution rate.
        Measures if the generated Cypher query executes without syntax errors.
        """
        results = {
            "total": len(questions),
            "successful_execution": 0,
            "failed_execution": 0,
            "details": []
        }
        
        logger.info(f"Evaluating Text-to-Cypher for {len(questions)} questions...")
        
        for q in questions:
            res = self.graph_rag.cypher_answer(q)
            success = res["error"] is None
            
            if success:
                results["successful_execution"] += 1
            else:
                results["failed_execution"] += 1
                
            results["details"].append({
                "question": q,
                "cypher": res["cypher"],
                "success": success,
                "error": res["error"],
                "row_count": len(res["rows"]) if success else 0
            })
            
        # Calculate execution rate
        results["execution_rate"] = results["successful_execution"] / results["total"] if results["total"] > 0 else 0
        return results
