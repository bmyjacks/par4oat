class FFSets:
    def __init__(self, grammar_parser):
        self.rule = grammar_parser.rule
        self.nullable = {}
        self.first = {}
        self.follow = {}

    def is_nullable(self, symbol):
        return symbol in self.nullable or symbol == "''"

    def is_terminal(self, symbol):
        return symbol not in self.rule

    def compute_nullable(self):
        for non_terminal, productions in self.rule.items():

            for production in productions:
                all_nullable = True
                for symbol in production:
                    if not self.is_nullable(symbol):
                        all_nullable = False
                        break

                if all_nullable:
                    self.nullable[non_terminal] = True

    def compute_first(self):
        def add_to_first(symbol, non_terminal):
            if symbol not in self.first[non_terminal]:
                self.first[non_terminal].add(symbol)
                return True
            return False

        for non_terminal in self.rule:
            self.first[non_terminal] = set()

        changed = True
        while changed:
            changed = False
            for non_terminal, productions in self.rule.items():
                for production in productions:
                    if production[0] == "''":
                        if add_to_first("''", non_terminal):
                            changed = True
                        continue

                    for symbol in production:
                        if self.is_terminal(symbol):
                            if add_to_first(symbol, non_terminal):
                                changed = True
                            break
                        else:
                            for s in self.first.get(symbol):
                                if s == "''":
                                    continue
                                if add_to_first(s, non_terminal):
                                    changed = True

                            if changed or not self.is_nullable(symbol):
                                break

            if not changed:
                break

    def compute_follow(self):
        def add_to_follow(symbol, non_terminal):
            if symbol not in self.follow[non_terminal]:
                self.follow[non_terminal].add(symbol)
                return True
            return False

        for non_terminal in self.rule:
            self.follow[non_terminal] = set()

        self.follow[list(self.rule.keys())[0]].add('$')

        changed = True
        while changed:
            changed = False

            for non_terminal, productions in self.rule.items():
                for production in productions:
                    for i, symbol in enumerate(production):
                        if self.is_terminal(symbol):
                            continue

                        if i + 1 < len(production):
                            next_symbol = production[i + 1]
                            if self.is_terminal(next_symbol):
                                if add_to_follow(next_symbol, symbol):
                                    changed = True
                            else:
                                for s in self.first.get(next_symbol):
                                    if s == "''":
                                        continue
                                    if add_to_follow(s, symbol):
                                        changed = True

                                if self.is_nullable(next_symbol):
                                    for s in self.follow.get(non_terminal):
                                        if add_to_follow(s, symbol):
                                            changed = True
                        else:
                            for s in self.follow.get(non_terminal):
                                if add_to_follow(s, symbol):
                                    changed = True

            if not changed:
                break
