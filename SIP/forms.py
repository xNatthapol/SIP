from django import forms
from .models import Cocktail, Review, Star


class CocktailForm(forms.ModelForm):
    class Meta:
        model = Cocktail
        fields = [
            'name',
            'alternate_name',
            'cocktail_tag',
            'tags',
            'category',
            'glass',
            'instructions',
            'ingredients',
            'image',
            'image_source',
            'image_attribution',
            'date_modified',
        ]

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        alternate_name = cleaned_data.get('alternate_name')
        cocktail_tag = cleaned_data.get('cocktail_tag')
        category = cleaned_data.get('category')
        glass = cleaned_data.get('glass')
        instructions = cleaned_data.get('instructions')
        image = cleaned_data.get('image')
        image_source = cleaned_data.get('image_source')
        image_attribution = cleaned_data.get('image_attribution')
        date_modified = cleaned_data.get('date_modified')
        if not name and not alternate_name:
            raise forms.ValidationError('You must enter a name or alternate name.')
        if not cocktail_tag:
            raise forms.ValidationError('You must enter a cocktail tag.')
        if not category:
            raise forms.ValidationError('You must enter a category.')
        if not glass:
            raise forms.ValidationError('You must enter a glass.')
        if not instructions:
            raise forms.ValidationError('You must enter instructions.')
        if not image:
            raise forms.ValidationError('You must enter an image.')
        if not image_source:
            raise forms.ValidationError('You must enter an image source.')
        if not image_attribution:
            raise forms.ValidationError('You must enter an image attribution.')
        if not date_modified:
            raise forms.ValidationError('You must enter a date modified.')
        return cleaned_data

    def save(self, commit=True):
        cocktail = super().save(commit=False)
        cocktail.name = self.cleaned_data['name']
        cocktail.alternate_name = self.cleaned_data['alternate_name']
        cocktail.cocktail_tag = self.cleaned_data['cocktail_tag']
        cocktail.category = self.cleaned_data['category']
        cocktail.glass = self.cleaned_data['glass']
        cocktail.instructions = self.cleaned_data['instructions']
        cocktail.image = self.cleaned_data['image']
        cocktail.image_source = self.cleaned_data['image_source']
        cocktail.image_attribution = self.cleaned_data['image_attribution']
        cocktail.date_modified = self.cleaned_data['date_modified']
        if commit:
            cocktail.save()
        return cocktail


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
