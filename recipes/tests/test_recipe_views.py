from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Category, Recipe, User


class RecipeViewTest(TestCase):
    # Home Tests
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_templates_show_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipes found here',
            response.content.decode('utf-8'))
        
    def test_recipe_home_template_loads_recipes(self):
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
                                          first_name='user',
                                          last_name='name',
                                          username='username',
                                          password='123456',
                                          email='username@email.com',
                                          )
        recipe = Recipe.objects.create(
                category = category,
                author = author,
                title = 'Recipe Title',
                description = 'description',
                preparation_time = '10',
                preparation_time_unit = 'minutes',
                slug = 'title-slug',
                servings = 5,
                servings_unit = 'slice',
                preparation_steps = 'Recipe Preparation steps',
                preparation_steps_is_html = False,
                is_published = True,
                cover = '',
        )
        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertEqual(response_context_recipes[0].title, 'Recipe Title' )
        self.assertIn('Recipe Title', content)
        self.assertIn('10 minutes', content)
        self.assertIn('5 slice', content)
        self.assertEqual(len(response_context_recipes), 1)

    # Category Tests
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)


    # Recipe Tests
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)   

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)
