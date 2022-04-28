from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView

from delicious_project.delicious.forms import CreateRecipeForm, EditRecipeForm, DeleteRecipeForm
from delicious_project.delicious.models import Recipe


class UserRecipesView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'delicious/user_recipes.html'

    def get_queryset(self):
        recipes = Recipe.objects.filter(user_id=self.request.user)
        return recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #     context['is_owner'] = self.object.user == self.request.user
        recipes = list(Recipe.objects.filter(user_id=self.request.user))

        context.update({
            'recipes': recipes,
        })
        return context


class CreateRecipeView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = CreateRecipeForm
    template_name = 'delicious/create_recipe.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self, **kwargs):
        return reverse_lazy('details recipe', kwargs={'pk': self.object.id})


class EditRecipeView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = EditRecipeForm
    template_name = 'delicious/recipe_edit.html'

    def get_success_url(self):
        recipe_id = self.kwargs['pk']
        return reverse_lazy('details recipe', kwargs={'pk': recipe_id})


class DetailRecipeView(DetailView):
    model = Recipe
    template_name = 'delicious/recipe_details.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_owner'] = self.object.user == self.request.user
        context['is_anonymous'] = not self.request.user.is_authenticated

        return context


class DeleteRecipeView(LoginRequiredMixin, CreateView, DeleteView):
    model = Recipe
    form_class = DeleteRecipeForm
    template_name = 'delicious/recipe_delete.html'

    def get_success_url(self):
        return reverse_lazy('all recipes')


def cooked_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    recipe = get_object_or_404(Recipe, id=recipe.pk)

    if request.user in recipe.cooked.all():
        recipe.cooked.remove(request.user)
    else:
        recipe.cooked.add(request.user)

    return HttpResponseRedirect(reverse('details recipe', args=[str(pk)]))
