# Include your imports here, if any are used.

student_name = "Brianna Huang"

# 1. Value Iteration


class ValueIterationAgent:
    """Implement Value Iteration Agent using Bellman Equations."""

    def __init__(self, game, discount):
        """Store game object and discount value into the agent object,
        initialize values if needed.
        """
        self.game = game
        self.states = game.states
        self.discount = discount
        self.values = {}

    def get_value(self, state):
        """Return value V*(s) correspond to state.
        State values should be stored directly for quick retrieval.
        """
        return self.values.get(state, 0)

    def get_q_value(self, state, action):
        """Return Q*(s,a) correspond to state and action.
        Q-state values should be computed using Bellman equation:
        Q*(s,a) = Σ_s' T(s,a,s') [R(s,a,s') + γ V*(s')]
        """
        transitions = self.game.get_transitions(state, action)
        q_value = 0
        for next_state, prob in transitions.items():
            q_value += prob * (self.game.get_reward(state, action, next_state)
                               + (self.discount * self.get_value(next_state)))
        return q_value

    def get_best_policy(self, state):
        """Return policy π*(s) correspond to state.
        Policy should be extracted from Q-state values using policy extraction:
        π*(s) = argmax_a Q*(s,a)
        """
        max_q_value = float('-inf')
        best_action = None
        for action in self.game.get_actions(state):
            q_value = self.get_q_value(state, action)
            if q_value > max_q_value:
                max_q_value = q_value
                best_action = action
        return best_action

    def iterate(self):
        """Run single value iteration using Bellman equation:
        V_{k+1}(s) = max_a Q*(s,a)
        Then update values: V*(s) = V_{k+1}(s)
        """
        new_state_values = {}
        for state in self.states:
            max_q_value = float('-inf')
            for action in self.game.get_actions(state):
                # get all q-values for (s,a) pair
                q_value = self.get_q_value(state, action)
                max_q_value = max(max_q_value, q_value)
            new_state_values[state] = max_q_value
        self.values = new_state_values


# 2. Policy Iteration
class PolicyIterationAgent(ValueIterationAgent):
    """Implement Policy Iteration Agent.

    The only difference between policy iteration and value iteration is at
    their iteration method. However, if you need to implement helper function
    or override ValueIterationAgent's methods, you can add them as well.
    """

    def iterate(self):
        """Run single policy iteration.
        Fix current policy, iterate state values V(s) until
        |V_{k+1}(s) - V_k(s)| < ε
        """
        epsilon = 1e-6
        policy = {}
        for state in self.states:
            policy[state] = self.get_best_policy(state)

        # policy evaluation
        while True:
            delta = 0
            v_k = self.values.copy()
            for state in self.states:
                action = policy[state]
                self.values[state] = self.get_q_value(state, action)
                delta = max(delta, abs(self.values[state] - v_k.get(state, 0)))
            if delta < epsilon:
                break

        # policy improvement (one iteration)
        for state in self.states:
            policy[state] = self.get_best_policy(state)


# 3. Bridge Crossing Analysis


def question_3():
    discount = 0.9
    noise = 0
    return discount, noise


# 4. Policies
def question_4a():
    discount = 0.9
    noise = 0.01
    living_reward = -5.0
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4b():
    discount = 0.01
    noise = 0.01
    living_reward = 0.0
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4c():
    discount = 0.9
    noise = 0
    living_reward = 0.0
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4d():
    discount = 0.9
    noise = 0.2
    living_reward = 0.0
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4e():
    discount = 0
    noise = 0.2
    living_reward = 1.0
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


# 5. Feedback
# Just an approximation is fine.
feedback_question_1 = """
10
"""

feedback_question_2 = """
Wrapping my head around the Bellman equation to really understand it
intuitively was the most challenging part. All the different equations
were pretty intimidating at first, but implemeting the different
functions one by one definitely helped.
"""

feedback_question_3 = """
I liked the Bridge Crossing and Discount Grid problems. It was
interesting to see how the different factors of the Bellman equation
affected the behavior of the agents!
"""
