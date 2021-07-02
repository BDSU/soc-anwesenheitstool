from django import forms
from .models import Meeting


class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = "__all__"

    name = forms.CharField(label='Name', max_length=100)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    begin = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    end = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    category = forms.ChoiceField(
        label='Kategorie', choices=Meeting.CATEGORIES)