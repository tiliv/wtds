import json
from operator import attrgetter

from django import forms
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

from sorl.thumbnail.shortcuts import get_thumbnail

class DragAndDropImageProcesserWidget(forms.FileInput):
    class Media:
        css = {'all': ('css/image-processor.css',)}
        js = ('js/image-processor.js', 'js/calculate-gcd-javascript.js')

    def render(self, name, value, attrs=None):
        s = super(DragAndDropImageProcesserWidget, self).render(name, value, attrs)
        s = mark_safe(s + u""
            u'<div id="hover-indicator"></div>'
            u'<div id="preview-stage">'
                u'<div id="size-readout"></div>'
            u'</div>')
        return s


class TagListInput(forms.TextInput):
    class Media:
        css = {'all': ('lib/tagsinput/jquery.tagsinput.css',)}
        js = ('lib/tagsinput/jquery.tagsinput.js',)

    def __init__(self, attrs=None, tagsInput_options={}):
        self.tagsInput_options = tagsInput_options
        super(TagListInput, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        elif not isinstance(value, basestring):
            value = ','.join([taggeditem.tag.name for taggeditem in value])
        s = super(TagListInput, self).render(name, value, attrs)
        js = '<script type="text/javascript">$("#{id}").tagsInput({tagsInput_options});</script>'
        attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        options = json.dumps(self.tagsInput_options)
        return mark_safe(s + js.format(tagsInput_options=options, **attrs))


class ClearableThumbnailImageWidget(forms.ClearableFileInput):
    """
    Subtle modification to the style of implementation found in ``sorl.thumbnail.admin.current``.
    The original doesn't work very well with ``form.as_p`` and such, due to the way it is designed
    to work only with the ``contrib.admin`` interface.
    
    """

    template_with_initial = u'%(clear_template)s %(input_text)s: %(input)s'

    def render(self, name, value, attrs=None):
        output = super(ClearableThumbnailImageWidget, self).render(name, value, attrs)
        if value and hasattr(value, 'url'):
            try:
                thumbnail = get_thumbnail(value, '280x188', crop="center")
            except Exception:
                pass
            else:
                output = (u'<a class="thumbnail tile" target="_blank" href="%s">'
                    u'<img src="%s" width="140" height="94" /></a>') % (value.url, thumbnail.url) \
                    + output
        return mark_safe(output)
