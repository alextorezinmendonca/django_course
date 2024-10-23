from django.urls import path
from recipes.views import home, about, contact


urlpatterns = [
    path('', home),
    path('sobre/', about),
    path('contato', contact),
]
