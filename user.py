"""User Class file"""

from review import Review


class User:
    """Node that represents a user in a graph
    Instance Attributes:
    - user_id: a unique integer representing a user
    - reviewed_recipes: a list of that user's recipes they've given reviews for,
                        in the case of the user that is receiving recommendations, this includes recipes they like

    Representation Invariants:
    - each user_id is unique
    """
    user_id: int
    reviewed_recipes: list[Review]

    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        self.reviewed_recipes = []

    def get_review(self, recipe_id: int) -> Review:
        """Return a review of a recipe, given the recipe id."""

        for review in self.reviewed_recipes:
            if review.recipe_id == recipe_id:
                return review

        raise ValueError


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'disable': ['forbidden-import'],
        'max-line-length': 120
    })
