import argparse
import logging

import ff_sets
import grammar_parser
import parse4oat
import parse_table

if __name__ == '__main__':
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Argument parser
    arg_parser = argparse.ArgumentParser(prog="par4oat")
    arg_parser.add_argument('tokens_file', type=str, help="Path to the source file")
    arg_parser.add_argument('--emit', type=str, choices=['sets', 'parse_table', 'dot'], nargs='+', default=[],
                            help="Emit sets, parse table, or dot file")

    # Parse arguments
    args = arg_parser.parse_args()

    grammar_par_obj = grammar_parser.GrammarParser('grammar/grammar.txt')
    grammar_par_obj.parse()

    ff_sets_obj = ff_sets.FFSets(grammar_par_obj)
    ff_sets_obj.compute_nullable()
    ff_sets_obj.compute_first()
    ff_sets_obj.compute_follow()
    if 'sets' in args.emit:
        ff_sets_obj.print_sets()

    parse_table_obj = parse_table.ParseTable(ff_sets_obj)
    parse_table_obj.compute_table()
    if 'parse_table' in args.emit:
        parse_table_obj.print_table()

    parse4oat_obj = parse4oat.Parse4Oat(parse_table_obj)

    with open(args.tokens_file, 'r') as file:
        input_string = file.read().strip()

    parse4oat_obj.parse(input_string, enable_dot='dot' in args.emit)
