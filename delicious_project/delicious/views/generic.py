from django.views.generic import TemplateView, ListView

# from delicious_project.delicious.models import Category
from delicious_project.delicious.models import Recipe


class HomeView(TemplateView):
    template_name = 'home.html'


class ShowAllRecipesView(ListView):
    model = Recipe
    template_name = 'recipes.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['recipes'] = Recipe.objects.all()
        return context


class ShowCategoryView(ListView):
    model = Recipe
    template_name = 'categories.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['categories'] = Recipe.DISH_TYPES
        return context


class ShowBreakfastRecipesView(ListView):
    model = Recipe
    template_name = 'recipes.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['recipes'] = Recipe.objects.filter(category='Breakfast')
        return context


class ShowLunchRecipesView(ListView):
    model = Recipe
    template_name = 'recipes.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['recipes'] = Recipe.objects.filter(category='Lunch')
        return context


class ShowDinnerRecipesView(ListView):
    model = Recipe
    template_name = 'recipes.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['recipes'] = Recipe.objects.filter(category='Dinner')
        return context


class ShowDessertRecipesView(ListView):
    model = Recipe
    template_name = 'recipes.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['recipes'] = Recipe.objects.filter(category='Dessert')
        return context


class ShowAppetizersRecipesView(ListView):
    model = Recipe
    template_name = 'recipes.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['recipes'] = Recipe.objects.filter(category='Appetizers')
        return context


class ShowDrinksRecipesView(ListView):
    model = Recipe
    template_name = 'recipes.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['recipes'] = Recipe.objects.filter(category='Drinks')
        return context
