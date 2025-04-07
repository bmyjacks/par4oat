import logging
import grammar_parser
import ff_sets
import parse_table
import parse4oat

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    grammar_par_obj = grammar_parser.GrammarParser("grammar/grammar.txt")
    grammar_par_obj.parse()

    ff_sets_obj = ff_sets.FFSets(grammar_par_obj)
    ff_sets_obj.compute_nullable()
    ff_sets_obj.compute_first()
    ff_sets_obj.compute_follow()

    parse_table_obj = parse_table.ParseTable(ff_sets_obj)
    parse_table_obj.compute_table()
    parse_table_obj.print_table()

    parse4oat_obj = parse4oat.Parse4Oat(parse_table_obj)



