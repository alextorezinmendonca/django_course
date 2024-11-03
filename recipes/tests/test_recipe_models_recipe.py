from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError
from parameterized import parameterized
from recipes.models import Recipe

class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        recipe = Recipe(
            category = self.make_category(name='Test Default category'),
            author = self.make_author(username='newuser'),
            title = 'Recipe Titlex',
            description = 'description',
            preparation_time = '10',
            preparation_time_unit = 'minutes',
            slug = 'title-slug',
            servings = 5,
            servings_unit = 'slice',
            preparation_steps = 'Recipe Preparation steps',
            cover = '',
        )
        recipe.full_clean()
        recipe.save()
        return recipe
    
    @parameterized.expand([
        ('title',50),
        ('description',150),
        ('preparation_time_unit',20),
        ('servings_unit',20),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steips_is_htmk_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.preparation_steps_is_html)
        
    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.is_published, msg='is_published is not False')

    def test_recipe_string_representation(self):
        self.recipe.title = 'Testing Representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'Testing Representation')


    #Category
    def test_category_string_representation(self):
        self.recipe.title = 'Testing Representation'
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'Testing Representation')