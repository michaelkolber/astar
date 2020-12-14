# Python A* Search

A class that implements a simple version of A\* search. The user provides the start state, an h\*()
function, and a function that creates children of a current state. A solution state is returned,
whose `.ancestors()` method can be called to get the full list of ancestors up to the start state.

Here is a simple example:

```python
asearch = AStarSearch(
    [2, 8, 3, 1, 6, 4, 7, 0, 5],  # Start state
    h_star,                       # User-defined function
    create_children               # User-defined function
)

solution = asearch.search(
    [1, 2, 3, 8, 0, 4, 7, 6, 5]  # Goal state
)

print(solution.ancestors())
```

For a more in-depth example, see `8puzzle_test.py`.
