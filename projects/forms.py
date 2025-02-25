from django.forms import ModelForm
from django import forms
from .models import Movies, Review

class MoviesForm(ModelForm):
    class Meta:
        model = Movies
        fields = ['title', 'featured_image', 'description', 'trailer_link', 'source_link', 'tags']
        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(MoviesForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
        
        #self.fields['title'].widget.attrs.update({'class':'input', 'placeholder': 'Add Title'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        label = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})