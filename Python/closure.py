def preorderTraversal(root: TreeNode) -> List[int]:
    res = []
    def dfs(node):
        if node is None:
            return
        res.append(node.val)
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return res
