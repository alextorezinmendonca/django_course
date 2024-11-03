from django.shortcuts import render, get_list_or_404, get_object_or_404
from utils.recipes.factory import make_recipe
from .models import Category, Recipe
from django.http import HttpResponse, Http404
from django.db.models import Q

def home(request):
    recipes = Recipe.objects.filter(
                    is_published=True,
                ).order_by('-id')
    return render(request, 'recipes/pages/home.html', context = {
                                                            'recipes': [recipe for recipe in recipes],
    })


def recipe(request, id):
    recipe = get_object_or_404(Recipe,
                                pk=id, 
                                is_published=True,
                            )
    return render(request, 'recipes/pages/recipe-view.html', context = {
                                                            'recipe': recipe,
                                                            'is_detail_page': True,
    })


def category(request, category_id):
    # recipes = Recipe.objects.filter(
    #     category__id=category_id, 
    #     is_published=True,
    # ).order_by('-id')
    # if not recipes:
    #     raise Http404('Not found 🤷‍♀️')
    
    # category_name = getattr(
    #     getattr(recipes.first(), 'category', None), 
    #     'name', 
    #     'Not found'
    # ) 

    # if not recipes:
    #     return HttpResponse(content='Not found', status=404)

    recipes = get_list_or_404(
        Recipe.objects.filter( #noaq
            category__id=category_id, 
            is_published=True,
        ).order_by('-id')
    )

    return render(request, 'recipes/pages/category.html', context = {
        'recipes': [recipe for recipe in recipes],
        'title': f'{recipes[0].category.name}  - Category |',
    })

def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()
    
    recipes = Recipe.objects.filter(
        Q(title__icontains=search_term) | Q(description__icontains=search_term), #Filter with OR function
        is_published=True, 
        ).order_by('-id')
    
    return render(request, 'recipes/pages/search.html', {
                    'page_title': f'Search for "{search_term}" | ',
                    'search_term': search_term,
                    'recipes': recipes,
    })
