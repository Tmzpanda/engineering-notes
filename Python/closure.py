# 144. Binary Tree Preorder Traversal
def preorderTraversal(root: TreeNode) -> List[int]:

    def dfs(node):
        if node is None:
            return
          
        res.append(node.val)  # closure
        dfs(node.left)
        dfs(node.right)

    res = []
    dfs(root)
    
    return res
  
  
# 90. Subsets II 
def subsets(nums: List[int]) -> List[List[int]]:

    def dfs(index, subset):
        res.append(list(subset))  # deep copy
        
        for i in range(index, n):
            if i != 0 and nums[i] == nums[i - 1] and i != index:    # deduplicate
                  continue
                
            subset.append(nums[i])
            dfs(i + 1, subset)
            subset.pop()

    nums = sorted(nums)
    n = len(nums)
    res = []
    dfs(0, [])

    return res
  
  
