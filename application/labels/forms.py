from django.forms import ModelForm
from django.forms.util import flatatt
from django.forms.widgets import TextInput
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from labels.models import MuseumObject

class ObjectNumberInput(TextInput):
    """
    Base class for all <input> widgets (except type='checkbox' and
    type='radio', which are special).
    """
    input_type = None # Subclasses must define this.

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))
            final_attrs['readonly'] = 'readonly'
        return mark_safe(u'<input%s />' % flatatt(final_attrs))

class EditMuseumObjectForm(ModelForm):
    class Meta:
        model = MuseumObject
        widgets = {
            'object_number': ObjectNumberInput,
        }
