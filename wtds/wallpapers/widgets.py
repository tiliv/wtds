import json
from operator import attrgetter

from django import forms
from django.utils.safestring import mark_safe

class DragAndDropImageProcesserWidget(forms.FileInput):
    class Media:
        css = {'all': ('css/image-processor.css',)}
        js = ('js/image-processor.js', 'js/calculate-gcd-javascript.js')

    def render(self, name, value, attrs=None):
        s = super(DragAndDropImageProcesserWidget, self).render(name, value, attrs)

        s = mark_safe(s + """
            <div id="hover-indicator"></div>
            <div id="preview-stage">
                <div id="size-readout"></div>
            </div>
        """)

        return s


class TagListInput(forms.TextInput):
    class Media:
        css = {'all': ('lib/tagsinput/jquery.tagsinput.css',)}
        js = ('lib/tagsinput/jquery.tagsinput.js',)

    def __init__(self, attrs=None, tagsInput_options={}):
        self.tagsInput_options = tagsInput_options
        super(TagListInput, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        if not isinstance(value, basestring):
            value = ','.join([taggeditem.tag.name for taggeditem in value])
        s = super(TagListInput, self).render(name, value, attrs)
        js = '<script type="text/javascript">$("#{id}").tagsInput({tagsInput_options});</script>'
        attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        options = json.dumps(self.tagsInput_options)
        return mark_safe(s + js.format(tagsInput_options=options, **attrs))

