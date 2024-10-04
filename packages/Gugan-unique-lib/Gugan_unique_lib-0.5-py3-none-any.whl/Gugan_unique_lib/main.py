def hello():
    print('This is Gugan, welcome to my Library...')
def addition():
    a = int(input("Enter value for a :"))
    b = int(input("Enter value for b :"))
    print(a+b)

class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    # Get the height of the node
    def get_height(self, node):
        if not node:
            return 0
        return node.height

    # Get balance factor of the node
    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    # Right rotate the subtree rooted with y
    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    # Left rotate the subtree rooted with x
    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    # Insert node into the AVL tree
    def insert(self, root, key):
        if not root:
            return Node(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        # Left Left Case
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)
        
        # Right Right Case
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        # Left Right Case
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left Case
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    # A utility function to print the AVL tree
    def print_tree(self, node, level=0, prefix="Root: "):
        if node is not None:
            print(" " * (level * 4) + prefix + str(node.key))
            if node.left: 
                self.print_tree(node.left, level + 1, prefix="L--- ")
            if node.right:
                self.print_tree(node.right, level + 1, prefix="R--- ")

# Function to build and display the AVL tree from a user input
def display_avl_tree_from_input():
    user_input = input("Enter the list of nodes (separated by commas): ")
    node_list = list(map(int, user_input.split(',')))  # Convert input into list of integers
    
    avl = AVLTree()
    root = None
    for key in node_list:
        root = avl.insert(root, key)
    
    print("\nAVL Tree structure:")
    avl.print_tree(root)

