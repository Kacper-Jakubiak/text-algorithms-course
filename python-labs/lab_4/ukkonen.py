class SuffixTreeNode:
    def __init__(self):
        # Initialize children list to store child nodes for each ASCII character
        self.children = [None] * 256  # Assuming ASCII characters
        # Suffix link for suffix tree construction
        self.suffix_link = None
        # Start index of the substring represented by the edge leading to this node
        self.start = 0
        # End index (as a list to facilitate updates) of the substring represented by the edge leading to this node
        self.end = [0]
        # Index of the suffix represented by the path from root to this node
        self.suffix_index = -1


class SuffixTree:
    def new_node(self, start, end):
        global count
        count += 1
        node = SuffixTreeNode()
        # Set suffix link to root initially
        node.suffix_link = root
        node.start = start
        node.end = end
        node.suffix_index = -1
        return node

    # Function to calculate the length of an edge represented by a node
    def edge_length(self, n):
        return n.end[0] - n.start + 1

    # Function to handle the walk down in suffix tree construction
    def walk_down(self, curr_node):
        global active_length, active_edge, remaining_suffix_count, active_node
        if active_length >= self.edge_length(curr_node):
            # Update active edge and active length to walk down the tree
            active_edge = ord(text[size - remaining_suffix_count + 1]) - ord(' ')
            active_length -= self.edge_length(curr_node)
            active_node = curr_node
            return True
        return False

    # Function to extend the suffix tree for a given position in the text
    def extend_suffix_tree(self, pos):
        global leaf_end, remaining_suffix_count, last_new_node, active_node, active_length, active_edge
        leaf_end = pos
        remaining_suffix_count += 1
        last_new_node = None

        while remaining_suffix_count > 0:
            if active_length == 0:
                # If active length is zero, set active edge for the current position
                active_edge = ord(text[pos]) - ord(' ')

            if not active_node.children[active_edge]:
                # If active edge has no child, create a new node
                active_node.children[active_edge] = self.new_node(pos, [leaf_end])

                if last_new_node:
                    # If there was a previously created node, update its suffix link
                    last_new_node.suffix_link = active_node
                    last_new_node = None
            else:
                next_node = active_node.children[active_edge]
                if self.walk_down(next_node):
                    continue

                if text[next_node.start + active_length] == text[pos]:
                    if last_new_node and active_node != root:
                        last_new_node.suffix_link = active_node
                        last_new_node = None
                    active_length += 1
                    break

                split_end = [next_node.start + active_length - 1]
                split_node = self.new_node(next_node.start, split_end)
                active_node.children[active_edge] = split_node
                split_node.children[ord(text[pos]) - ord(' ')] = self.new_node(pos, [leaf_end])
                next_node.start += active_length
                split_node.children[active_edge] = next_node

                if last_new_node:
                    last_new_node.suffix_link = split_node

                last_new_node = split_node

            remaining_suffix_count -= 1
            if active_node == root and active_length > 0:
                active_length -= 1
                active_edge = ord(text[pos - remaining_suffix_count + 1]) - ord(' ')
            elif active_node != root:
                active_node = active_node.suffix_link

    # Function to print the substring of the text given its start and end indices
    def print_string(self, i, j):
        output = ""
        for k in range(i, j + 1):
            output += text[k]
        print(output)

    # Function to set suffix indices using depth-first search (DFS)
    def set_suffix_index_by_dfs(self, n, label_height):
        if not n:
            return

        if n.start != -1:
            # Print the substring represented by the edge leading to this node
            self.print_string(n.start, n.end[0])

        leaf = 1
        for i in range(256):
            if n.children[i]:
                if leaf == 1 and n.start != -1:
                    # If this node has children and it's not a leaf node, print its suffix index
                    print(" [" + str(n.suffix_index) + "]")

                leaf = 0
                self.set_suffix_index_by_dfs(
                    n.children[i],
                    label_height + self.edge_length(n.children[i]))

        if leaf == 1:
            # If this is a leaf node, set its suffix index
            n.suffix_index = size - label_height
            print(" [" + str(n.suffix_index) + "]")

    # Function to free the memory allocated for the suffix tree using post-order traversal
    def free_suffix_tree_by_post_order(self, n):
        if not n:
            return

        for i in range(256):
            if n.children[i]:
                self.free_suffix_tree_by_post_order(n.children[i])

        if n.suffix_index == -1:
            # If this node doesn't represent any suffix, free its memory
            n.end = None

    # Function to build the suffix tree for the given text
    def build_suffix_tree(self):
        global size, root_end, root, active_node, remaining_suffix_count, active_length, active_edge
        size = len(text)
        root_end = [None]
        root_end[0] = -1

        root = self.new_node(-1, root_end)

        active_node = root
        remaining_suffix_count = 0
        active_length = 0
        active_edge = -1

        for i in range(size):
            # Extend the suffix tree for each position in the text
            self.extend_suffix_tree(i)
        label_height = 0
        # Set suffix indices using depth-first search (DFS)
        self.set_suffix_index_by_dfs(root, label_height)

        # Free the memory allocated for the suffix tree using post-order traversal
        self.free_suffix_tree_by_post_order(root)


if __name__ == "__main__":
    text = list("abbc")
    root = None
    last_new_node = None
    active_node = None
    count = 0
    active_edge = -1
    active_length = 0
    remaining_suffix_count = 0
    leaf_end = -1
    root_end = None
    split_end = None
    size = -1
    t = SuffixTree()
    t.build_suffix_tree()
    print("Number of nodes in suffix tree are", count)
