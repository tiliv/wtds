# coding=utf-8

from django import forms

from .models import Wallpaper
from .widgets import TagListInput, DragAndDropImageProcesserWidget

class CreateForm(forms.ModelForm):
    class Meta:
        model = Wallpaper
        fields = ('tags', 'name', 'author', 'license', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'optional'}),
            'tags': TagListInput(tagsInput_options={'defaultText': '', 'removeText': '◉'}),
            'image': DragAndDropImageProcesserWidget,
        }

