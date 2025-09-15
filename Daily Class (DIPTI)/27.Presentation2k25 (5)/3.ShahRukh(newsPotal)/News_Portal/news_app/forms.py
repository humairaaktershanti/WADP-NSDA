from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget


class NewsForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = NewsModel
        fields = [
            'title',
            'excerpt',
            'content',
            'category',
            'author',
            'featured_image',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter news title'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Short summary of the news',
                'rows': 3
            }),
            
            'category': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'featured_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }




class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        fields = ['catagory_name']  
        widgets = {
            'catagory_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
        }