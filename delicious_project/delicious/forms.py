from django import forms

from delicious_project.common.helpers import DisabledFieldsFormMixin
from delicious_project.delicious.models import Recipe, Comment, Category


class CreateRecipeForm(forms.ModelForm):
    category = forms.CharField(
        max_length=max(len(x) for x, _ in Category.TYPES),
        initial='Uncategorized',
        widget=forms.Select(
            choices=Category.TYPES,
        )
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields['title'].widget.attrs['placeholder'] = 'Enter title'
        self.fields['ingredients'].widget.attrs['placeholder'] = 'Enter each ingredient on new line'
        self.fields['description'].widget.attrs['placeholder'] = 'How it\'s made?'
        self.fields['picture'].widget.attrs['placeholder'] = 'Enter URL'
        self.fields['preparation_time'].widget.attrs['placeholder'] = 'in minutes'
        self.fields['cooking_time'].widget.attrs['placeholder'] = 'in minutes'

    def save(self, commit=True):
        recipe = super().save(commit=False)
        recipe.user = self.user

        if commit:
            recipe.save()
        return recipe

    class Meta:
        model = Recipe
        fields = ('title', 'ingredients', 'description', 'picture', 'preparation_time', 'cooking_time', 'category')
        widgets = {
            'ingredients': forms.Textarea(
                attrs={
                    'rows': 3,
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'rows': 5,
                }
            ),
        }


class EditRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'ingredients', 'description', 'picture', 'preparation_time', 'cooking_time', 'category')
        widgets = {
            'ingredients': forms.Textarea(
                attrs={
                    'rows': 3,
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'rows': 5,
                }
            ),
        }


class DeleteRecipeForm(DisabledFieldsFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_disabled_fields()

    def save(self, commit=True):
        Recipe.objects.get(pk=self.instance.pk).delete()
        return self.instance

    class Meta:
        model = Recipe
        fields = ('title', 'ingredients', 'description', 'picture', 'preparation_time', 'cooking_time', 'category')
        widgets = {
            'ingredients': forms.Textarea(
                attrs={
                    'rows': 3,
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'rows': 5,
                }
            ),
        }


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Add your comment',
                }
            ),
        }
