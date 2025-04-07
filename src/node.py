import uuid


class Node:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.father = None
        self.id = uuid.uuid4()

    def add_child(self, child_node):
        self.children.insert(0, child_node)
        child_node.father = self

    def get_father(self):
        return self.father

    def to_dot(self):
        dot_representation = f'"{self.id}" [label="{self.data}"];\n'
        for child in self.children:
            dot_representation += f'"{self.id}" -> "{child.id}";\n'
            dot_representation += child.to_dot()
        return dot_representation
