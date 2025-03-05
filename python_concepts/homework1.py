import numpy as np
import nltk

############################################################
# CIS 521: Homework 1
############################################################

student_name = "Brianna Huang"

# This is where your grade report will be sent.
student_email = "bhua@seas.upenn.edu"

############################################################
# Section 1: Python Concepts
############################################################

python_concepts_question_1 = """
Python is strongly typed, as operations that are not suitable for a
certain variable will cause errors instead of Python trying to execute
it anyway. For example, Python won't allow addition of a string and an
integer without type casting one of them first ("2" + 2 will raise an
error). However, it is also dynamically typed since you don't need to
declare the type of variable at initialization. It also allows you to
change the type of a variable through reassignment or casting (x=1;
x="abc" is allowed).
"""

python_concepts_question_2 = """
Dictionary keys must be immutable. In this example, they keys are arrays
and do not satisfy this condition. Thus, we can change the keys to be
tuples instead, since they are an immutable type.
"""

python_concepts_question_3 = """
The latter function is significantly faster for larger inputs, since it
uses the join method which is optimized and only creates a new string
once, rather than the += operation which makes a copy the string each
time it is used.
"""

############################################################
# Section 2: Working with Lists
############################################################


def extract_and_apply(lst, p, f):
    return [f(x) for x in lst if p(x)]


def concatenate(seqs):
    return [s for seq in seqs for s in seq]


def transpose(matrix):
    h = len(matrix)
    w = len(matrix[0])
    return [[matrix[i][j] for i in range(h)] for j in range(w)]

############################################################
# Section 3: Sequence Slicing
############################################################


def copy(seq):
    return seq[0:]


def all_but_last(seq):
    if len(seq) < 1:
        return seq
    return seq[0:len(seq)-1]


def every_other(seq):
    return seq[0:len(seq):2]

############################################################
# Section 4: Combinatorial Algorithms
############################################################


def prefixes(seq):
    for i in range(len(seq)+1):
        yield seq[0:i]


def suffixes(seq):
    for i in range(len(seq)+1):
        yield seq[i:len(seq)]


def slices(seq):
    for i in range(len(seq)):
        for j in range(i+1, len(seq)+1):
            yield seq[i:j]

############################################################
# Section 5: Text Processing
############################################################


def normalize(text):
    words = [w.lower() for w in text.split()]
    words = " ".join(words)
    return words


def no_vowels(text):
    for v in ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']:
        text = text.replace(v, '')
    return text


def digits_to_words(text):
    nums = ['zero', 'one', 'two', 'three', 'four',
            'five', 'six', 'seven', 'eight', 'nine']
    num_list = [nums[int(n)] for n in text if n.isdigit()]
    return " ".join(num_list)


def to_mixed_case(name):
    word_lst = name.split('_')
    word_lst = [w for w in word_lst if w != '']
    if len(word_lst) < 1:
        return ""
    first = word_lst[0]
    rest = ''.join([w.capitalize() for w in word_lst[1:]])
    return first.lower() + rest

############################################################
# Section 6: Polynomials
############################################################


class Polynomial(object):

    def __init__(self, polynomial):
        self.polynomial = tuple(tuple(t) for t in polynomial)

    def get_polynomial(self):
        return self.polynomial

    def __neg__(self):
        return Polynomial((-c, x) for c, x in self.polynomial)

    def __add__(self, other):
        return Polynomial(self.polynomial + other.polynomial)

    def __sub__(self, other):
        res = [t for t in self.polynomial]
        for c, x in other.polynomial:
            res.append((-c, x))
        return Polynomial(res)

    def __mul__(self, other):
        res = []
        for c1, x1 in self.polynomial:
            for c2, x2 in other.polynomial:
                res.append((c1*c2, x1+x2))
        return Polynomial(res)

    def __call__(self, x):
        return sum([t[0]*(x**t[1]) for t in self.polynomial])

    def simplify(self):
        terms = {}
        for c, x in self.polynomial:
            terms[x] = terms.get(x, 0) + c
        poly_lst = [(c, x) for x, c in terms.items() if c != 0]
        if len(poly_lst) < 1:
            self.polynomial = ((0, 0),)
        else:
            poly_lst.sort(key=lambda t: t[1], reverse=True)
            self.polynomial = tuple(poly_lst)

    def __str__(self):
        res = []
        for c, x in self.polynomial:
            if x == 0 and c >= 0:
                res.append(f"+{c}")
            elif x == 0:
                res.append(f"{c}")
            elif c == 1 and x == 1:
                res.append(f"+x")
            elif c == -1 and x == 1:
                res.append(f"-x")
            elif c == 1:
                res.append(f"+x^{x}")
            elif c == -1:
                res.append(f"-x^{x}")
            elif x == 1 and c >= 0:
                res.append(f"+{c}x")
            elif x == 1:
                res.append(f"{c}x")
            elif c >= 0:
                res.append(f"+{c}x^{x}")
            else:
                res.append(f"{c}x^{x}")
        res_str = " ".join(res)
        res_str = res_str.replace('-', '- ')
        res_str = res_str.replace('+', '+ ')
        if len(res_str) < 1:
            return ""
        if res_str[0] == '-':
            res_str = res_str.replace('- ', '-', 1)
        else:
            res_str = res_str.replace('+ ', '', 1)
        return res_str

############################################################
# Section 7: Python Packages
############################################################


def sort_array(list_of_matrices):
    flat = np.concatenate([lst.flatten() for lst in list_of_matrices])
    return np.sort(flat)[::-1]


def POS_tag(sentence):
    tokens = nltk.word_tokenize(sentence)
    all_words = [w.lower() for w in tokens if w.isalpha()]
    stop = set(nltk.corpus.stopwords.words('english'))
    pos_words = [w for w in all_words if w not in stop]
    tags = nltk.pos_tag(pos_words)
    return tags

############################################################
# Section 8: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
9
"""

feedback_question_2 = """
The Python Packages section was more difficult for me, since it
took more time to do research on the packages and find the appropriate
functions to use. There weren't many significant blockers, but
definitely had to refresh on some of my Python knowledge.
"""

feedback_question_3 = """
I actually liked writing the test cases for the functions we wrote,
it seems like a very useful thing to have practice doing since we'll
need to be testing a lot in industry. The Polynomial section was
particularly fun for me to build. Wouldn't change anything.
"""
