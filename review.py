"""Review Class file"""


class Review:
    """Node that represents a review in a graph
    Instance Attributes:
    - user_id: a unique integer representing the user
    - recipe_id: a unique integer representing the recipe
    - date: the date the recipe was created
    - rating: an integer, from 0 to 5, representing the rating a user gave for a recipe.
    - review: the comments the user chose to leave with their review on this recipe

    Representation Invariants:
    - self.rating in {0, 1, 2, 3, 4, 5}
    """
    user_id: int
    recipe_id: int
    date: str
    rating: int
    review: str

    def __init__(self, user_id: int, recipe_id: int, date: str, rating: int, review: str) -> None:
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.date = date
        self.rating = rating
        self.review = review


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'disable': ['too-many-arguments'],
        'max-line-length': 120
    })
