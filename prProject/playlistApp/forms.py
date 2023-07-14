from django import forms

class RequestSearchForm(forms.Form):
    search_word = forms.CharField(label='Search Word')
    
class RecommendSearchForm(forms.Form):
    search_word = forms.CharField(label='Search Word')