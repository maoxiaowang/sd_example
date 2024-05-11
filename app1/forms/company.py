from django import forms

from app1.models import Company


class CompanyCreateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


class CompanyUpdateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name',)
