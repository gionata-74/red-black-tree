class Node:
    def __init__(self, key, data, color="red") -> None:
        self.key = key
        self.right = 0
        self.left = 0
        self.parent = 0
        self.data = data
        self.color = color

class RBTree:
    def __init__(self) -> None:
        self.root = 0
        self.nodes = {}
        self.left_most = 0
        self.right_most = 0


# Insertion functions
def rb_insert(tree, key, data):
    if key in tree.nodes:
        raise TypeError("unhashable type")

    new_node = Node(key, data)
    basic_tree_insert(tree, new_node)
    tree.nodes[key] = new_node

    # Update left_most and right_most
    if tree.left_most == 0 or key < tree.left_most:
        tree.left_most = new_node.key
    if tree.right_most == 0 or key > tree.right_most:
        tree.right_most = new_node.key
    
    rb_insert_fixup(tree, new_node)

def basic_tree_insert(tree, new_node):
    if not tree.root:
        new_node.color = "black"
        tree.root = new_node.key
        return
    
    current_node = tree.nodes[tree.root]
    while True:
        if new_node.key < current_node.key:
            if current_node.left:
              current_node = tree.nodes[current_node.left]
            else:
              current_node.left = new_node.key
              new_node.parent = current_node.key
              break
        else:
            if current_node.right:
              current_node = tree.nodes[current_node.right]
            else:
              current_node.right = new_node.key
              new_node.parent = current_node.key
              break


def rb_insert_fixup(tree, new_node):
    while new_node.parent and tree.nodes[new_node.parent].color == "red":
        grand_parent = tree.nodes[tree.nodes[new_node.parent].parent]
        if new_node.parent == grand_parent.right:
            uncle = grand_parent.left
            if uncle and tree.nodes[uncle].color == "red":
                tree.nodes[new_node.parent].color = "black"
                tree.nodes[uncle].color = "black"
                grand_parent.color = "red"
                new_node = grand_parent
            else:
                if new_node.key == tree.nodes[new_node.parent].left:
                    new_node = tree.nodes[new_node.parent]
                    right_rotate(tree, new_node)
                tree.nodes[new_node.parent].color = "black"
                grand_parent.color = "red"
                left_rotate(tree, grand_parent)
        else:
            uncle = grand_parent.right
            if uncle and tree.nodes[uncle].color == "red":
                tree.nodes[new_node.parent].color = "black"
                tree.nodes[uncle].color = "black"
                grand_parent.color = "red"
                new_node = grand_parent
            else:
                if new_node.key == tree.nodes[new_node.parent].right:
                    new_node = tree.nodes[new_node.parent]
                    left_rotate(tree, new_node)
                tree.nodes[new_node.parent].color = "black"
                grand_parent.color = "red"
                right_rotate(tree, grand_parent)
        if new_node == tree.nodes[tree.root]:
            break
    tree.nodes[tree.root].color = "black"

def left_rotate(tree, node):
    if not node.right:
        return
    y = tree.nodes[node.right]
    node.right = y.left
    if y.left:
        tree.nodes[y.left].parent = node.key
    y.parent = node.parent
    if not node.parent:
        tree.root = y.key
    elif node.key == tree.nodes[node.parent].left:
        tree.nodes[node.parent].left = y.key
    else:
        tree.nodes[node.parent].right = y.key
    y.left = node.key
    node.parent = y.key

def right_rotate(tree, node):
    if not node.left:
        return
    y = tree.nodes[node.left]
    node.left = y.right
    if y.right:
        tree.nodes[y.right].parent = node.key
    y.parent = node.parent
    if not node.parent:
        tree.root = y.key
    elif node.key == tree.nodes[node.parent].right:
        tree.nodes[node.parent].right = y.key
    else:
        tree.nodes[node.parent].left = y.key
    y.right = node.key
    node.parent = y.key


def display_tree(btree):
    def display_tree_helper(node_key, indent, branch):
        if node_key != 0:
            node = btree.nodes[node_key]
            display_tree_helper(node.right, indent + "    ", "/")
            print(indent + branch + str(node.key))
            display_tree_helper(node.left, indent + "    ", "\\")

    display_tree_helper(btree.root, "", "")

my_tree = RBTree()

import random

my_list = [i for i in range(1, 20)]
random.shuffle(my_list)

for i in my_list:
  rb_insert(my_tree, i, {})

display_tree(my_tree)
print("END")