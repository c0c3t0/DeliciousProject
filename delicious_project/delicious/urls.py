from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from delicious_project.delicious.views.comments import AddCommentView
from delicious_project.delicious.views.generic import HomeView, ShowAllRecipesView, ShowCategoryView, \
    ShowBreakfastRecipesView, ShowDrinksRecipesView, ShowLunchRecipesView, ShowDinnerRecipesView, \
    ShowDessertRecipesView, ShowAppetizersRecipesView
from delicious_project.delicious.views.recipes import CreateRecipeView, EditRecipeView, DetailRecipeView, \
    DeleteRecipeView, UserRecipesView, cooked_recipe

urlpatterns = [
                  path('', HomeView.as_view(), name='home'),

                  path('category/', ShowCategoryView.as_view(), name='show category'),
                  path('category/breakfast/', ShowBreakfastRecipesView.as_view(), name='breakfast'),
                  path('category/lunch/', ShowLunchRecipesView.as_view(), name='lunch'),
                  path('category/dinner/', ShowDinnerRecipesView.as_view(), name='dinner'),
                  path('category/dessert/', ShowDessertRecipesView.as_view(), name='dessert'),
                  path('category/appetizers/', ShowAppetizersRecipesView.as_view(), name='appetizers'),
                  path('category/drinks/', ShowDrinksRecipesView.as_view(), name='drinks'),

                  path('all-recipies/', ShowAllRecipesView.as_view(), name='all recipes'),
                  path('add/', CreateRecipeView.as_view(), name='add recipe'),
                  path('my-recipes/<int:pk>/', UserRecipesView.as_view(), name='user recipes'),
                  path('edit/<int:pk>/', EditRecipeView.as_view(), name='edit recipe'),
                  path('details/<int:pk>/', DetailRecipeView.as_view(), name='details recipe'),
                  path('delete/<int:pk>/', DeleteRecipeView.as_view(), name='delete recipe'),
                  path('photo/cooked/<int:pk>', cooked_recipe, name='cooked'),

                  path('comment/<int:pk>/', AddCommentView.as_view(), name='add comment')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
