from django.views.generic import TemplateView, ListView

from delicious_project.delicious.models import Recipe, Category


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
    model = Category
    template_name = 'categories.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['categories'] = context['category_list']
        return context


class ShowRecipesByCategoryView(ListView):
    model = Recipe
    template_name = 'recipes.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        slug = self.kwargs['slug']
        context['recipes'] = Recipe.objects.filter(category__slug=slug)
        return context
