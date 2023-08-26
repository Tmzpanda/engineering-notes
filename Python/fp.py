# map
def findLength(nums1: List[int], nums2: List[int]) -> int:
    m, n = len(nums1), len(nums2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    
    for i in range(1, m+1):
        for j in range(1, n+1):
            if nums1[i-1] == nums2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            
    return max(map(max, dp))  # map
  
# filter
def findAndReplacePattern(words: List[str], pattern: str) -> List[str]:
    def match(word):
        charToWord = {}
        wordSet = set()

        for c, w in zip(pattern, word):
            if c in charToWord and charToWord[c] != w: 
                return False
            if c not in charToWord and w in wordSet:
                return False

            charToWord[c] = w
            wordSet.add(w)

        return True

    return filter(match, words)  # filter
  
# reduce
def sequenceReconstruction(nums: List[int], sequences: List[List[int]]) -> bool:
    if set(reduce(lambda x, y: x + y, sequences)) != set(nums):  # reduce   
        return False
  
    n = len(nums)
    graph = defaultdict(list)
    in_degrees = defaultdict(int)
    for seq in sequences:
        for f, t in zip(seq, seq[1:]):  
            graph[f].append(t)
            in_degrees[t] += 1
  
    queue = [node for node in nums if in_degrees[node] == 0]
    order = []
    while queue:
        if len(queue) != 1:
            return False
        node = queue.pop()
        order.append(node)
        for next_node in graph[node]:
            in_degrees[next_node] -= 1
            if in_degrees[next_node] == 0:
                queue.append(next_node)
  
    return nums == order

