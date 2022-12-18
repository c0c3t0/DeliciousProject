from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from delicious_project.delicious.models import Recipe, Category


class HomeView(TemplateView):
    template_name = 'home.html'
    def get(self, request, *args, **kwargs):
        context = {
            'messages': messages.get_messages(request),
        }
        return render(request, self.template_name, context)

class ShowAllRecipesView(ListView):
    paginate_by = 6
    model = Recipe
    template_name = 'recipes.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['recipes'] = Recipe.objects.all()
        context['template_name'] = 'All Recipes'
        return context


class ShowCategoryView(ListView):
    paginate_by = 9
    model = Category
    template_name = 'categories.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['page_obj'] = context['category_list']
        return context


class ShowRecipesByCategoryView(ListView):
    paginate_by = 6
    model = Recipe
    template_name = 'recipes.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        slug = self.kwargs['slug']
        context['page_obj'] = Recipe.objects.filter(category__slug=slug)
        context['template_name'] = slug
        return context
