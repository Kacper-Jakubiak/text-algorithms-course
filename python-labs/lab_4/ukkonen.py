class Node:
    def __init__(self, start = -1, end = None):
        self.children = {}
        self.suffix_link = None
        self.start = start
        self.end = end
        self.index = -1


class SuffixTree:
    def __init__(self, text: str):
        self.text = text + "$"
        self.root = Node()
        self.root.suffix_link = self.root
        self.active_node = self.root
        self.active_edge = -1
        self.active_length = 0
        self.remainder = 0
        self.leaf_end = -1  # Wspólny wskaźnik końca (technika wskaźnika końcowego)
        self.last_new_node = None
        self.node_count = 1  # Rozpoczynamy od korzenia
        self.size = 0        # Liczba węzłów w drzewie
        self.build_tree()

    def edge_length(self, node):
        return (node.end[0] if node.end else self.leaf_end) - node.start + 1

    def walk_down(self, next_node):
        # Technika skip/count: chodzimy po całych krawędziach
        if self.active_length >= self.edge_length(next_node):
            self.active_edge += self.edge_length(next_node)
            self.active_length -= self.edge_length(next_node)
            self.active_node = next_node
            return True
        return False

    def build_tree(self):
        self.leaf_end = -1
        self.root.end = [-1]
        for pos in range(len(self.text)):
            self.extend(pos)

    def extend(self, pos):
        self.leaf_end = pos
        self.remainder += 1
        self.last_new_node = None

        while self.remainder > 0:
            if self.active_length == 0:
                self.active_edge = pos

            ch = self.text[self.active_edge]
            if ch not in self.active_node.children:
                # Tworzymy nowy liść
                leaf = Node(pos, [self.leaf_end])
                leaf.index = pos - self.remainder + 1
                self.active_node.children[ch] = leaf
                self.size += 1  # Zwiększamy liczbę węzłów

                if self.last_new_node:
                    self.last_new_node.suffix_link = self.active_node
                    self.last_new_node = None
            else:
                next_node = self.active_node.children[ch]
                if self.walk_down(next_node):  # Skip/count
                    continue
                if self.text[next_node.start + self.active_length] == self.text[pos]:
                    if self.last_new_node:
                        self.last_new_node.suffix_link = self.active_node
                        self.last_new_node = None
                    self.active_length += 1
                    break
                split_end = [next_node.start + self.active_length - 1]
                split = Node(next_node.start, split_end)
                self.active_node.children[ch] = split
                self.size += 1

                leaf = Node(pos, [self.leaf_end])
                leaf.index = pos - self.remainder + 1
                split.children[self.text[pos]] = leaf
                self.size += 1

                next_node.start += self.active_length
                split.children[self.text[next_node.start]] = next_node

                if self.last_new_node:
                    self.last_new_node.suffix_link = split
                self.last_new_node = split

            self.remainder -= 1
            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = pos - self.remainder + 1
            elif self.active_node != self.root:
                self.active_node = self.active_node.suffix_link

    def find_pattern(self, pattern: str) -> list[int]:
        node = self.root
        i = 0
        while i < len(pattern):
            if pattern[i] not in node.children:
                return []
            child = node.children[pattern[i]]
            label_len = self.edge_length(child)
            j = 0
            while j < label_len and i < len(pattern):
                if self.text[child.start + j] != pattern[i]:
                    return []
                i += 1
                j += 1
            if j < label_len:
                return []
            node = child

        results = []
        self.collect_leaves(node, results)
        return results

    def collect_leaves(self, node, results):
        if node.index != -1:
            results.append(node.index)
        for child in node.children.values():
            self.collect_leaves(child, results)


if __name__ == '__main__':
    txt = "ananas"
    tree = SuffixTree(txt)
    pattern = "ana"
    print("Wystąpienia:", tree.find_pattern(pattern))  # [0, 2]
    print("Liczba węzłów:", tree.size)
