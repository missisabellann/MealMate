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

import math
from datetime import datetime
from typing import Any

from recipe import Recipe
from review import Review
from user import User


class Graph:
    """A graph.
    Contains users, recipes, and reviews

    Instance Attributes:
    - user_nodes: contains all users in this graph, stored in a dictionary.
        The key of the dictionary contains the user id, the value is the user object.
    - reipce_nodes: contains all recipes in this graph, stored in a dictionary.
        The key of the dictionary contains the recipe id, the value is the recipe object.
    - links: contains all reviews in this graph, stored in a set.

    """

    user_nodes: dict[Any, User]  # user id: user object
    recipe_nodes: dict[Any, Recipe]  # recipe name (or id?): recipe object
    links: set[Review]

    def __init__(self) -> None:
        self.user_nodes = {}
        self.recipe_nodes = {}
        self.links = set()

    def add_user(self, user: User) -> None:
        """Add a user to the graph,
        stored in a dictionary with the user_id as the key and the user object as the value."""

        self.user_nodes[user.user_id] = user  # user_id: user object

    def add_recipe(self, recipe: Recipe) -> None:
        """Add a recipe to the graph,
        stored in a dictionary with the recipe_id as the key and the recipe object as the value."""

        self.recipe_nodes[recipe.recipe_id] = recipe  # recipe_id: recipe object

    def add_link(self, review: Review) -> None:
        """Add a review to the graph, stored in a set.
        Then add the review to the recipe's received_reviews and to the user's reviewed_recipes.
        The review connects to exactly one user and exactly one recipe.
        Thus, the review forms a link between user and recipe.

        Preconditions:
        - review.user_id is not None
        - review.recipe_id is not None
        """

        self.links.add(review)
        self.recipe_nodes[review.recipe_id].reviews_received.append(review)
        self.user_nodes[review.user_id].reviewed_recipes.append(review)

    def get_connected_users(self, user: User) -> list[User]:
        """Given a user, get that user's list of recipes they've reviewed.
        Then, get the users who are connected to each recipe (not self).
        """

        shared_recipe_users = []
        recipes = [self.recipe_nodes[rev.recipe_id] for rev in user.reviewed_recipes]

        for recipe in recipes:
            for review in recipe.reviews_received:
                if self.user_nodes[review.user_id] not in shared_recipe_users:
                    shared_recipe_users.append(self.user_nodes[review.user_id])

        return shared_recipe_users

    def calculate_similarity_score(self, user: User, other_user: User) -> float:
        """Given another user, calculate the similarity score between your items and their items.

        Preconditions:
        - user and other_user share at least one recipe in their recipe lists.
        """
        # getting all reviews
        user_reviews = user.reviewed_recipes
        other_user_reviews = other_user.reviewed_recipes

        # getting all recipes
        user_recipes = []
        other_user_recipes = []
        for review in user_reviews:
            user_recipes.append(review.recipe_id)
        for review in other_user_reviews:
            other_user_recipes.append(review.recipe_id)

        # getting all recipes between the 2 people
        all_recipes_ids = []
        for recipe_id in user_recipes:
            if recipe_id not in all_recipes_ids:
                all_recipes_ids.append(recipe_id)
        for recipe_id in other_user_recipes:
            if recipe_id not in all_recipes_ids:
                all_recipes_ids.append(recipe_id)

        # creating a list of all reviews of all recipes
        all_user_reviews = []
        all_other_user_reviews = []

        for recipe_id in all_recipes_ids:
            if recipe_id not in user_recipes:
                all_user_reviews.append(0)
            else:
                all_user_reviews.append(user.get_review(recipe_id).rating)

        for recipe_id in all_recipes_ids:
            if recipe_id not in other_user_recipes:
                all_other_user_reviews.append(0)
            else:
                all_other_user_reviews.append(other_user.get_review(recipe_id).rating)

        # calculate cosine similarity
        products = []
        for i in range(0, len(all_user_reviews)):
            products.append(all_user_reviews[i] * all_other_user_reviews[i])

        score = sum(products) / math.sqrt(sum([rating ** 2 for rating in all_user_reviews]))

        return score

    def get_similar_users(self, user: User) -> list[User]:
        """Return a list of users sorted by similarity score in descending order."""

        connected_users = self.get_connected_users(user)
        users_and_scores = []

        for other_user in connected_users:
            score = self.calculate_similarity_score(user, other_user)
            # store user and score as tuple in a list
            users_and_scores.append((other_user, score))

        # sort
        descending_scores = mergesort(users_and_scores)
        similar_users = []

        for tup in descending_scores:
            similar_users.append(tup[0])

        return similar_users  # returns all connected users, in descending order by score

    def get_recommendations(self, user: User, other_user: User) -> list[Recipe]:
        """Return a list of recommended recipes.
        This means returning a list of recipes that a similar user has in their reviewed_recipes,
        but you don't have in your reviewed_recipes, since we are assuming similar users have similar taste."""

        recommendations = []
        user_reviews = [rev.recipe_id for rev in user.reviewed_recipes]

        for review in other_user.reviewed_recipes:
            if review.recipe_id not in user_reviews:
                if review.rating >= 4:
                    recommendations.append(self.recipe_nodes[review.recipe_id])

        return recommendations

    def rate_recommendation(self, user: User, recipe: Recipe, rating: int) -> None:
        """Have the user give a review on the recipe they were recommended and add it to the graph."""

        review = Review(user_id=user.user_id,
                        recipe_id=recipe.recipe_id,
                        date=datetime.today().strftime('%Y-%m-%d'),
                        rating=rating,
                        review="")
        self.add_link(review)


def mergesort(lst: list) -> list:
    """Sort a list recursively"""

    if len(lst) < 2:
        return lst.copy()
    else:
        middle = len(lst) // 2
        left_sorted = mergesort(lst[:middle])
        right_sorted = mergesort(lst[middle:])

        return merge(left_sorted, right_sorted)


def merge(lst1: list, lst2: list) -> list:
    """Combine two sublists. This is a helper function of mergesort."""

    merged_lst = []
    i1, i2 = 0, 0

    while i1 < len(lst1) and i2 < len(lst2):
        if lst1[i1][1] >= lst2[i2][1]:
            merged_lst.append(lst1[i1])
            i1 += 1
        else:
            merged_lst.append(lst2[i2])
            i2 += 1

    if i1 == len(lst1):
        return merged_lst + lst2[i2:]
    else:
        return merged_lst + lst1[i1:]


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['math', 'datetime', 'Any'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'disable': ['forbidden-import', 'too-many-branches'],
        'max-line-length': 120
    })
