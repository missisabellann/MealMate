""" CSC111: MealMate (Final Project) by Evan Wang and Isabella Nguyen
===============================
This file contains the recipe class.
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


class Recipe:
    """ A node that represents a recipe in a graph
    Instance Attributes
    - name: name of the recipe
    - recipe_id: the address of this recipe
    - contributer_id: id of the user who wrote the recipe
    - submitted_date: the date the recipe was submitted
    - nutrition:
        a mapping of the nutritional data for each recipe
    - n_steps: number of steps the recipe takes
    - steps: a description for each step
    - description: the description of the recipe written by the contributer
    - ingredients: a list of the ingredients the recipe requires
    - n_ingredients: the number of ingredients
    - users: list of users that have rated this recipe
    Representation Invariants:
    - name != ''
    - id > 0
    - contributer_id > 0
    - len(nutrition) == 7
    - n_steps > 0
    - len(steps) == n_steps
    - len(ingredients) == n_ingredients
    """

    name: str
    recipe_id: int
    minutes: int
    contributor_id: int
    submitted_date: str
    tags: list[str]
    nutrition: dict[str, float]
    n_steps: int
    steps: list[str]
    description: str
    ingredients: list[str]
    n_ingredients: int
    reviews_received: list[Review]

    def __init__(self,
                 name: str,
                 recipe_id: int,
                 minutes: int,
                 contributor_id: int,
                 submitted_date: str,
                 tags: list[str],
                 nutrition_lst: list[str],
                 n_steps: int,
                 steps: list[str],
                 description: str,
                 ingredients: list[str],
                 n_ingredients: int) -> None:
        self.name = name
        self.recipe_id = recipe_id
        self.minutes = minutes
        self.contributor_id = contributor_id
        self.submitted_date = submitted_date
        self.tags = tags
        # nutrition_lst = nutrition_lst.split(',')
        self.nutrition = {'calories': float(nutrition_lst[0]),
                          'fat': float(nutrition_lst[1]),
                          'sodium': float(nutrition_lst[2]),
                          'protein': float(nutrition_lst[3]),
                          'saturated fats': float(nutrition_lst[4]),
                          'carbohydrates': float(nutrition_lst[5])}
        self.n_steps = n_steps
        self.steps = steps
        self.description = description
        self.ingredients = ingredients
        self.n_ingredients = n_ingredients
        self.reviews_received = []

    def get_review(self, user_id: int) -> Review:
        """Return a review of the recipe, given id of the user that gave the review."""

        for review in self.reviews_received:
            if review.user_id == user_id:
                return review

        raise ValueError


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
    import python_ta
    python_ta.check_all(config={
        'disable': ['forbidden-import', 'too-many-instance-attributes', 'too-many-arguments'],
        'max-line-length': 120
    })
