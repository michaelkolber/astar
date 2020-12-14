"""Test A* search using an 8-puzzle example."""

from typing import List
from a_star_search import AStarSearch, AStarState


def h_star(child: List[int], goal: List[int]) -> int:
    total = 0
    for i, j in zip(child, goal):
        if i != j:
            total += 1
    return total


def create_children(parent: List[int]) -> List[List[int]]:
    # Depending on where the 0 is, there are either 2, 3, or 4 moves.
    # The puzzle indices are as follows:
    #    0 1 2
    #    3 4 5
    #    6 7 8

    children: List[List[int]] = []

    def move_piece(zero_index: int, piece_index):
        child = parent[:]
        child[zero_index] = child[piece_index]
        child[piece_index] = 0
        return child

    # Two moves, i.e. corners
    if parent[0] == 0:
        children.append(move_piece(0, 1))
        children.append(move_piece(0, 3))
    elif parent[2] == 0:
        children.append(move_piece(2, 1))
        children.append(move_piece(2, 5))
    elif parent[6] == 0:
        children.append(move_piece(6, 3))
        children.append(move_piece(6, 7))
    elif parent[8] == 0:
        children.append(move_piece(8, 5))
        children.append(move_piece(8, 7))

    # Three moves, i.e. sides
    elif parent[1] == 0:
        children.append(move_piece(1, 0))
        children.append(move_piece(1, 2))
        children.append(move_piece(1, 4))
    elif parent[3] == 0:
        children.append(move_piece(3, 0))
        children.append(move_piece(3, 4))
        children.append(move_piece(3, 6))
    elif parent[5] == 0:
        children.append(move_piece(5, 2))
        children.append(move_piece(5, 4))
        children.append(move_piece(5, 8))
    elif parent[7] == 0:
        children.append(move_piece(7, 4))
        children.append(move_piece(7, 6))
        children.append(move_piece(7, 8))

    # Four moves, i.e. center
    elif parent[4] == 0:
        children.append(move_piece(4, 1))
        children.append(move_piece(4, 3))
        children.append(move_piece(4, 5))
        children.append(move_piece(4, 7))

    # Should not happen
    else:
        print('Programming error! No zero was found in configuration', parent)
        exit(1)

    return children


def print_solution(solution: AStarState):
    for item in solution.ancestors():
        data = item.data
        for i in range(len(data)):
            if data[i] == 0:
                data[i] = ' '
                break

        print(data[0], data[1], data[2])
        print(data[3], data[4], data[5])
        print(data[6], data[7], data[8])
        print()


asearch = AStarSearch([2, 8, 3, 1, 6, 4, 7, 0, 5], h_star, create_children)
solution = asearch.search([1, 2, 3, 8, 0, 4, 7, 6, 5])
print_solution(solution)
