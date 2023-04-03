""" CSC111: MealMate (Final Project) by Evan Wang and Isabella Nguyen
Project Description
===============================
Sometimes it gets difficult to choose what to eat throughout the day, especially with all options
available in Toronto. Deciding what to eat, commuting, then finding a spot to eat can be
time-consuming. Food delivery apps are an option, but they tend to be expensive. As university students,
we want to save some money so we should opt to cook sometimes instead.
Sometimes students want something new but it is difficult to explore new recipes and meals
because we do not want to spend hours scrolling through recipe pages and students want to
use up what is left in their fridges. So our question was, How can we recommend a meal
based on user preferences? Including their past favourites, ratings.
preferred cooking time, and any ingredients they want to use.
Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of Evan Wang and Isabella Nguyen
for CSC111  t the University of Toronto St. George campus. All forms of
distribution of this code without concent, whether as given or with any changes, are
expressly prohibited. For more information on copyright for this project,
please consult Evan Wang (eevan.wang@mail.utoronto.ca) or Isabella Nguyen (isabella.nguyen@mail.utoronto.ca).
This file is Copyright (c) 2023 Evan Wang and Isabella Nguyen.
"""

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
    import doctest
    doctest.testmod(verbose=True)
    import python_ta
    python_ta.check_all(config={
        'disable': ['too-many-arguments'],
        'max-line-length': 120
    })
