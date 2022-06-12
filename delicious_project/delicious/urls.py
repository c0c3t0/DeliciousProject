from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from delicious_project.delicious.views.comments import AddCommentView
from delicious_project.delicious.views.generic import HomeView, ShowAllRecipesView, ShowCategoryView, \
    ShowRecipesByCategoryView
from delicious_project.delicious.views.recipes import CreateRecipeView, EditRecipeView, DetailRecipeView, \
    DeleteRecipeView, UserRecipesView, cooked_recipe

urlpatterns = [
                  path('', HomeView.as_view(), name='home'),

                  path('category/', ShowCategoryView.as_view(), name='show category'),
                  path('category/<slug:slug>/', ShowRecipesByCategoryView.as_view(), name='category slug'),

                  path('all-recipies/', ShowAllRecipesView.as_view(), name='all recipes'),
                  path('add/', CreateRecipeView.as_view(), name='add recipe'),
                  path('my-recipes/<int:pk>/', UserRecipesView.as_view(), name='user recipes'),
                  path('edit/<int:pk>/', EditRecipeView.as_view(), name='edit recipe'),
                  path('details/<int:pk>/', DetailRecipeView.as_view(), name='details recipe'),
                  path('delete/<int:pk>/', DeleteRecipeView.as_view(), name='delete recipe'),
                  path('photo/cooked/<int:pk>', cooked_recipe, name='cooked'),

                  path('comment/<int:pk>/', AddCommentView.as_view(), name='add comment')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
