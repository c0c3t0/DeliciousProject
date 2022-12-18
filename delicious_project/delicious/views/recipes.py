from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView, ListView
from django.views.generic.edit import FormMixin

from delicious_project.delicious.forms import CreateRecipeForm, EditRecipeForm, DeleteRecipeForm, AddCommentForm
from delicious_project.delicious.models import Recipe, Comment


class DetailRecipeView(FormMixin, DetailView):
    model = Recipe
    template_name = 'delicious/recipe_details.html'
    form_class = AddCommentForm
    context_object_name = 'recipe'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        comment = Comment(
            text=form.cleaned_data['text'],
            recipe=recipe,
            user=self.request.user,
        )
        comment.save()
        messages.success(self.request, 'Comment has been posted successfully!')

        return redirect('details recipe', recipe.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])

        context['recipe'] = recipe
        comments_count = len(recipe.comment_set.all())

        context['is_owner'] = self.object.user == self.request.user
        context['is_anonymous'] = not self.request.user.is_authenticated
        context['comments'] = recipe.comment_set.all()
        context.update({'comments_count': comments_count, })

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
        messages.success(self.request, 'Recipe has been added successfully!')
        return reverse_lazy('details recipe', kwargs={'pk': self.object.id})


class EditRecipeView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = EditRecipeForm
    template_name = 'delicious/recipe_edit.html'

    def get_success_url(self):
        recipe_id = self.kwargs['pk']
        messages.success(self.request, 'Recipe has been updated successfully!')
        return reverse_lazy('details recipe', kwargs={'pk': recipe_id})


class DeleteRecipeView(LoginRequiredMixin, CreateView, DeleteView):
    model = Recipe
    form_class = DeleteRecipeForm
    template_name = 'delicious/recipe_delete.html'

    def get_success_url(self):
        messages.success(self.request, 'Recipe has been deleted successfully!')
        return reverse_lazy('all recipes')


def cooked_recipe(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    recipe = get_object_or_404(Recipe, id=recipe.pk)

    if request.user in recipe.cooked.all():
        recipe.cooked.remove(request.user)
    else:
        recipe.cooked.add(request.user)

    return HttpResponseRedirect(reverse('details recipe', args=[str(pk)]))


class UserRecipesView(LoginRequiredMixin, ListView):
    paginate_by = 6
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


class UserCookedRecipesView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'delicious/user_recipes.html'

    def get_queryset(self):
        recipes = Recipe.objects.filter(cooked=self.request.user)
        return recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipes = list(Recipe.objects.filter(cooked=self.request.user))

        context.update({
            'recipes': recipes,
        })
        return context
