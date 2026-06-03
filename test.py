import pytest
from recipes import DietaryRecipe, Ingredient, Recipe, ShoppingList

def test_ingredient_creation_and_str():
    ingredient = Ingredient("Мука", 500, "г")

    assert ingredient.name == "Мука"
    assert ingredient.quantity == 500.0
    assert ingredient.unit == "г"
    assert str(ingredient) == "Мука: 500.0 г"

def test_ingredient_equality():
    assert Ingredient("Мука", 500, "г") == Ingredient("Мука", 100, "г")
    assert Ingredient("Мука", 500, "г") != Ingredient("Сахар", 500, "г")
    assert Ingredient("Мука", 500, "г") != Ingredient("Мука", 500, "кг")

def test_ingredient_quantity_must_be_positive():
    with pytest.raises(ValueError):
        Ingredient("Мука", 0, "г")

def test_recipe_creation_and_add_ingredient():
    flour = Ingredient("Мука", 500, "г")
    recipe = Recipe("Пицца", [flour])

    assert recipe.title == "Пицца"
    assert recipe.ingredients == [flour]

    recipe.add_ingredient(Ingredient("Сыр", 200, "г"))
    recipe.add_ingredient(Ingredient("Мука", 100, "г"))

    assert len(recipe) == 2
    assert recipe.ingredients[0].quantity == 600.0

def test_recipe_scale():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    scaled_recipe = recipe.scale(2)

    assert scaled_recipe is not recipe
    assert scaled_recipe.ingredients[0].quantity == 1000.0
    assert recipe.ingredients[0].quantity == 500.0

    with pytest.raises(ValueError):
        recipe.scale(0)

def test_shopping_list_add_recipe_and_remove_recipe():
    recipe = Recipe("Пицца", [Ingredient("Мука", 500, "г")])
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 2)

    assert shopping_list.get_list() == [Ingredient("Мука", 1000, "г")]

    shopping_list.remove_recipe("Пицца")
    assert shopping_list.get_list() == []

    shopping_list.remove_recipe("Несуществующий рецепт")

    with pytest.raises(ValueError):
        shopping_list.add_recipe(recipe, 0)


def test_shopping_list_get_list():
    pizza = Recipe(
        "Пицца",
        [Ingredient("Мука", 500, "г"), Ingredient("Сыр", 200, "г")],
    )
    pie = Recipe(
        "Пирог",
        [Ingredient("Мука", 300, "г"), Ingredient("Яблоки", 3, "шт")],
    )
    shopping_list = ShoppingList()
    shopping_list.add_recipe(pizza, 1)
    shopping_list.add_recipe(pie, 1)

    assert shopping_list.get_list() == [
        Ingredient("Мука", 800, "г"),
        Ingredient("Сыр", 200, "г"),
        Ingredient("Яблоки", 3, "шт"),
    ]

def test_shopping_list_addition():
    first_list = ShoppingList()
    second_list = ShoppingList()
    first_list.add_recipe(Recipe("Пицца", [Ingredient("Сыр", 200, "г")]), 1)
    second_list.add_recipe(Recipe("Пирог", [Ingredient("Мука", 300, "г")]), 1)

    combined_list = first_list + second_list

    assert combined_list.get_list() == [
        Ingredient("Мука", 300, "г"),
        Ingredient("Сыр", 200, "г"),
    ]
    assert len(first_list.get_list()) == 1
    assert len(second_list.get_list()) == 1

def test_dietary_recipe():
    recipe = DietaryRecipe(
        "Овощной салат",
        "веган",
        [Ingredient("Помидоры", 2, "шт")],
    )
    scaled_recipe = recipe.scale(2)

    assert isinstance(scaled_recipe, DietaryRecipe)
    assert scaled_recipe.diet_type == "веган"
    assert scaled_recipe.ingredients[0].quantity == 4.0
    assert str(recipe).startswith("[веган] Овощной салат")

