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
import tkinter as tk
import random
import csv
from tkinter import ttk, messagebox, simpledialog
from graph import Graph
from user import User
from recipe import Recipe
from review import Review


class FoodRecommenderStartPage(tk.Frame):
    """The main screen that shows up when the program is run.
    Instance Attributes:
    - random_recipes:
        random dictionary of recipes the user can select from
    - picked_recipes:
        list of recipes that the user picked
    - recipe_listbox:
        listbox that contains and displays the random recipes the user can select from
    - picked_recipes_listbox:
        listbox that contains and displays the recipes the user has chose
    - add_button:
        allow the user to add recipes to their picked_recipes list
    - delete_button:
        allow the user to delete recipes from their picked_recipes list
    """
    random_recipes: dict[str:Recipe]
    picked_recipes: list[Recipe]
    recipe_listbox: tk.Listbox
    picked_recipes_listbox: tk.Listbox
    add_button: ttk.Button
    delete_button: ttk.Button
    next_button: ttk.Button

    def __init__(self, parent: tk.Tk, graph: Graph, *args, **kwargs) -> None:
        """ Create the Start Page Frame"""

        # Initialize variables
        self.random_recipes = {}
        self.picked_recipes = []

        tk.Frame.__init__(self, parent, *args, **kwargs)
        parent.title("Food Recommender")

        # Set font
        font = ("Century Gothic", 12)

        # Set background color for start frame
        self.configure(background="#AAA1C8")

        # Label and introduction
        header = ttk.Label(self, text="Welcome to MealMate", style="Header.TLabel")
        header.pack(side="top")
        intro = ttk.Label(self,
                          text="Helping you with you recipe needs. \nTo begin, please "
                               "generate recipes and select 5 that interest you",
                          style="Text.TLabel")
        intro.configure(justify="center")
        intro.pack(side="top")

        subheader_recipe = ttk.Label(self, text="Options:", style="Subheader.TLabel")
        subheader_recipe.pack(pady=10)

        # Recipe Listbox
        self.recipe_listbox = tk.Listbox(self, height=5, width=50, font=font)
        self.recipe_listbox.pack(pady=10)

        subheader_picked_recipe = ttk.Label(self, text="Your Recipes:", style="Subheader.TLabel")
        subheader_picked_recipe.pack(pady=10)

        # Picked Recipes Listbox
        self.picked_recipes_listbox = tk.Listbox(self, height=5, width=50, font=font)
        self.picked_recipes_listbox.pack(pady=10)

        self.create_buttons(graph=graph, parent=parent)

    def create_buttons(self, graph: Graph, parent: tk.Tk) -> None:
        """Creates interactive buttons on the Start screen"""
        generate_button = ttk.Button(self, text="Generate Recipes",
                                     command=lambda: self.generate_recipes(graph), style="Custom.TButton")
        generate_button.pack(pady=10, padx=30)

        # Add Recipe button
        self.add_button = ttk.Button(self, text="Add Recipe", command=self.add_recipe, style="Custom.TButton",
                                     state="disabled")
        self.add_button.pack(side="left", padx=60)

        # Delete Recipe button
        self.delete_button = ttk.Button(self, text="Delete Recipe", command=self.delete_recipe, style="Custom.TButton",
                                        state="disabled")
        self.delete_button.pack(side="left", padx=60)

        # Next Button
        self.next_button = ttk.Button(self, text="Next",
                                      command=lambda: self.open_recommendations(graph=graph, parent=parent),
                                      style="Custom.TButton",
                                      state="disabled")
        self.next_button.pack(side="left", padx=60)

    def add_recipe(self) -> None:
        """Adds selected recipe to the user's recipes list.
                This button is disabled when there are already 5 recipes in the user's list.
                """
        selected_recipe = self.recipe_listbox.get(tk.ACTIVE)

        # Only add the recipe if it's not already in the picked recipes list
        picked_recipe = self.random_recipes[selected_recipe]
        if selected_recipe == '' or picked_recipe in self.picked_recipes:
            return
        # Add the recipe to the picked recipes list
        self.picked_recipes.append(picked_recipe)

        # Update the picked recipes listbox
        self._update_list()
        self.check_button_state()

    def delete_recipe(self) -> None:
        """Deletes a selected recipe from the user's list.
               When no recipe is selected, deletes the most recent recipe from user's list.
               A confirmation screen will pop up if user decides to delete a recipe.
               Button is disabled when there are no recipes in user's list."""
        # Get the index of the selected recipe in the listbox
        selected_recipe = self.picked_recipes_listbox.get(tk.ACTIVE)

        # Ask the user for confirmation before deleting the recipe
        answer = messagebox.askyesno("Confirm Deletion",
                                     f"Are you sure you want to delete '{selected_recipe}' from your selected recipes?")
        if answer:
            # Remove the recipe from the picked_recipes list
            for recipe in self.picked_recipes:
                if recipe.name == selected_recipe:
                    self.picked_recipes.remove(recipe)
            self._update_list()
            self.check_button_state()

    def check_button_state(self) -> None:
        """Enables/Disables buttons depending on number of recipes in user's list."""
        # Check if there is at least one recipe to enable the Delete button
        if len(self.picked_recipes) > 0:
            self.delete_button["state"] = "normal"

        # Check if there are 5 recipes in picked_recipes to enable the Next button
        if len(self.picked_recipes) >= 5:
            self.add_button["state"] = "disable"
            self.next_button["state"] = "normal"
        else:
            self.add_button["state"] = "normal"
            self.next_button["state"] = "disable"

    def _update_list(self) -> None:
        """Updates user's list of recipes in the listbox"""
        self.picked_recipes_listbox.delete(0, tk.END)
        for recipe in self.picked_recipes:
            self.picked_recipes_listbox.insert(tk.END, recipe.name)

    def generate_recipes(self, graph: Graph) -> None:
        """On the beginning screen randomly generates 5 recipes
                for the user to pick from.
                Recipes can be added or deleted or skipped."""
        self.recipe_listbox.delete(0, tk.END)
        self.random_recipes.clear()
        len_random = 0
        while len_random < 5:
            recipe = random.choice(list(graph.recipe_nodes.values()))
            self.random_recipes[recipe.name] = recipe
            len_random += 1
        for recipe in self.random_recipes:
            self.recipe_listbox.insert(tk.END, recipe)

        if len(self.picked_recipes) != 5:
            self.add_button["state"] = "normal"

    def open_recommendations(self, graph: Graph, parent: tk.Tk) -> None:
        """Open a RecipeGridFrame so the user can browse recommendations"""
        self.destroy()
        new_user = User(max(graph.user_nodes.keys()) + 1)
        graph.add_user(new_user)
        for recipe in self.picked_recipes:
            graph.rate_recommendation(user=new_user, recipe=recipe, rating=5)
        similar_user = random.choice(graph.get_similar_users(new_user))
        recommendations = []
        while len(recommendations) < 1:
            similar_user = random.choice(graph.get_similar_users(new_user))
            recommendations = graph.get_recommendations(new_user, similar_user)
        frame = RecipeGridFrame(parent=parent, recommendations=recommendations, user=new_user, graph=graph)
        frame.pack_propagate(False)
        frame.pack()


class RecipeGridFrame(tk.Frame):
    """The main screen that shows up when the program is run.
        Instance Attributes:
        - parent:
            main window for the GUI
        - recipes:
            list of recommended recipes
        - graph:
            graph containing other users and recipes to reccommend recipes based on user preference
        - user:
           the current user with the given recommendations
        - recipe_window:
            a window for the recipe the user selects
        Representation Invariants:
        - graph.user_nodes != {}
        - graph.recipe_nodes != {}
        - graph.links != []
        - user in graph.user_nodes
        - all(recommendation in graph.recipe_nodes for recommendation in recommendations)
        - len(recommendations) > 0
        """
    parent: tk.Tk
    recommendations: list[Recipe]
    graph: Graph
    user: User
    recipe_window: tk.Toplevel

    def __init__(self, parent: tk.Tk, recommendations: list[Recipe], user: User, graph: Graph, *args, **kwargs) -> None:
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.recommendations = recommendations
        self.graph = graph
        self.user = user

        # Set background color for start frame
        self.configure(background="#AAA1C8")
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

        header = ttk.Label(self, text="Here are your recommendations", style="Header.TLabel")
        header.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="n")

        intro = ttk.Label(self, text="Click on a recipe to view and feel free to rate", style="Text.TLabel")
        intro.configure(justify="center")
        intro.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="n")

        refresh = ttk.Button(self, text="Refresh", command=lambda: self.refresh_page(user=user, graph=graph),
                             style="Custom.TButton")
        refresh.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="n")

        self.create_widgets()

    def create_widgets(self) -> None:
        """Creates buttons for each recipe"""
        for i in range(0, min(len(self.recommendations), 9)):
            recipe = self.recommendations[i]
            button = ttk.Button(self, text=recipe.name,
                                command=lambda curr_recipe=recipe: self.open_recipe(curr_recipe),
                                style="Custom.TButton")
            button.grid(row=4 + i, column=1, padx=2, pady=10, sticky="w")
            num = ttk.Label(self, text=str(i + 1) + ".", style="Text.TLabel")
            num.grid(row=4 + i, column=0, padx=2, pady=10, sticky="w")

    def open_recipe(self, recipe: Recipe) -> None:
        """Opens the recommeended recipe in a new window.
                Displays all the recipe's attributes.
        """
        # main frame
        self.recipe_window = tk.Toplevel(self)
        self.recipe_window.title(recipe.name)
        self.recipe_window.geometry('800x500')
        self.recipe_window.resizable(False, False)
        self.recipe_window.pack_propagate(False)
        self.recipe_window.configure(background="#967AA1")

        widget_frame = ttk.Frame(self.recipe_window)
        widget_frame.pack(fill=tk.BOTH, expand=True)

        # add scrollbar
        scrollbar = ttk.Scrollbar(widget_frame, orient=tk.VERTICAL)
        scrollbar.pack(side='right', fill='y')

        # create a canvas and attach it to the scrollbar
        canvas = tk.Canvas(widget_frame, yscrollcommand=scrollbar.set)
        canvas.configure(bg="#967AA1")
        canvas.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=canvas.yview)

        # create another frame inside the canvas to hold the widgets
        inner_frame = tk.Frame(canvas)
        inner_frame.configure(background="#D5C6E0")
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        header = ttk.Label(inner_frame, text=recipe.name, style="HeaderDark.TLabel")
        header.configure(justify="center")
        header.pack(side='top', fill='both')

        submission_text = "   " + f'Submitted by {recipe.contributor_id} on {recipe.submitted_date}'
        submitted_by = ttk.Label(inner_frame, text=submission_text, style="TextDark.TLabel")
        submitted_by.configure(anchor='w')
        submitted_by.pack(fill='both')

        if len(recipe.description) > 100:
            n = len(recipe.description) // 90
            desc = (recipe.description[i * 90:(i + 1) * 90] for i in range(0, n + 1))
            desc_text = ""
            for d in desc:
                desc_text += "     " + d.strip() + "\n"
            # recipe.description[0:90] + '\n' + recipe.description[90:]
        else:
            desc_text = "     " + recipe.description
        description = ttk.Label(inner_frame, text=desc_text + "\n", style="TextDark.TLabel")
        description.configure(anchor='w')
        description.pack(fill='both')

        self.recipe_text(recipe=recipe, inner_frame=inner_frame)

        rate_recipe = ttk.Button(self.recipe_window, text="Rate this Recipe",
                                 command=lambda: self.rate_recipe(self.graph, self.user, recipe),
                                 style="Custom.TButton")
        rate_recipe.pack(anchor='se')

        # update the canvas to show the widgets
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        self.recipe_window.protocol(name="WM_DELETE_WINDOW", func=lambda window=self.recipe_window: window.destroy())

    def recipe_text(self, recipe: Recipe, inner_frame: tk.Frame) -> None:
        """ (Helper Function) Helps display the recipe's attributes
        """
        time_subheader = ttk.Label(inner_frame, text='Time to make:', style="SubheaderDark.TLabel")
        time_subheader.configure(anchor='w')
        time_subheader.pack(fill='both')

        time_text = "     " + str(recipe.minutes)
        time_label = ttk.Label(inner_frame, text=time_text + " minutes\n", style="TextDark.TLabel")
        time_label.configure(anchor='w')
        time_label.pack(fill='both')

        nutrition_subheader = ttk.Label(inner_frame, text='Nutrition Facts:', style="SubheaderDark.TLabel")
        nutrition_subheader.configure(anchor='w')
        nutrition_subheader.pack(fill='both')

        nutrition_text = ''
        for nutrition in recipe.nutrition:
            nutrition_text += "     " + f'{nutrition}: {recipe.nutrition[nutrition]}\n'
        nutrition_label = ttk.Label(inner_frame, text=nutrition_text, style="TextDark.TLabel")
        nutrition_label.configure(anchor='w')
        nutrition_label.pack(fill='both')

        ingredients_subheader = ttk.Label(inner_frame, text='Ingredients', style="SubheaderDark.TLabel")
        ingredients_subheader.configure(anchor='w')
        ingredients_subheader.pack(fill='both')

        n_ingredients = ttk.Label(inner_frame, text=f'Number of Ingredients: {recipe.n_ingredients}',
                                  style="TextDark.TLabel")
        n_ingredients.configure(anchor='w')
        n_ingredients.pack(fill='both')

        ingredients_text = ''
        ingredient_num = 1
        for ingredient in recipe.ingredients:
            ingredient = ingredient.strip("'") + '\n'
            ingredients_text += "   " + str(ingredient_num) + ". " + ingredient
            ingredient_num += 1
        ingredients = ttk.Label(inner_frame, text=ingredients_text, style="TextDark.TLabel")
        ingredients.configure(anchor='w')
        ingredients.pack(fill='both')

        steps_subheader = ttk.Label(inner_frame, text='Steps', style="SubheaderDark.TLabel")
        steps_subheader.configure(anchor='w')
        steps_subheader.pack(fill='both')

        n_steps = ttk.Label(inner_frame, text=f'Number of steps: {recipe.n_steps}', style="TextDark.TLabel")
        n_steps.configure(anchor='w')
        n_steps.pack(fill='both')

        steps = ''
        step_num = 1
        for step in recipe.steps:
            step = step.strip("'") + '\n'
            if len(step) > 90:
                step = step[0:90] + '\n        -' + step[90:]
            steps += "   " + str(step_num) + ". " + step
            step_num += 1
        steps_text = ttk.Label(inner_frame, text=steps, style="TextDark.TLabel")
        steps_text.configure(anchor='w')
        steps_text.pack(fill='both')

    def refresh_page(self, user: User, graph: Graph) -> None:
        """Re-recommends recipes to the user."""
        self.destroy()
        recommendations = []
        while len(recommendations) < 1:
            similar_user = random.choice(graph.get_similar_users(user))
            recommendations = graph.get_recommendations(user, similar_user)
        frame = RecipeGridFrame(parent=self.parent, recommendations=recommendations, user=user, graph=graph)
        frame.pack()

    def rate_recipe(self, graph: Graph, user: User, recipe: Recipe) -> None:
        """Allows the user to give a rating to the selected recipe, an integer from 1 to 5."""
        while True:
            rating = simpledialog.askinteger(title='Rating', prompt='How would you rate this recipe from 1 to 5?')
            try:
                rating = int(rating)
            except ValueError:
                messagebox.showinfo("Valid number, please")
            if not 1 <= rating <= 5:
                messagebox.showinfo(title="Error", message="Please enter a value between 1 and 5 inclusive")
            else:
                break
        messagebox.showinfo(title='Thanks', message="Thank you for your rating!")
        graph.rate_recommendation(user=user, recipe=recipe, rating=rating)


class MainApplication(tk.Tk):
    """ Main Window where all the frames go and styling is set
    """

    def __init__(self, *args, **kwargs) -> None:
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("700x700")
        self.configure(bg="#AAA1C8")
        self.resizable(False, False)

        # Custom style for buttons and labels
        style = ttk.Style()
        style.configure("Custom.TButton", font=("Century Gothic", 12), background="#D5C6E0")
        style.configure("Header.TLabel", font=("Century Gothic", 25, 'bold'), background="#AAA1C8", foreground="white")
        style.configure("Text.TLabel", font=("Century Gothic", 12), background="#AAA1C8", foreground="white")
        style.configure("Subheader.TLabel", font=("Century Gothic", 18, 'bold'), background="#AAA1C8",
                        foreground="white")

        # Darker background
        style.configure("SubheaderDark.TLabel", font=("Century Gothic", 18, 'bold'), background="#967AA1",
                        foreground="white")
        style.configure("TextDark.TLabel", font=("Century Gothic", 12), background="#967AA1", foreground="white")
        style.configure("HeaderDark.TLabel", font=("Century Gothic", 22, 'bold'), background="#967AA1",
                        foreground="white")

        # Create the start page
        graph = generate_graph()
        start_page = FoodRecommenderStartPage(parent=self, graph=graph)
        start_page.pack(expand=True, fill="both")


##########################################################
# Top Level Functions
##########################################################
def read_interactions(graph: Graph, csv_file: str) -> None:
    """Given a csv file containg review information, reads it and parses it.
       Creates user objects and its attributes.
       Creates review objects and its attributes.
       Adds user and review objects to the graph.
       Representation Invariants:
       - csv_file is formatted as seen in Datasets/RAW_interactions
       """
    with open(csv_file, newline='', encoding="utf8") as file:
        reader = csv.reader(file)
        next(reader)

        # user_id, recipe_id, date, rating, review
        for row in reader:
            user_id = int(row[0])
            if user_id not in graph.user_nodes.keys():
                user = User(user_id)
                graph.add_user(user)
            recipe_id = int(row[1])
            date = row[2]
            rating = int(row[3])
            review = row[4]
            new_review = Review(user_id, recipe_id, date, rating, review)
            graph.add_link(new_review)


def read_recipes(graph: Graph, csv_file: str) -> None:
    """Given a csv file containing recipe information, reads it in and parses it.
        Creates the recipe object and its attributes.
        Adds recipe object to the graph.
        Representation Invariants:
       - csv_file is formatted as seen in Datasets/RAW_recipes
        """
    with open(csv_file, newline='', encoding="utf8") as file:
        reader = csv.reader(file)
        next(reader)
        # name,id,minutes,contributor_id,submitted,tags,nutrition,n_steps,steps,description,ingredients,n_ingredients
        for row in reader:
            tags = row[5].strip('][').split(', ')
            nutrition = row[6].strip('][').split(', ')
            n_steps = int(row[7])

            steps = row[8].strip('][')
            steps = steps.split("', '")

            description = row[9]
            ingredients = row[10].strip('][').split(', ')
            n_ingredients = int(row[11])
            new_recipe = Recipe(name=row[0], recipe_id=int(row[1]), minutes=int(row[2]), contributor_id=int(row[3]),
                                submitted_date=row[4], tags=tags, nutrition_lst=nutrition, n_steps=n_steps,
                                steps=steps, description=description, ingredients=ingredients,
                                n_ingredients=n_ingredients)
            graph.add_recipe(new_recipe)


def generate_graph() -> Graph():
    """Initializes the graph and calls function to start adding nodes and edges to the graph."""
    graph = Graph()
    read_recipes(graph=graph, csv_file='Dataset/RAW_recipes.csv')
    read_interactions(graph=graph, csv_file='Dataset/RAW_interactions.csv')
    return graph


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['random', 'tkinter', 'csv', 'graph', 'user', 'recipe', 'review'],
        'max-line-length': 120,
        'allow-io': ['read_interactions', 'read_recipes'],
        'disable': ['E9969', 'E9998', 'too-many-locals']
    })
