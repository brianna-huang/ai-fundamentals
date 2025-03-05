from scenarios import *
from wampa_world import WampaWorld
from visualize_world import visualize_world
from utils import *

w = WampaWorld(S1)
visualize_world(w, w.agent.loc, get_direction(w.agent.degrees))
w.agent.record_percepts(w.get_percepts(), w.agent.loc)
w.agent.inference_algorithm()

w.take_action("forward")
visualize_world(w, w.agent.loc, get_direction(w.agent.degrees))
w.agent.record_percepts(w.get_percepts(), w.agent.loc)
w.agent.inference_algorithm()

w.take_action("left")
w.take_action("left")
w.take_action("forward")
w.take_action("left")
w.take_action("forward")
visualize_world(w, w.agent.loc, get_direction(w.agent.degrees))
w.agent.record_percepts(w.get_percepts(), w.agent.loc)
w.agent.inference_algorithm()

# w.take_action("right")
# visualize_world(w, w.agent.loc, get_direction(w.agent.degrees))
# w.agent.record_percepts(w.get_percepts(), w.agent.loc)
# w.agent.inference_algorithm()

# print('safe actions:', w.agent.all_safe_next_actions())

# w.take_action("right")
# visualize_world(w, w.agent.loc, get_direction(w.agent.degrees))
# w.agent.record_percepts(w.get_percepts(), w.agent.loc)
# w.agent.inference_algorithm()
# print('safe actions:', w.agent.all_safe_next_actions())