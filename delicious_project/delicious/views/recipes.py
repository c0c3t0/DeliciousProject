from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView

from delicious_project.delicious.forms import CreateRecipeForm, EditRecipeForm, DeleteRecipeForm
from delicious_project.delicious.models import Recipe


class UserRecipesView(ListView):
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

    def get_success_url(self, **kwargs):
        return reverse_lazy('details recipe', kwargs={'pk': self.object.pk})


class DetailRecipeView(DetailView):
    model = Recipe
    template_name = 'delicious/recipe_details.html'
    context_object_name = 'recipe'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['is_owner'] = self.object.user == self.request.user
    #     estates = list(Estate.objects.filter(user_id=self.object.user_id))
    #     context.update({
    #         'estates': estates,
    #     })
    #     return context


class DeleteRecipeView(LoginRequiredMixin, CreateView, DeleteView):
    model = Recipe
    form_class = DeleteRecipeForm
    template_name = 'delicious/recipe_delete.html'
    success_url = reverse_lazy('home')
