class ParseTable:
    def __init__(self, ff_sets):
        self.table = {}
        self.ff_sets = ff_sets
        self.start_symbol = list(ff_sets.rule.keys())[0]

    def is_terminal(self, symbol):
        return symbol not in self.ff_sets.rule

    def compute_table(self):
        def get_first_set(production):
            result = set()

            for symbol in production:
                if self.ff_sets.is_terminal(symbol):
                    result.add(symbol)
                    break

                for s in self.ff_sets.first.get(symbol):
                    if s != "''":
                        result.add(s)

                if not self.ff_sets.is_nullable(symbol):
                    break

            return result

        for non_terminal in self.ff_sets.rule:
            self.table[non_terminal] = {}

        for non_terminal, productions in self.ff_sets.rule.items():
            for production in productions:
                first_set = get_first_set(production)
                for terminal in first_set:
                    if terminal != "''":
                        self.table[non_terminal][terminal] = production

                if "''" in first_set:
                    for terminal in self.ff_sets.follow[non_terminal]:
                        self.table[non_terminal][terminal] = production

    def print_table(self):
        print("Parsing Table:")
        for non_terminal, productions in self.table.items():
            print(f"{non_terminal}:")
            for terminal, production in productions.items():
                print(f"  {terminal} -> {production}")
