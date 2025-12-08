# test_evaluate.py

from evaluation import evaluate_answer

if __name__ == "__main__":
    qid = "q1"  

    print("Question:")
    result = evaluate_answer(qid, """
Supervised learning uses labeled data and is used for classification and regression. 
Unsupervised learning uses unlabeled data and finds patterns such as clustering 
and dimensionality reduction.
""")

    print(result["question"])
    print("\nTotal Score:", result["total_score"])
    print("Keyword Score:", result["keyword_score"])
    print("Length Score:", result["length_score"])
    print("\nFeedback:", result["feedback"])
    print("\nIdeal Answer:\n", result["ideal_answer"])
    print("\nMissing keywords:", result["missing_keywords"])
