from app1.models import Person
from app1.forms import person as forms
from common.views import AdvancedListView, CreateView


class PersonList(AdvancedListView):
    model = Person
    related_sets = ('company',)


class PersonCreate(CreateView):
    model = Person
    form_class = forms.PersonCreateForm
