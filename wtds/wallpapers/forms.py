# coding=utf-8

from django import forms

from .models import Wallpaper
from .widgets import TagListInput, DragAndDropImageProcesserWidget

class CreateForm(forms.ModelForm):
    class Meta:
        model = Wallpaper
        fields = ('tags', 'name', 'author', 'license', 'image')
        widgets = {
            'tags': TagListInput({'defaultText': '', 'removeText': '◉'}),
            'image': DragAndDropImageProcesserWidget,
        }

