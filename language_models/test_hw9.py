import homework9
import random

m = homework9.NgramModel(1)
m.update("a b c d")
m.update("a b a b")
random.seed(1)
print(m.random_text(13))
# print(m.perplexity("a b"))

# m = homework9.create_ngram_model(1, "/Users/briannahuang/Desktop/cis 521/language_models/frankenstein.txt")
# print(m.random_text(15))