from django.forms import ModelForm, Textarea, TextInput, HiddenInput

from .models import Post, Item, Prediction

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['text']
        widgets = {
        'text': TextInput(attrs={'class' : 'input', 'placeholder' : 'Say something...'}),
        }

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'desc', 'expenditure', 'recurring']
        widgets = {
        'desc': Textarea(attrs={'cols': 50, 'rows': 5}),
        }

class PredictionForm(ModelForm):
    class Meta:
        model = Prediction
        fields = ['item', 'amount']
        widgets = {
        'item': HiddenInput(),
        }