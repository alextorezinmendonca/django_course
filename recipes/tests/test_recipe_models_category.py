from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError

class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Category Test'
        )
        return super().setUp()

    def test_category_string_representation(self):
        self.category.name = 'Pasta'
        self.category.full_clean()
        self.category.save()
        self.assertEqual(str(self.category), 'Pasta')

    def test_recipe_fields_max_length(self):
        max_length = 50
        field = 'name'
        self.category.name = 'A' * (max_length + 1)
        with self.assertRaises(ValidationError):
            self.category.full_clean()