from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from delicious_project.accounts.forms import AddCommentForm
from delicious_project.delicious.models import Comment, Recipe


class AddCommentView(LoginRequiredMixin, CreateView):
    form_class = AddCommentForm
    template_name = 'delicious/recipe_comment.html'


    def get_success_url(self, **kwargs):
        return reverse_lazy('add comment', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        comment = Comment(
            text=form.cleaned_data['text'],
            recipe=recipe,
            user=self.request.user,
        )
        comment.save()

        return redirect('add comment', recipe.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        context['recipe'] = recipe
        comments_count = len(recipe.comment_set.all())

        context['comments'] = recipe.comment_set.all()
        context.update({'comments_count': comments_count,})

        return context