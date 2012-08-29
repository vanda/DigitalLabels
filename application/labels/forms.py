from django.forms import ModelForm
from django.forms.util import flatatt
from django.forms.widgets import TextInput
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from labels.models import MuseumObject

class ObjectNumberInput(TextInput):
    """
    Class for managing the object_number input editability 
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
            final_attrs['style'] = 'width: 272px;'
        return mark_safe(u'<input%s />' % flatatt(final_attrs))

class EditMuseumObjectForm(ModelForm):
    class Meta:
        model = MuseumObject
        widgets = {
            'object_number' : ObjectNumberInput,
        }
