############################################################
# CIS 521: Homework 8
############################################################

import math
import random
from collections import defaultdict
import string
student_name = "Brianna Huang"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

############################################################
# Section 1: Ngram Models
############################################################


def tokenize(text):
    tokens = []
    curr = ""
    for char in text:
        if char.isspace():
            if curr:
                tokens.append(curr)
                curr = ""
        elif char in string.punctuation:
            if curr:
                tokens.append(curr)
                curr = ""
            tokens.append(char)
        else:
            curr += char
    if curr:
        tokens.append(curr)
    return tokens


def ngrams(n, tokens):
    tokens = ["<START>"] * (n - 1) + tokens + ["<END>"]
    n_grams = []
    for i in range(len(tokens) - (n - 1)):
        context = tuple(tokens[i: i + n - 1])
        token = tokens[i + n - 1]
        n_grams.append((context, token))
    return n_grams


class NgramModel(object):

    def __init__(self, n):
        self.n = n
        self.contexts = defaultdict(lambda: defaultdict(int))
        self.counts = defaultdict(int)

    def update(self, sentence):
        tokens = tokenize(sentence)
        n_grams = ngrams(self.n, tokens)
        for context, token in n_grams:
            self.contexts[context][token] += 1
            self.counts[context] += 1

    def prob(self, context, token):
        if self.counts[context] == 0:
            return 0
        return self.contexts[context][token] / self.counts[context]

    def random_token(self, context):
        tokens = sorted(self.contexts[context].keys())
        total_prob = 0
        r = random.random()

        for token in tokens:
            total_prob += self.prob(context, token)
            if r < total_prob:
                return token

    def random_text(self, token_count):
        context = ("<START>",) * (self.n - 1) if self.n > 1 else ()
        tokens = []
        for i in range(token_count):
            token = self.random_token(context)
            tokens.append(token)
            if token == "<END>":
                # reset to starting context
                context = ("<START>",) * (self.n - 1) if self.n > 1 else ()
            else:
                context = context[1:] + (token,) if self.n > 1 else ()
        return " ".join(tokens)

    def perplexity(self, sentence):
        tokens = tokenize(sentence)
        n_grams = ngrams(self.n, tokens)
        num_tokens = len(n_grams)
        total_prob = 0
        for context, token in n_grams:
            prob = self.prob(context, token)
            total_prob += math.log(prob)
        return math.exp(-total_prob/num_tokens)


def create_ngram_model(n, path):
    m = NgramModel(n)
    with open(path, "r", encoding='utf-8') as file:
        for line in file:
            seq = line.strip()
            m.update(seq)
    return m


############################################################
# Section 2: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
10
"""

feedback_question_2 = """
Wrapping my head around the context and count dictionaries was
a bit challenging, as well as the implementing perplexity in
log-space then re-exponentiating.
"""

feedback_question_3 = """
I liked seeing the randomly generated frankenstein texts!
I wouldn't change anything.
"""
