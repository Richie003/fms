from django.conf import settings
from django.db import models
from django.core.files import File
from io import BytesIO


class FileData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    file = models.FileField(default='', blank=True,
                            upload_to=f'./')
    associate_folder = models.CharField(default='', blank=True, max_length=45)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return str('%s%s%s' % (self.file, '-', self.associate_folder))
        return str(self.file)

    def __unicode__(self):
        return self.file

    # def save(self, *args, **kwargs):
    #     fname = f"{'%s%s%s' % (self.author, '-', self.file)}"
    #     buffer = BytesIO()
    #     self.file.save(fname, File(buffer), save=False)
    #     super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created']


class Folder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    folder = models.CharField(default='', blank=False, max_length=45)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str('%s%s%s' % (self.user, '-', self.folder))
    
    class Meta:
        ordering = ['-created']