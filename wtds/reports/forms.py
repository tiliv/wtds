from operator import itemgetter

from django import forms

from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        widgets = {
            'object_fieldname': forms.Select,
        }

    def __init__(self, model, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)

        if hasattr(model, 'get_reportable_fields'):
            reportable_fields = model.get_reportable_fields()
            model_fields = map(itemgetter(0), map(model._meta.get_field_by_name, reportable_fields))
        else:
            model_fields = model._meta.local_fields
        self.fields['object_fieldname'].widget.choices = (
            (field.name, field.verbose_name) for field in model_fields
        )
