def is_code_block(s: str) -> bool:
    return s.startswith("<code>") and s.endswith("</code>")

def get_similarity_matrix(quiz: list) -> list:
    """Returns a matrix of floats with similarities scores.
    
    A score between two lists of questions is defined as the fraction
    of questions that are present on both lists. Two questions are
    equal if they have the same id.
    
    Notice that this scores are meaningful only when computed between
    lists with the same number of questions."""
    n = len(quiz)
    if n == 0:
        return []
    m = len(quiz[0])
    matrix = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            a = set([q.id for q in quiz[i]])
            b = set([q.id for q in quiz[j]])
            matrix[i][j] = len(a.intersection(b)) / m
    return matrix
            

