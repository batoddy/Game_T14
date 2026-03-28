class TreeNode:
    def __init__(self, state, move=None, parent=None, depth=0):
        self.state = state
        self.move = move
        self.parent = parent
        self.depth = depth
        self.children = []
        self.value = None

    def create_child(self, state, move=None, parent=None, depth=0):
        child = TreeNode(state, move, parent, depth)
        self.children.append(child)
        return child
