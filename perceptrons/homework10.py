############################################################
# CIS 521: Homework 9
############################################################

from collections import defaultdict
import homework10_data as data
student_name = "Brianna Huang"

############################################################
# Imports
############################################################


# Include your imports here, if any are used.

############################################################
# Section 1: Perceptrons
############################################################


class BinaryPerceptron(object):

    def __init__(self, examples, iterations):
        self.iterations = iterations
        self.examples = list(examples)
        self.weights = {}

        for i in range(self.iterations):
            for features, y_true in self.examples:
                pred = self.predict(features)
                if pred != y_true:
                    if y_true > 0:
                        for x, value in features.items():
                            self.weights[x] = self.weights.get(x, 0) + value
                    else:
                        for x, value in features.items():
                            self.weights[x] = self.weights.get(x, 0) - value

    def predict(self, x):
        sum = 0
        for xi, value in x.items():
            sum += self.weights.get(xi, 0) * value
        return sum > 0


class MulticlassPerceptron(object):

    def __init__(self, examples, iterations):
        self.iterations = iterations
        self.examples = examples
        # weights[label] = {x1:_, x2:_,...}
        self.weights = defaultdict(dict)

        for i in range(self.iterations):
            for features, label in self.examples:
                pred = self.predict(features)
                if pred != label:
                    for x, value in features.items():
                        self.weights[label][x] = self.weights[label].get(
                            x, 0) + value
                        if pred:
                            self.weights[pred][x] = self.weights[pred].get(
                                x, 0) - value

    def predict(self, x):
        probs = {}
        for label in self.weights:
            prob = 0
            for feature, value in x.items():
                prob += self.weights[label].get(feature, 0) * value
            probs[label] = prob
        if probs:
            return max(probs, key=probs.get)
        return None

############################################################
# Section 2: Applications
############################################################


class IrisClassifier(object):

    def __init__(self, data):
        examples = [({'x1': x[0], 'x2': x[1], 'x3': x[2], 'x4': x[3]}, label)
                    for x, label in data]
        self.cls = MulticlassPerceptron(examples, 5)

    def classify(self, instance):
        features = {'x1': instance[0], 'x2': instance[1],
                    'x3': instance[2], 'x4': instance[3]}
        return self.cls.predict(features)


class DigitClassifier(object):

    def __init__(self, data):
        examples = [({ind: val for ind, val in enumerate(x)}, label)
                    for x, label in data]
        self.cls = MulticlassPerceptron(examples, 15)

    def classify(self, instance):
        features = {ind: val for ind, val in enumerate(instance)}
        return self.cls.predict(features)


class BiasClassifier(object):

    def __init__(self, data):
        examples = [({'x1': x, 'b': 1}, label) for x, label in data]
        self.cls = BinaryPerceptron(examples, 5)

    def classify(self, instance):
        feature = {'x1': instance, 'b': 1}
        return self.cls.predict(feature)


class MysteryClassifier1(object):

    def __init__(self, data):
        examples = [({'x1': x1, 'x2': x2, 'x3': x1**2 + x2**2, 'b': 1}, label)
                    for (x1, x2), label in data]
        self.cls = BinaryPerceptron(examples, 5)

    def classify(self, instance):
        x1, x2 = instance
        feature = {'x1': x1, 'x2': x2, 'x3': x1**2 + x2**2, 'b': 1}
        return self.cls.predict(feature)


class MysteryClassifier2(object):

    def __init__(self, data):
        examples = [({'x7': x1*x2*x3, 'b': 1}, label)
                    for (x1, x2, x3), label in data]
        self.cls = BinaryPerceptron(examples, 7)

    def classify(self, instance):
        x1, x2, x3 = instance
        feature = {'x7': x1*x2*x3, 'b': 1}
        return self.cls.predict(feature)

############################################################
# Section 3: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
10
"""

feedback_question_2 = """
Figuring out which features to add for the mystery classifiers
was the most challenging. Even after visualizing the data, adding
the correct transformations to the features was a bit confusing.
"""

feedback_question_3 = """
I liked the Iris problem! It was cool how quickly you could
use the perceptron to just classify a flower by its features.
"""
