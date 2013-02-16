import re
from base64 import b64decode
import uuid

from django import forms
from django.forms import ValidationError
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile

from .models import Wallpaper
from .widgets import TagListInput, DragAndDropImageProcesserWidget, ClearableThumbnailImageWidget

# For base64 generated uploads (drag-and-drop API), this map converts the inline content type to a nice usable extension for automatic file name generation.
IMAGE_TYPE_EXTENSION_MAP = {
    'png': 'png',
    'jpeg': 'jpg',
}
BASE64_CONTENT_PATTERN = re.compile(r'^data:(?P<content_type>image/(?P<type>{}));base64,(?P<data>.*)$'.format(
        r'|'.join(IMAGE_TYPE_EXTENSION_MAP.keys())))


class CreateForm(forms.ModelForm):
    # Not required if image_raw is sent
    image = forms.ImageField(widget=DragAndDropImageProcesserWidget, required=False)

    # Receives drag-and-drop binary data, if any
    image_raw = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Wallpaper
        fields = ('tags', 'name', 'author', 'license', 'purity_rating', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'optional'}),
            'tags': TagListInput,
        }
    
    def clean_image_raw(self):
        """
        Some trickery to make the fake file field pass through the normal machinery without having
        been sent via ``request.FILES``.  The base64-encoded data, if present, is picked apart into
        its content type, decoded to the binary payload, its size measured, and a simulated
        ``UploadedFile`` is generated to satisfy a call to ``ImageField.to_python()``.

        All normal validation errors are raised, and we keep things as simple as is possible.

        """

        # TODO: Check performance of base64 encoded payload.  How does this compare to multipart/form-data?  Do we lose some kind of webserver chunk streaming?

        data = self.cleaned_data['image_raw']
        match = BASE64_CONTENT_PATTERN.match(data)
        if not match:
            raise ValidationError("Not a valid image file.")

        # Extract identifying information from the content string
        content_type = match.group('content_type')
        data = b64decode(match.group('data'))
        filename = uuid.uuid4()
        extension = IMAGE_TYPE_EXTENSION_MAP.get(match.group('type'))
        filename = '{}.{}'.format(filename, extension)

        # Generate some internal objects to keep things as close to legit as possible
        content_file = ContentFile(data, name=filename)
        uploaded_file = UploadedFile(content_file, filename, content_type, size=content_file.size)

        # Run the built-in image file validation so that we don't have to reinvent that wheel
        return forms.ImageField().to_python(uploaded_file)

    def clean(self):
        """ Validates that either ``image`` or ``image_raw`` exists. """
        cleaned_data = super(CreateForm, self).clean()
        image = cleaned_data.get('image')
        image_raw = cleaned_data.get('image_raw')

        if image_raw:
            cleaned_data['image'] = image_raw
        elif not image:
            raise ValidationError("File-picker image or drag-and-drop image is required.")

        return cleaned_data

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Wallpaper
        fields = ('tags', 'name', 'author', 'license', 'purity_rating', 'image', 'uploader',
                'duplicate_of', 'is_public', 'views', 'tags')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'optional'}),
            'duplicate_of': forms.TextInput(attrs={'placeholder': 'wallpaper id'}),
            'tags': TagListInput,
            'image': ClearableThumbnailImageWidget,
        }
