from node import Node


class Parse4Oat:
    def __init__(self, parse_table):
        self.parse_table = parse_table
        self.cst = Node(self.parse_table.start_symbol)

    def is_terminal(self, symbol):
        return self.parse_table.is_terminal(symbol)

    def parse(self, tokens):
        stack = [(self.parse_table.start_symbol, self.cst), ('$', None)]

        tokens = tokens.split() + ['$']

        while stack[0] != ('$', None):
            stack_top, current_node = stack.pop(0)
            current_token = tokens[0]

            if self.is_terminal(stack_top):
                # Terminal symbol
                if stack_top == current_token:
                    # new_node = Node(current_token)
                    # current_node.add_child(new_node)
                    tokens.pop(0)
            else:
                # Non-terminal symbol
                production = self.parse_table.table.get(stack_top, dict()).get(current_token)
                if production is None:
                    print(f"Error: No production for {stack_top} with input {current_token}")
                    return

                if production[0] != "''":
                    for symbol in reversed(production):
                        new_node = Node(symbol)
                        current_node.add_child(new_node)
                        stack.insert(0, (symbol, new_node))

        if tokens[0] == '$':
            print("Parsing successful!")
        else:
            print("Error: Input string not fully consumed.")

        dot_representation = self.cst.to_dot()
        with open("output.dot", "w") as f:
            f.write("digraph G {\n")
            f.write(dot_representation)
            f.write("}\n")

        self.cst.print_tree()
