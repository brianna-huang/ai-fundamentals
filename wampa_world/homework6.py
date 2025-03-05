from random import shuffle, choice
from itertools import combinations
from utils import flatten, get_direction, is_facing_wampa
from collections import deque


# KNOWLEDGE BASE
class KB:
    def __init__(self, agent):
        self.all_rooms = {agent.loc}  # set of rooms that are known to exist
        self.safe_rooms = {agent.loc}  # set of rooms that are known to be safe
        self.visited_rooms = {agent.loc}  # set of visited rooms (x, y)
        self.stench = set()  # set of rooms where stench has been perceived
        self.breeze = set()  # set of rooms where breeze has been perceived
        self.bump = dict()  # {loc: direction} where bump has been perceived
        self.gasp = False  # True if gasp has been perceived
        self.scream = False  # True if scream has been perceived
        self.walls = set()  # set of rooms (x, y) that are known to be walls
        self.pits = set()  # set of rooms (x, y) that are known to be pits
        self.wampa = set()  # room (x, y) that is known to be the Wampa
        self.luke = None  # room (x, y) that is known to be Luke


# AGENT
class Agent:
    def __init__(self, world):
        self.world = world
        self.loc = (0, 0)
        self.score = 0
        self.degrees = 0
        self.blaster = True
        self.has_luke = False
        self.percepts = ['stench', 'breeze', 'gasp', 'bump', 'scream']
        self.orientation_to_delta = {
            "up": (0, 1),  # (dx, dy)
            "down": (0, -1),
            "left": (-1, 0),
            "right": (1, 0)
        }
        self.KB = KB(self)
        self.moves = 0

    def turn_left(self):
        self.degrees -= 90

    def turn_right(self):
        self.degrees += 90

    def adjacent_rooms(self, room):
        """Returns a set of tuples representing all possible adjacent rooms to
        'room' Use this function to update KB.all_rooms."""
        x, y = room
        adjacent = {(x+1, y), (x-1, y), (x, y+1), (x, y-1)}
        return adjacent

    def record_percepts(self, sensed_percepts, current_location):
        """Update the percepts in agent's KB with the percepts sensed in the
        current location, and update visited_rooms and all_rooms."""
        self.loc = current_location
        present_percepts = set(p for p in sensed_percepts if p)

        if "stench" in present_percepts:
            self.KB.stench.add(current_location)
        if "breeze" in present_percepts:
            self.KB.breeze.add(current_location)
        if "gasp" in present_percepts:
            self.KB.gasp = True
            self.KB.luke = current_location
        if "bump" in present_percepts:
            direction = get_direction(self.degrees)
            self.KB.bump[current_location] = direction
            x, y = self.orientation_to_delta[direction]
            curr_x, curr_y = current_location
            self.KB.walls.add((curr_x+x, curr_y+y))
        if "scream" in present_percepts:
            self.KB.scream = True

        # add current room to visited, add adjacent rooms to all rooms
        self.KB.visited_rooms.add(current_location)
        adjacent = self.adjacent_rooms(current_location)
        self.KB.all_rooms.update(adjacent)

    def enumerate_possible_worlds(self):
        """Return the set of all possible worlds, where a possible world is a
        tuple of (pit_rooms, wampa_room), pit_rooms is a tuple of tuples
        representing possible pit rooms, and wampa_room is a tuple representing
        a possible wampa room.

        Since the goal is to combinatorially enumerate all the possible worlds
        (pit and wampa locations) over the set of rooms that could potentially
        have a pit or a wampa, we first want to find that set. To do that,
        subtract the set of rooms that you know cannot have a pit or wampa from
        the set of all rooms. For example, you know that a room with a wall
        cannot have a pit or wampa.

        Then use itertools.combinations to return the set of possible worlds,
        or all combinations of possible pit and wampa locations.

        You may find the utils.flatten(tup) method useful here for flattening
        wampa_room from a tuple of tuples into a tuple.

        The output of this function will be queried to find the model of the
        query, and will be checked for consistency with the KB
        to find the model of the KB."""

        possible_bad_rooms = (self.KB.all_rooms - self.KB.safe_rooms
                              - self.KB.walls)

        # get possible pits, get possible wampa
        possible_pits = set()
        for num_pits in range(len(possible_bad_rooms) + 1):
            possible_pits.update(
                set(combinations(possible_bad_rooms, num_pits)))
        possible_pits.add(())
        possible_wampas = set(combinations(possible_bad_rooms, 1))

        # get all possible worlds with pits and wampa
        possible_worlds = set()
        for pit_rooms in possible_pits:
            for wampa_room in possible_wampas | {()}:
                if (len(wampa_room) == 0 or
                        flatten(wampa_room) not in pit_rooms):
                    possible_worlds.add(
                        (tuple(pit_rooms), tuple(flatten(wampa_room))))

        # if there are no possible pits or wampas
        if possible_worlds == set():
            return {((), ())}

        return possible_worlds

    def pit_room_is_consistent_with_KB(self, pit_room):
        """Return True if the room could be a pit given breeze in KB, False
        otherwise. A room could be a pit if all adjacent rooms that have been
        visited have had breeze perceived in them. A room cannot be a pit if
        any adjacent rooms that have been visited have not had breeze perceived
        in them. This will be used to find the model of the KB."""
        if pit_room == tuple():  # It is possible that there are no pits
            return not self.KB.breeze  # if no breeze has been perceived yet
        adjacent = self.adjacent_rooms(pit_room)

        # if none of the rooms next to the pit room has a breeze, return False
        for room in self.KB.visited_rooms:
            if room in adjacent:
                if room not in self.KB.breeze:
                    return False
        return True

    def wampa_room_is_consistent_with_KB(self, wampa_room):
        """Return True if the room could be a wampa given stench in KB, False
        otherwise. A room could be a wampa if all adjacent rooms that have been
        visited have had stench perceived in them. A room cannot be a wampa if
        any adjacent rooms that have been visited have not had stench perceived
        in them. This will be used to find the model of the KB."""
        if wampa_room == tuple():  # It is possible that there is no Wampa
            return not self.KB.stench  # if no stench has been perceived yet
        adjacent = self.adjacent_rooms(wampa_room)

        # if none of the rooms next to the wampa has a stench, return False
        for room in self.KB.visited_rooms:
            if room in adjacent:
                if room not in self.KB.stench:
                    return False

        for room in self.KB.visited_rooms:
            if (room not in self.KB.stench and
                    any(wampa == room for wampa in adjacent)):
                return False
        return True

    def find_model_of_KB(self, possible_worlds):
        """Return the subset of all possible worlds consistent with KB.
        possible_worlds is a set of tuples (pit_rooms, wampa_room),
        pit_rooms is a set of tuples of possible pit rooms,
        and wampa_room is a tuple representing a possible wampa room.
        A world is consistent with the KB if wampa_room is consistent
        and all pit rooms are consistent with the KB."""
        worlds = set()
        for pit_rooms, wampa_room in possible_worlds:
            if not pit_rooms and self.KB.breeze:
                continue
            # if all the pits are consistent with the KB
            if (all(self.pit_room_is_consistent_with_KB(pit)
                    for pit in pit_rooms)):
                if self.wampa_room_is_consistent_with_KB(wampa_room):
                    worlds.add((pit_rooms, wampa_room))
        return worlds

    def find_model_of_query(self, query, room, possible_worlds):
        """Where query can be "pit_in_room", "wampa_in_room", "no_pit_in_room"
        or "no_wampa_in_room",filter the set of worlds
        according to the query and room."""
        worlds = set()
        for pit_rooms, wampa_room in possible_worlds:
            if query == "pit_in_room" and room in pit_rooms:
                worlds.add((pit_rooms, wampa_room))
            elif query == "wampa_in_room" and room == wampa_room:
                worlds.add((pit_rooms, wampa_room))
            elif query == "no_pit_in_room" and room not in pit_rooms:
                worlds.add((pit_rooms, wampa_room))
            elif query == "no_wampa_in_room" and wampa_room != room:
                worlds.add((pit_rooms, wampa_room))
        return worlds

    def infer_wall_locations(self):
        """If a bump is perceived, infer wall locations along the entire known
        length of the room."""
        min_x = min(self.KB.all_rooms, key=lambda x: x[0])[0]
        max_x = max(self.KB.all_rooms, key=lambda x: x[0])[0]
        min_y = min(self.KB.all_rooms, key=lambda x: x[1])[1]
        max_y = max(self.KB.all_rooms, key=lambda x: x[1])[1]
        for room, orientation in self.KB.bump.items():
            if orientation == "up":
                for x in range(min_x, max_x + 1, 1):
                    self.KB.walls.add((x, room[1] + 1))
            elif orientation == "down":
                for x in range(min_x, max_x + 1, 1):
                    self.KB.walls.add((x, room[1] - 1))
            elif orientation == "left":
                for y in range(min_y, max_y + 1, 1):
                    self.KB.walls.add((room[0] - 1, y))
            elif orientation == "right":
                for y in range(min_y, max_y + 1, 1):
                    self.KB.walls.add((room[0] + 1, y))

    def inference_algorithm(self):
        """First, make some basic inferences:
        1. If there is no breeze or stench in current location, infer that the
        adjacent rooms are safe.
        2. Infer wall locations given bump percept.
        3. Infer Luke's location given gasp percept.
        4. Infer whether the Wampa is alive given scream percept. Clear stench
        from the KB if Wampa is dead.

        Then, infer whether each adjacent room is safe, pit or wampa by
        following the backward-chaining resolution algorithm:
        1. Enumerate possible worlds.
        2. Find the model of the KB, i.e. the subset of possible worlds
        consistent with the KB.
        3. For each adjacent room and each query, find the model of the query.
        4. If the model of the KB is a subset of the model of the query, the
        query is entailed by the KB.
        5. Update KB.pits, KB.wampa, and KB.safe_rooms based on any newly
        derived knowledge.
        """

        location = self.loc
        adjacent = self.adjacent_rooms(location)
        self.KB.all_rooms.update(adjacent)

        # basic inferences
        self.KB.safe_rooms.update(self.KB.visited_rooms)
        if location not in self.KB.breeze and location not in self.KB.stench:
            self.KB.safe_rooms.update(adjacent)
        if location in self.KB.bump.keys():
            self.infer_wall_locations()
        if self.KB.gasp:
            self.KB.luke = location
        if self.KB.scream:
            self.KB.stench.clear()
            self.KB.safe_rooms.add(self.KB.wampa)

        # backward-chaining resolution algorithm
        possible_worlds = self.enumerate_possible_worlds()
        model_of_KB = self.find_model_of_KB(possible_worlds)

        for room in adjacent:
            # get models for potential
            pit_model = self.find_model_of_query(
                "pit_in_room", room, possible_worlds)
            wampa_model = self.find_model_of_query(
                "wampa_in_room", room, possible_worlds)
            no_pit_model = self.find_model_of_query(
                "no_pit_in_room", room, possible_worlds)
            no_wampa_model = self.find_model_of_query(
                "no_wampa_in_room", room, possible_worlds)

            if model_of_KB:
                # query is entailed by the KB
                if model_of_KB.issubset(pit_model):
                    self.KB.pits.add(room)
                elif model_of_KB.issubset(wampa_model):
                    self.KB.wampa = room
                elif (model_of_KB.issubset(no_pit_model) and
                        model_of_KB.issubset(no_wampa_model)):
                    self.KB.safe_rooms.add(room)

    def all_safe_next_actions(self):
        """Define R2D2's valid and safe next actions based on his current
        location and knowledge of the environment."""
        safe_actions = []
        x, y = self.loc
        dx, dy = self.orientation_to_delta[get_direction(self.degrees)]
        forward_room = (x+dx, y+dy)

        safe_actions.append("left")
        safe_actions.append("right")
        if (forward_room in self.KB.safe_rooms and
                forward_room not in self.KB.walls):
            safe_actions.append("forward")
        if self.loc == self.KB.luke and not self.has_luke:
            safe_actions.append("grab")
        if self.KB.wampa and is_facing_wampa(self) and self.blaster:
            safe_actions.append("shoot")
        if self.loc == (0, 0) and self.has_luke:
            safe_actions.append("climb")
        return safe_actions

    def make_move(self, loc, dir, move):
        x, y = loc
        new_dir_left = {'up': 'left', 'left': 'down',
                        'down': 'right', 'right': 'up'}
        new_dir_right = {'left': 'up', 'down': 'left',
                         'right': 'down', 'up': 'right'}
        if move == 'left':
            return (loc, new_dir_left[dir])
        elif move == 'right':
            return (loc, new_dir_right[dir])
        else:
            delta_x, delta_y = self.orientation_to_delta[dir]
            new_loc = (x+delta_x, y+delta_y)
            return (new_loc, dir)

    def go_home(self):
        """Goes to (0,0) once R2D2 has Luke"""
        safe_rooms = self.KB.safe_rooms
        location = self.loc
        direction = get_direction(self.degrees)

        # (location, direction), [moves]
        queue = deque([((location, direction), [])])
        visited = set()
        actions = ["left", "right", "forward"]

        while queue:
            (loc, dir), moves = queue.popleft()
            if loc == (0, 0):
                return moves[0] if moves else None
            if (loc, dir) not in visited:
                visited.add((loc, dir))
                for move in actions:
                    new_loc, new_dir = self.make_move(loc, dir, move)
                    if new_loc in safe_rooms and new_loc not in self.KB.walls:
                        queue.append(((new_loc, new_dir), moves + [move]))
        return None

    def choose_next_action(self):
        """Choose next action from all safe next actions. You may want to
        prioritizesome actions based on current state. For example, if R2D2
        knows Luke's location and is in the same room as Luke, you may want
        to prioritize 'grab' over all other actions. Similarly, if R2D2 has
        Luke, you may want to prioritize moving toward the exit. You can
        implement this as basically (randomly choosing between safe actions)
        or as sophisticated (optimizing exploration of unvisited states,
        finding shortest paths, etc.) as you like."""
        actions = self.all_safe_next_actions()
        self.moves += 1
        if "climb" in actions:
            return "climb"
        if "grab" in actions:
            return "grab"
        if "shoot" in actions:
            return "shoot"
        if self.has_luke:
            return self.go_home()
        action = choice(actions)
        return action


# Approximately how many hours did you spend on this assignment?
feedback_question_1 = 15

# Which aspects of this assignment did you find most challenging?
# Were there any significant stumbling blocks?
feedback_question_2 = """
Making sure the logic in not just the inference algorithm but the
x_room_is_consistent_with_KB functions worked as expected was
the most challenging part for me. It was hard to trace back errors
to the specific functions they arise from, since from my perspective,
all I know is the agent isn't doing what it's supposed to. I had
to trace through what exact rooms were in the safe, visited, adjacent,
pit sets, etc.
"""

# Which aspects of this assignment did you like?
# Is there anything you would have changed?
feedback_question_3 = """
Like usual, it's very fun seeing the algorithm work in the end and
saving Luke! It's interesting to see a search-like game be done
with just logic statements and knowledge base operations. Wouldn't
change anything.
"""
