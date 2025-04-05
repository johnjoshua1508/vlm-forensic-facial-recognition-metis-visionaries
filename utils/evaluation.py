import numpy as np

def precision_at_k(retrieved, ground_truth, k):
    """
    Calculate precision@k
    
    Args:
        retrieved: List of retrieved items
        ground_truth: Set of relevant items
        k: Number of items to consider
        
    Returns:
        float: Precision@k value
    """
    retrieved_k = retrieved[:k]
    relevant = sum(1 for r in retrieved_k if r in ground_truth)
    return relevant / k if k > 0 else 0

def recall_at_k(retrieved, ground_truth, k):
    """
    Calculate recall@k
    
    Args:
        retrieved: List of retrieved items
        ground_truth: Set of relevant items
        k: Number of items to consider
        
    Returns:
        float: Recall@k value
    """
    retrieved_k = retrieved[:k]
    relevant = sum(1 for r in retrieved_k if r in ground_truth)
    return relevant / len(ground_truth) if len(ground_truth) > 0 else 0

def average_precision(retrieved, ground_truth):
    """
    Calculate average precision
    
    Args:
        retrieved: List of retrieved items
        ground_truth: Set of relevant items
        
    Returns:
        float: Average precision value
    """
    if len(ground_truth) == 0:
        return 0
    
    ap = 0.0
    relevant = 0
    
    for i, r in enumerate(retrieved, start=1):
        if r in ground_truth:
            relevant += 1
            ap += relevant / i
    
    return ap / len(ground_truth)

def mean_average_precision(queries):
    """
    Calculate mean average precision
    
    Args:
        queries: List of (retrieved, ground_truth) tuples
        
    Returns:
        float: Mean average precision value
    """
    if not queries:
        return 0
    
    aps = [average_precision(retrieved, ground_truth) for retrieved, ground_truth in queries]
    return np.mean(aps)

