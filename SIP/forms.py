from django import forms
from django.utils import timezone

from .models import Cocktail, Review, Star , Tag, \
    CocktailIngredient


class CocktailIngredientForm(forms.ModelForm):
    class Meta:
        model = CocktailIngredient
        fields = [
            'ingredient',
            'measure'
        ]


CocktailIngredientFormSet = forms.inlineformset_factory(Cocktail,
                                                        CocktailIngredient,
                                                        form=CocktailIngredientForm,
                                                        extra=15,
                                                        can_delete=False)


class CocktailForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cocktail_tag'].initial = 'u'
        self.fields['date_modified'].initial = timezone.now

    class Meta:
        model = Cocktail
        fields = [
            'name',
            'instructions',
            'date_modified',
            'user_uploaded_image',
            'cocktail_tag'
        ]

        widgets = {
            'cocktail_tag': forms.HiddenInput(),
            'date_modified': forms.HiddenInput(),
            'user_uploaded_image': forms.FileInput(attrs={'accept': '.png,.jpg,.jpeg'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        instructions = cleaned_data.get('instructions')
        if not name:
            raise forms.ValidationError('You must enter a name.')
        if not instructions:
            raise forms.ValidationError('You must enter instructions.')
        return cleaned_data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'message',
        ]

    def clean(self):
        cleaned_data = super().clean()
        message = cleaned_data.get('message')
        if not message:
            raise forms.ValidationError('You must enter a message.')
        return cleaned_data

    def save(self, commit=True):
        review = super().save(commit=False)
        review.message = self.cleaned_data['message']
        if commit:
            review.save()
        return review


class StarForm(forms.ModelForm):
    class Meta:
        model = Star
        fields = [
            'score',
        ]

    def clean(self):
        cleaned_data = super().clean()
        score = cleaned_data.get('score')
        if not score:
            raise forms.ValidationError('You must enter a score.')
        return cleaned_data

    def save(self, commit=True):
        # Get the score directly from the form's data
        score = self.data.get('score')
        if not score:
            raise forms.ValidationError('You must enter a score.')

        star = super().save(commit=False)
        star.score = score  # Use the score obtained from the form's data
        if commit:
            star.save()
        return star
