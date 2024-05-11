import json

from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.core.validators import ListFieldValidator, DictFieldValidator, MACAddressValidator
from common.forms.fields import (
    DictField as FormDictField, ListField as FormListField,
    GenericObjectField as FormGenericObjectField)
from common.log import default_logger as logger
from common.utils.json import is_json_str, CJsonEncoder

__all__ = [
    'JsonField',
    'DictField',
    'ListField',
    'GenericObjectField',
    'MACField',
    'MACSetField',
]


class JsonField(models.TextField):
    max_length = 2048

    def __init__(self, *args, **kwargs):
        max_length = kwargs.pop('max_length') if 'max_length' in kwargs else self.max_length
        super().__init__(*args, max_length=max_length, **kwargs)

    def get_prep_value(self, value):
        # before saving to db, value could be a string or Promise
        if value is None:
            return value
        # call super method to internationalize value
        value = super().get_prep_value(value)
        # here, value could be a python object
        if isinstance(value, Exception):
            raise value
        return json.dumps(value, cls=CJsonEncoder)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if isinstance(value, (dict, list)):
            return value
        else:
            if value is None:
                return
            try:
                return json.loads(value)
            except json.decoder.JSONDecodeError:
                return ValidationError(
                    self.error_messages['invalid'],
                    code='invalid',
                    params={'value': value}
                )

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        if value is None:
            return
        if is_json_str(value):
            return value
        return json.dumps(value, cls=CJsonEncoder)


class ListField(JsonField):
    description = _('List')
    default_error_messages = {
        'invalid': _('value must be a list-like jsonable string or null')
    }
    default_validators = [ListFieldValidator()]

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        if value is None:
            return
        if is_json_str(value):
            return value
        try:
            return json.dumps(value, cls=CJsonEncoder)
        except TypeError:
            return '[]'  # blank

    def to_python(self, value):
        if isinstance(value, str) and not value:
            return list()
        return super().to_python(value)

    def formfield(self, **kwargs):
        defaults = {'form_class': FormListField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class DictField(JsonField):
    description = _('Dict')
    default_error_messages = {
        'invalid': _('value must be a dict-like jsonable string or null')
    }
    default_validators = [DictFieldValidator()]
    empty_values = {}

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        if value is None:
            return
        if is_json_str(value):
            return value
        try:
            return json.dumps(value, cls=CJsonEncoder)
        except TypeError:
            return '{}'  # blank

    def to_python(self, value):
        if isinstance(value, str) and not value:
            return dict()
        return super().to_python(value)

    def formfield(self, **kwargs):
        defaults = {'form_class': FormDictField}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class GenericObjectField(models.CharField):
    """
    根据字符串自动判断类型
    支持int，float，str，list，bool
    """
    max_length = 2048
    description = _('Generic object field')
    default_error_messages = {
        'type_error': _('Valid choices are int, float, str, list, bool.')
    }
    form_klass = FormGenericObjectField

    def __init__(self, *args, **kwargs):
        max_length = kwargs.pop('max_length') if 'max_length' in kwargs else self.max_length
        super().__init__(*args, max_length=max_length, **kwargs)

    # def value_to_string(self, obj):
    #     value = self.value_from_object(obj)
    #     if value is None:
    #         return
    #     return str(value)
    # 
    # def get_prep_value(self, value):
    #     return self.to_python(value)

    def from_db_value(self, value, expression, connection):
        return self.form_klass.typed_val(value)

    def to_python(self, value):
        value = super().to_python(value)
        return self.form_klass.raw_val(value)

    def formfield(self, **kwargs):
        defaults = {'form_class': self.form_klass}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class MACField(models.CharField):
    """
    XX:XX:XX:XX:XX:XX
    """
    max_length = 17
    description = _('MAC field')
    default_error_messages = {
        'invalid': _('Value must a valid IPv4/IPv6 address (segment).')
    }
    default_validators = [MACAddressValidator]

    def __init__(self, *args, **kwargs):
        max_length = kwargs.pop('max_length') if 'max_length' in kwargs else self.max_length
        super().__init__(*args, max_length=max_length, **kwargs)

    def get_prep_value(self, value):
        # before saving to db, value could be a string or Promise
        if value is None:
            return value
        # call super method to internationalize value
        value = super().get_prep_value(value)
        # here, value could be a python object
        value = self.value_to_string(value)
        value = value.replace('-', ':')
        return value

    def value_to_string(self, obj):
        if not isinstance(obj, str):
            return self.value_from_object(obj)
        return obj


class MACSetField(ListField):
    """
    这里只能保证新传入的MAC不重复，整个字段不重复需要在逻辑里处理下，如：
    s = list(set(s))
    s.sorted()
    """

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        if value is None:
            return
        if is_json_str(value):
            return value
        try:
            value = list(set(value))
            value.sort()
            return json.dumps(value)
        except TypeError:
            return '[]'  # blank
