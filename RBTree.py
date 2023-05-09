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

def find_left_most(tree, node):
    while node.left:
        node = tree.nodes[node.left]
    return node

def find_right_most(tree, node):
    while node.right:
        node = tree.nodes[node.right]
    return node


def rb_remove(tree, key):
    if key not in tree.nodes:
        raise TypeError("key not found in the tree")
    node_to_remove = tree.nodes[key]

    y = node_to_remove
    y_original_color = y.color
    x = None

    if not node_to_remove.left:
        x = tree.nodes.get(node_to_remove.right)
        rb_transplant(tree, node_to_remove, x)
    elif not node_to_remove.right:
        x = tree.nodes.get(node_to_remove.left)
        rb_transplant(tree, node_to_remove, x)
    else:
        y = find_left_most(tree, tree.nodes[node_to_remove.right])
        y_original_color = y.color
        x = tree.nodes.get(y.right)

        if y.parent != node_to_remove.key:
            rb_transplant(tree, y, x)
            y.right = node_to_remove.right
            tree.nodes[y.right].parent = y.key

        rb_transplant(tree, node_to_remove, y)
        y.left = node_to_remove.left
        tree.nodes[y.left].parent = y.key
        y.color = node_to_remove.color

    # Call rb_delete_fixup only if x exists and y_original_color is black
    if x and y_original_color == "black":
        rb_delete_fixup(tree, x.key)

    del tree.nodes[key]
    # Update left_most and right_most pointers if necessary
    if tree.left_most == key:
        tree.left_most = find_left_most(tree, tree.nodes[tree.root]).key if tree.root else 0
    if tree.right_most == key:
        tree.right_most = find_right_most(tree, tree.nodes[tree.root]).key if tree.root else 0


def rb_transplant(tree, node_u, node_v):
    if not node_u.parent:
        tree.root = node_v.key if node_v else 0
    elif node_u.key == tree.nodes[node_u.parent].left:
        tree.nodes[node_u.parent].left = node_v.key if node_v else 0
    else:
        tree.nodes[node_u.parent].right = node_v.key if node_v else 0
    if node_v:
        node_v.parent = node_u.parent


def rb_delete_fixup(tree, node):
    while node != tree.root and tree.nodes[node].color == "black":
        if node == tree.nodes[tree.nodes[node].parent].left:
            sibling = tree.nodes[node].parent.right
            if tree.nodes[sibling].color == "red":
                tree.nodes[sibling].color = "black"
                tree.nodes[tree.nodes[node].parent].color = "red"
                left_rotate(tree, tree.nodes[node].parent)
                sibling = tree.nodes[tree.nodes[node].parent].right
            if tree.nodes[sibling].left and tree.nodes[sibling].right and tree.nodes[sibling.left].color == "black" and tree.nodes[sibling.right].color == "black":
                tree.nodes[sibling].color = "red"
                node = tree.nodes[node].parent
            else:
                if tree.nodes[sibling.right].color == "black":
                    tree.nodes[sibling.left].color = "black"
                    tree.nodes[sibling].color = "red"
                    right_rotate(tree, sibling)
                    sibling = tree.nodes[tree.nodes[node].parent].right
                tree.nodes[sibling].color = tree.nodes[tree.nodes[node].parent].color
                tree.nodes[tree.nodes[node].parent].color = "black"
                tree.nodes[sibling.right].color = "black"
                left_rotate(tree, tree.nodes[node].parent)
                node = tree.root
        else:
            sibling = tree.nodes[node].parent.left
            if tree.nodes[sibling].color == "red":
                tree.nodes[sibling].color = "black"
                tree.nodes[tree.nodes[node].parent].color = "red"
                right_rotate(tree, tree.nodes[node].parent)
                sibling = tree.nodes[tree.nodes[node].parent].left
            if tree.nodes[sibling].right and tree.nodes[sibling].left and tree.nodes[sibling.right].color == "black" and tree.nodes[sibling.left].color == "black":
                tree.nodes[sibling].color = "red"
                node = tree.nodes[node].parent
            else:
                if tree.nodes[sibling.left].color == "black":
                    tree.nodes[sibling.right].color = "black"
                    tree.nodes[sibling].color = "red"
                    left_rotate(tree, sibling)
                    sibling = tree.nodes[tree.nodes[node].parent].left
                tree.nodes[sibling].color = tree.nodes[tree.nodes[node].parent].color
                tree.nodes[tree.nodes[node].parent].color = "black"
                tree.nodes[sibling.left].color = "black"
                right_rotate(tree, tree.nodes[node].parent)
                node = tree.root
    tree.nodes[node].color = "black"


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

my_list = [i for i in range(1, 100)]
random.shuffle(my_list)

for i in my_list:
  rb_insert(my_tree, i, {})
display_tree(my_tree)
num = random.randint(40, 50)
rb_remove(my_tree, num)
print("\n\n\n")
display_tree(my_tree)

print(num, "END")