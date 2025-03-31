import random

student_name = "Brianna Huang"


# 1. Q-Learning
class QLearningAgent:
    """Implement Q Reinforcement Learning Agent using Q-table."""

    def __init__(self, game, discount, learning_rate, explore_prob):
        """Store any needed parameters into the agent object.
        Initialize Q-table.
        """
        self.game = game
        self.discount = discount
        self.learning_rate = learning_rate
        self.explore_prob = explore_prob
        self.q_table = {}

    def get_q_value(self, state, action):
        """Retrieve Q-value from Q-table.
        For an never seen (s,a) pair, the Q-value is by default 0.
        """
        return self.q_table.get((state, action), 0)

    def get_value(self, state):
        """Compute state value from Q-values using Bellman Equation.
        V(s) = max_a Q(s,a)
        """
        q_values = [self.get_q_value(state, action)
                    for action in self.game.get_actions(state)]
        if not q_values:
            return 0
        return max(q_values)

    def get_best_policy(self, state):
        """Compute the best action to take in the state
        using Policy Extraction.
        π(s) = argmax_a Q(s,a)

        If there are ties, return a random one for better performance.
        Hint: use random.choice().
        """
        actions = self.game.get_actions(state)
        max_q_value = max(self.get_q_value(state, action)
                          for action in actions)
        best_actions = [action for action in actions if self.get_q_value(
            state, action) == max_q_value]
        return random.choice(best_actions)

    def update(self, state, action, next_state, reward):
        """Update Q-values using running average.
        Q(s,a) = (1 - α) Q(s,a) + α (R + γ V(s'))
        Where α is the learning rate, and γ is the discount.

        Note: You should not call this function in your code.
        """
        self.q_table[(state, action)] = ((1 - self.learning_rate)
                                         * self.get_q_value(state, action)
                                         + self.learning_rate *
                                         (reward + self.discount
                                         * self.get_value(next_state)))

    # 2. Epsilon Greedy
    def get_action(self, state):
        """Compute the action to take for the agent, incorporating exploration.
        That is, with probability ε, act randomly.
        Otherwise, act according to the best policy.

        Hint: use random.random() < ε to check if exploration is needed.
        """
        if random.random() < self.explore_prob:
            actions = list(self.game.get_actions(state))
            return random.choice(actions)
        else:
            return self.get_best_policy(state)

# 3. Bridge Crossing Revisited


def question3():
    epsilon = ...
    learning_rate = ...
    return 'NOT POSSIBLE'
    # return epsilon, learning_rate
    # If not possible, return 'NOT POSSIBLE'


# 5. Approximate Q-Learning
class ApproximateQAgent(QLearningAgent):
    """Implement Approximate Q Learning Agent using weights."""

    def __init__(self, *args, extractor):
        """Initialize parameters and store the feature extractor.
        Initialize weights table."""

        super().__init__(*args)
        self.extractor = extractor
        self.weights = {}

    def get_weight(self, feature):
        """Get weight of a feature.
        Never seen feature should have a weight of 0.
        """
        return self.weights.get(feature, 0)

    def get_q_value(self, state, action):
        """Compute Q value based on the dot product of
        feature components and weights.
        Q(s,a) = w_1 * f_1(s,a) + w_2 * f_2(s,a) + ... + w_n * f_n(s,a)
        """
        features = self.extractor(state, action)
        q_value = 0
        for feature, value in features.items():
            q_value += self.get_weight(feature) * value
        return q_value

    def update(self, state, action, next_state, reward):
        """Update weights using least-squares approximation.
        Δ = R + γ V(s') - Q(s,a)
        Then update weights: w_i = w_i + α * Δ * f_i(s, a)
        """
        features = self.extractor(state, action)
        next_value = self.get_value(next_state)
        delta = reward + (self.discount * next_value) - \
            self.get_q_value(state, action)

        for feature, value in features.items():
            self.weights[feature] = self.weights.get(
                feature, 0) + (self.learning_rate * delta * value)


# 6. Feedback
# Just an approximation is fine.
feedback_question_1 = """
12
"""

feedback_question_2 = """
This assignment wasn't too challenging, I just had to address
a few bugs I was having with getting actions without returning None,
and remembering about the game.get_actions function.
"""

feedback_question_3 = """
Again, I liked how easily digestible this assignment was. It helps
me grasp the Q-learning and RL by breaking the problem down into
its separate parts.
"""
