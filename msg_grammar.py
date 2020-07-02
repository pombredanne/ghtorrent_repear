from gingerit.gingerit import GingerIt
text = "I would like to buy one apples"
ginger_parser = GingerIt()
ginger_grammar_results = ginger_parser.parse(text)
ginger_corrections = ginger_grammar_results['corrections']
print("\nNumber of grammar issues found with Ginger: " + str(len(ginger_corrections)) + "\n")