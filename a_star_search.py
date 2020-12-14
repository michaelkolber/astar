from typing import Callable, List, TypeVar, Union
from collections import deque


T = TypeVar('T')


class AStarList(deque):
    """Essentially a `deque` with a sorted insertion method that uses a state's f_star value as a key."""

    def sorted_insert(self, state: 'AStarState'):
        for i, item in enumerate(self):
            if (state.f_star >= item.f_star):
                continue
            self.insert(i, state)
            return
        self.append(state)

    def __repr__(self):
        return str([x.f_star for x in self])


class AStarState:
    def __init__(self, data: T, g: int, parent: 'AStarState' = None) -> None:
        self.data = data
        self.g = g
        self.parent = parent

        self.h_star: int = 0
        self.update_f_star()

    def __eq__(self, o: 'AStarState') -> bool:
        return self.data == o.data

    def update_f_star(self):
        self.f_star = self.g + self.h_star

    def check_ancestors(self):
        """Return `False` if the current state has a parent with the same data, and `True` otherwise."""
        parent = self.parent
        while parent:
            if parent.data == self.data:
                return False
            parent = parent.parent
        return True

    def ancestors(self):
        """Return the state's ancestors, with the most distant ancestor first and this state last."""
        stack = deque([self])
        parent = self.parent
        while parent:
            stack.appendleft(parent)
            parent = parent.parent
        return list(stack)


class AStarSearch:
    """
    An A* search starting from a given datapoint, `start`.

    `h_star` is a function that takes a datapoint and a goal datapoint, and returns how many steps
    away the datapoint is from the goal datapoint.

    `create_children` is a function that takes a datapoint and creates all the immediately derivative
    datapoints from that datapoint. For example, if the datapoint is a chess board, this function
    would return a list of all possible next moves of the chess board (for whosever turn it is).
    """

    def __init__(self, start: T, h_star: Callable[[T, T], int], create_children: Callable[[T], List[T]]) -> None:
        self.start_state = AStarState(start, 0)
        self.h_star = h_star  # This is a function
        self.create_children = create_children

    def search(self, goal: T) -> Union[AStarState, None]:
        """Search for a path to `goal`. Returns an `AStarState`, whose `.ancestors()` method can be
        called to get the ordered path taken from start node to goal node."""
        goal_state = AStarState(goal, 0)
        # States that have yet to be processed, in increasing order by `f_star`
        open_list = AStarList([self.start_state])
        # States that have been processed, in no particular order
        close_list = AStarList()

        while(len(open_list) > 0):
            current_state = open_list.popleft()

            if current_state == goal_state:
                return current_state

            for child in self.create_children(current_state.data):
                # Create the child state
                child_state = AStarState(child, current_state.g + 1, current_state)
                # Skip this child if it's its own ancestor
                if not child_state.check_ancestors():
                    continue
                child_state.h_star = self.h_star(child_state.data, goal_state.data)
                child_state.update_f_star()

                # Where in `open_list` this child appears, if at all
                try:
                    open_list_child_index = open_list.index(child_state)
                except ValueError:
                    open_list_child_index = -1
                # Where in `close_list` this child appears, if at all
                try:
                    close_list_child_index = close_list.index(child_state)
                except ValueError:
                    close_list_child_index = -1

                # Child does not appear in either list
                if open_list_child_index == -1 and close_list_child_index == -1:
                    open_list.sorted_insert(child_state)
                # Child appears in open_list and has a smaller `f_star`
                elif open_list_child_index != -1 and child_state.f_star < open_list[open_list_child_index].f_star:
                    open_list[open_list_child_index] = child_state
                # Child appears in close_list and has a smaller `f_star`
                elif close_list_child_index != -1 and child_state.f_star < close_list[close_list_child_index].f_star:
                    close_list.remove(child_state)
                    open_list.sorted_insert(child_state)

            # We're finished with the current node
            close_list.append(current_state)

        return None
