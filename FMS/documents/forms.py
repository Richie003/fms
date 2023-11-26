from django import forms
from .models import FileData, Folder
from django.template.defaultfilters import filesizeformat
# from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class FileDataForm(forms.ModelForm):
    class Meta:
        model = FileData
        fields = (
            'file',
        )
    # def clean_content(self):
    #     content = self.cleaned_data.get('file')
    #     content_type = content.content_type.split('/')[0]
    #     print(content_type)
    #     if content_type in settings.CONTENT_TYPES:
    #         if content._size > settings.MAX_UPLOAD_SIZE:
    #             raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content._size)))
    #     else:
    #         raise forms.ValidationError(_('File type is not supported'))
    #     return content


class FolderDataForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = (
            'folder',
        )