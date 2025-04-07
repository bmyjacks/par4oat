import logging


class GrammarParser:
    def __init__(self, grammar_file_path):
        self.grammar_file = grammar_file_path
        self.rule = {}

    def parse(self):
        try:
            with open(self.grammar_file, 'r') as f:
                lines = f.readlines()
        except Exception as err:
            logging.error("Failed to read input file: %s", err)
            exit(1)

        # logging.info("Starting Grammar Parser")
        for line in lines:
            line = line.strip()
            if not line or "::=" not in line:
                continue

            left, right = line.split("::=")
            left = left.strip()
            right = right.strip().split()

            if left in self.rule:
                self.rule[left].append(right)
            else:
                self.rule[left] = [right]

        # logging.info("Ending Grammar Parser\n")
