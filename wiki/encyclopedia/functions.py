from django import forms
from . import util

class SearchForm(forms.Form):
    query = forms.CharField(
    label='',
    required=False,
    widget=forms.TextInput(
    attrs={'class': 'search',
    'placeholder': 'Search Encyclopedia'}))


class NewPageForm(forms.Form):
    title = forms.CharField(
        label="Title",
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder':'Enter Title'}))

    content = forms.CharField(
        label="Markdown content",
        required= False, 
        widget= forms.Textarea(
            attrs={'placeholder':'Enter markdown content','class':'col-sm-11'}))


def search_entries(request):
    form = SearchForm(request.GET)
    entries = util.list_entries()

    if form.is_valid():
        query = form.cleaned_data["query"]
        entries = [entry for entry in entries if query.lower() in entry.lower()]
    
    return form, entries        
