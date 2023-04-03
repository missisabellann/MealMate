""" CSC111: MealMate (Final Project) by Evan Wang and Isabella Nguyen
===============================
This file contains the user class.
Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of Evan Wang and Isabella Nguyen
for CSC111  t the University of Toronto St. George campus. All forms of
distribution of this code without concent, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project,
please consult Evan Wang (eevan.wang@mail.utoronto.ca) or Isabella Nguyen (isabella.nguyen@mail.utoronto.ca).
This file is Copyright (c) 2023 Evan Wang and Isabella Nguyen.
"""
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
    import doctest
    doctest.testmod(verbose=True)
    import python_ta
    python_ta.check_all(config={
        'disable': ['forbidden-import'],
        'max-line-length': 120
    })
