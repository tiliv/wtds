import logging
from operator import itemgetter

from django import forms

from .models import Report

logger = logging.getLogger(__name__)

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'
        widgets = {
            'object_fieldname': forms.Select,
        }

    def __init__(self, model, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)

        # Configure the field choices
        if hasattr(model, 'get_reportable_fields'):
            reportable_fields = model.get_reportable_fields()
            model_fields = map(itemgetter(0), map(model._meta.get_field_by_name, reportable_fields))
        else:
            model_fields = model._meta.local_fields
        self.fields['object_fieldname'].widget.choices = (
            (field.name, field.verbose_name) for field in model_fields
        )

        # Hide inputs that are pre-filled by the circumstances
        for field_name, value in self.initial.items():
            self.fields[field_name].widget = forms.HiddenInput()

        if 'object_fieldname' in self.initial:
            field = getattr(model, self.initial['object_fieldname'])
            try:
                field = field.field
            except:
                pass
            self.fields['description'] = field.formfield()
