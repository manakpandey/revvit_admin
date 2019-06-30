from django import forms


class AddFacultyForm(forms.Form):
    name = forms.CharField(label='name', max_length=50)
    school = forms.CharField(label='school', max_length=10)
    designation = forms.CharField(label='designation', max_length=50)