import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
from leaseguard.evaluation.metrics import LeaseEvaluator

# ── Golden Dataset ─────────────────────────────────────────────────────────────
# Ground truth QA pairs for testing Graph-RAG retrieval and answering
GOLDEN_DATASET = [
    {
        "question": "Which leases expire in the next 90 days?",
        "ground_truth": "The leases expiring in the next 90 days are: LG-C317 (Brightline Legal at 875 Riverfront Dr) expiring in 76 days, LG-A192 (Vantage Analytics at 456 Commerce Blvd) expiring in 42 days, and LG-G731 (Coastal Retail Group at 456 Commerce Blvd) expiring in 58 days."
    },
    {
        "question": "Which tenant has the highest concentration risk?",
        "ground_truth": "Vantage Analytics has the highest concentration risk with 50,800 sqft across 3 leases, representing 45% of the total portfolio."
    },
    {
        "question": "Are there any high-risk termination clauses?",
        "ground_truth": "Yes, there are high-risk termination clauses. For example, Vantage Analytics (LG-A192) has a termination right after Year 3 with 12 months notice, and Coastal Retail Group (LG-G731) has a one-time early termination right after Month 24."
    },
    {
        "question": "What is the average base rent psf across all leases?",
        "ground_truth": "The average base rent across the portfolio is $38.40 per sqft."
    },
]

# Cypher execution test questions
CYPHER_QUESTIONS = [
    "How many active leases are in the portfolio?",
    "Which properties are located in Austin, TX?",
    "Find all leases where the tenant is 'Vantage Analytics'."
]


def run():
    logger.info("Initializing Evaluation Pipeline...")
    evaluator = LeaseEvaluator()

    # 1. Evaluate standard RAGAS Metrics
    logger.info(f"Starting Graph-RAG evaluation on {len(GOLDEN_DATASET)} cases...")
    ragas_results = evaluator.evaluate_graph_rag(GOLDEN_DATASET)
    
    # 2. Evaluate Graph-Specific Metric
    logger.info("Starting Cypher generation evaluation...")
    cypher_results = evaluator.evaluate_cypher_accuracy(CYPHER_QUESTIONS)

    # 3. Report
    print("\n" + "="*50)
    print("📋 LEASEGUARD EVALUATION REPORT")
    print("="*50)
    
    print("\n🎯 RAGAS METRICS (Graph-RAG Q&A)")
    print("-" * 30)
    if hasattr(ragas_results, 'scores'):
        # For ragas 0.1.x / 0.2.x returning Result object
        for metric, score in ragas_results.items():
            print(f"{metric.ljust(20)}: {score:.4f}")
    else:
        # Fallback if dictionary
        for metric, score in dict(ragas_results).items():
            print(f"{metric.ljust(20)}: {score:.4f}")

    print("\n🕸️  GRAPH-SPECIFIC METRICS (Text-to-Cypher)")
    print("-" * 30)
    print(f"Total Queries Tested: {cypher_results['total']}")
    print(f"Execution Success:    {cypher_results['successful_execution']}")
    print(f"Execution Failure:    {cypher_results['failed_execution']}")
    print(f"Accuracy Rate:        {cypher_results['execution_rate']:.2%}")

    print("\n" + "="*50)


if __name__ == "__main__":
    run()
