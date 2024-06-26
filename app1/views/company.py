from app1.models import Company
from app1.forms import company as forms
from common.views import AdvancedListView, CreateView, UpdateView, DeleteView


class CompanyList(AdvancedListView):
    """
    公司列表的说明
    """
    model = Company
    related_sets = ('person_set',)


class CompanyCreate(CreateView):
    model = Company
    form_class = forms.CompanyCreateForm


class CompanyUpdate(UpdateView):
    model = Company
    form_class = forms.CompanyUpdateForm


class CompanyDelete(DeleteView):
    model = Company
