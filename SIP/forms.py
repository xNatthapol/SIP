from django import forms
from django.forms import SelectMultiple
from django.utils import timezone
from django.utils.html import conditional_escape

from .models import Cocktail, Review, Star , Tag, \
    CocktailIngredient

MEASURE_UNIT_CHOICES = [
    ('grams', 'Grams'),
    ('ounces', 'Ounces'),
    ('liters', 'Liters'),
    ('milliliters', 'Milliliters'),
    (None , 'None'),
]

class CocktailIngredientForm(forms.ModelForm):
    measure = forms.CharField(label='measure', widget=forms.TextInput())
    measure_unit = forms.ChoiceField(label='', choices=MEASURE_UNIT_CHOICES, widget=forms.Select(attrs={'class': 'select2'}))
    class Meta:
        model = CocktailIngredient
        fields = [
            'ingredient',
            'measure',
            'measure_unit',
        ]

    def clean(self):
        cleaned_data = super().clean()
        ingredient = cleaned_data.get('ingredient')
        measure = cleaned_data.get('measure')
        measure_unit = cleaned_data.get('measure_unit')
        if not ingredient:
            raise forms.ValidationError('You must enter an ingredient.')
        if not measure:
            raise forms.ValidationError('You must enter a measure.')
        if not measure_unit:
            measure_unit = ''
        return cleaned_data

    def save(self, commit=True):
        cocktail_ingredient = super().save(commit=False)
        cocktail_ingredient.ingredient = self.cleaned_data['ingredient']
        cocktail_ingredient.measure = self.cleaned_data['measure'] + self.cleaned_data['measure_unit']
        if commit:
            cocktail_ingredient.save()
        return cocktail_ingredient


CocktailIngredientFormSet = forms.inlineformset_factory(Cocktail,
                                                        CocktailIngredient,
                                                        form=CocktailIngredientForm,
                                                        extra=15,
                                                        can_delete=False)


class CocktailForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=SelectMultiple(attrs={'class': 'select2'}),
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
            'tags',
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
        user_uploaded_image = cleaned_data.get('user_uploaded_image')
        if not name:
            raise forms.ValidationError('You must enter a name.')
        if not instructions:
            raise forms.ValidationError('You must enter instructions.')
        if not user_uploaded_image:
            raise forms.ValidationError('You must upload an image.')

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
