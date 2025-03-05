# Include your imports here, if any are used.

student_name = "Brianna Huang"

# 1. Value Iteration
class ValueIterationAgent:
    """Implement Value Iteration Agent using Bellman Equations."""

    def __init__(self, game, discount):
        """Store game object and discount value into the agent object,
        initialize values if needed.
        """
        # get_actions(state: State) -> Set[Action]
        # get_transitions(current_state: State, action: Action) -> Dict[State, float]
        # get_reward(current_state: State, action: Action, next_state: State) -> float
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
            q_value += prob * (self.game.get_reward(state, action, next_state) + (self.discount * self.get_value(next_state)))
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
        for state in self.states:
            self.values[state] = self.get_q_value(state, self.get_best_policy(state))


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

        ...  # TODO


# 3. Bridge Crossing Analysis
def question_3():
    discount = ...
    noise = ...
    return discount, noise


# 4. Policies
def question_4a():
    discount = ...
    noise = ...
    living_reward = ...
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4b():
    discount = ...
    noise = ...
    living_reward = ...
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4c():
    discount = ...
    noise = ...
    living_reward = ...
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4d():
    discount = ...
    noise = ...
    living_reward = ...
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


def question_4e():
    discount = ...
    noise = ...
    living_reward = ...
    return discount, noise, living_reward
    # If not possible, return 'NOT POSSIBLE'


# 5. Feedback
# Just an approximation is fine.
feedback_question_1 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_3 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""
