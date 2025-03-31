import homework9

m = homework9.NgramModel(1)
m.update("a b c d")
m.update("a b a b")
print(m.perplexity("a b"))

# m = homework9.create_ngram_model(1, "/Users/briannahuang/Desktop/cis 521/language_models/frankenstein.txt")
# print(m.random_text(15))