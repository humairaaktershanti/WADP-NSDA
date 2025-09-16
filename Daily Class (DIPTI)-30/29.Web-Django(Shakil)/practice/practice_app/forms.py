from django.forms import ModelForm
from .models import *

class authorForm(ModelForm):
    class Meta:
        model = Author
        fields = "__all__"

class bookForm(ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        

    