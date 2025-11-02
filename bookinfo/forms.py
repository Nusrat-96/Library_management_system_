from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review',]
        labels = {
            'review': ''  # remove label text in the visualize page, 
        }
        widgets = {
            'review': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review...'}),
        }
        
    