from django import forms


class MealForm(forms.Form):
    title = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        # cleaned_data['title'] = cleaned_data.get('title').lower()
        return cleaned_data
