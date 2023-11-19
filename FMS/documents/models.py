from django.conf import settings
from django.db import models
from django.core.files import File
from io import BytesIO
from django.utils.timezone import now


class FileData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    file = models.FileField(default='', blank=True, upload_to=f'./')
    associate_folder = models.CharField(default='', blank=True, max_length=45)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # return str('%s%s%s' % (self.file, '-', self.associate_folder))
        return str(self.file)

    def __unicode__(self):
        return self.file
    
    @property
    def get_folder(self):
        """
        The function `get_folder` returns the `Folder` object associated with the `associate_folder`
        attribute, or `None` if it doesn't exist.
        :return: The code is returning an instance of the `Folder` model that matches the `associate_folder`
        attribute of the current object. If no matching folder is found, it returns `None`.
        """
        try:
            return Folder.objects.get(folder=self.associate_folder).id
        except Exception as e:
            return None

    # def save(self, *args, **kwargs):
    #     """
    #     The `save` function saves a file with a specific filename format and then calls the parent class's
    #     `save` method.
    #     """
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


class Share(models.Model):
    sharer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="sharer", on_delete=models.SET_NULL)
    sharee = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True,)
    file = models.ForeignKey(FileData, null=True, blank=True, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, null=True, blank=True, on_delete=models.CASCADE)
    access_link = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(default=now)
    
    def __str__(self) -> str:
        if self.folder:
            return str(self.folder)
        elif self.file:
            return str(self.file)
        else:
            return str(self.sharer)