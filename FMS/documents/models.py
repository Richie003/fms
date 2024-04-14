from django.conf import settings
from django.db import models
from django.core.files import File
from django.db.models import Q
import os
from io import BytesIO
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import hashlib
from django.utils.timezone import now
from django.utils import timezone
from datetime import timedelta

# The `Notification` class represents a notification message with a recipient, message content, read
# status, and timestamp.
class Notification(models.Model):
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    message = models.TextField(default="", max_length=225)
    read_receipt = models.BooleanField(default=False)
    read = models.DateTimeField(default=now)
    
    class Meta:
        ordering = ['-read']
        
    def __str__(self):
        return str(self.message)

class FileTable(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    original_filename = models.CharField(max_length=255)
    file_Id = models.IntegerField(blank=True, null=True)
    file_size = models.IntegerField()
    file_path = models.CharField(max_length=255)
    associate_folder = models.CharField(default='', blank=True, max_length=45)
    identifier = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(default=now)
    
    def __str__(self):
        return str(self.original_filename)
    
    @property
    def approx_filesize(self):
        definite_size=None
        if self.file_size//(1024*1024) > 1:
            definite_size=f"{self.file_size//(1024*1024)}MB"
        else:
            definite_size=f"{self.file_size//1024}KB"
        return definite_size
    class Meta:
        ordering = ['-created']
    
    @classmethod
    def search_files(cls, associate_folder=None, user_id=None, filename=None):
        """
        The function `search_files` filters files based on the provided parameters and returns the result in
        descending order of creation.
        
        :param cls: The `cls` parameter refers to the class itself. In this case, it is likely a reference
        to the model class that this method belongs to
        :param associate_folder: The `associate_folder` parameter is used to filter the search results based
        on the associated folder. It is an optional parameter and if provided, the search will only return
        files that are associated with the specified folder
        :param user_id: The user_id parameter is used to filter the search results based on the user ID
        :param filename: The `filename` parameter is used to search for files based on their original
        filename. It is a string that represents the name of the file or a part of it. The search is
        case-insensitive and it uses the `icontains` lookup to find files that contain the specified
        filename as a substring
        :return: a queryset of objects that match the specified filters. The queryset is ordered by the
        'created' field in descending order.
        """
        query = Q()

        if associate_folder is not None:
            query &= Q(associate_folder=associate_folder)

        if user_id is not None:
            query &= Q(user_id=user_id)

        if filename is not None:
            query &= Q(original_filename__icontains=filename)

        # Apply the filter and return the result
        return cls.objects.filter(query).order_by('-created')
    
    @property
    def convertId(self):
        uuid = urlsafe_base64_encode(force_bytes(self.id))
        return uuid


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

def save_file(file_object, extras:dict):
    # Generate a unique identifier using SHA-256
    identifier = hashlib.sha256(file_object.read()).hexdigest()

    # Store the file information
    try:
        file = FileTable(
            user_id = int(extras["user"]),
            original_filename=file_object.name,
            file_Id=int(extras["ID"]),
            file_size=file_object.size,
            file_path=file_object.name,
            associate_folder = extras["folder"],
            identifier=identifier
        )
    except AttributeError:
        file = FileTable(
            user_id = int(extras["user"]),
            original_filename=file_object.name,
            file_Id=int(extras["ID"]),
            file_size=file_object.size,
            file_path=file_object.name,
            associate_folder = extras["folder"],
            identifier=identifier
        )
    file.save()

    # Store the actual file using the identifier
    with open(os.path.join(settings.MEDIA_ROOT, identifier), 'wb') as f:
        f.write(file_object.read())

def retrieve_file(filename):
    # Query the database to find the file's identifier
    file = FileTable.objects.get(original_filename=filename)
    identifier = file.identifier

    # Retrieve the file from the filesystem using the identifier
    with open(os.path.join(settings.MEDIA_ROOT, identifier), 'rb') as f:
        file_content = f.read()

    # Return the file content
    return file_content

class FileData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    file = models.FileField(default='', blank=True, upload_to=f'./')
    
    def delete(self, *args, **kwargs):
        self.file.delete()
        super(FileData, self).delete(*args, **kwargs)

    def __str__(self):
        # return str('%s%s%s' % (self.file, '-', self.associate_folder))
        return str(self.file)

    def __unicode__(self):
        return self.file
    
    @property
    def approx_filesize(self):
        definite_size=None
        filedata_size = FileTable.objects.get(user_id=self.user.id, original_filename=self.file).file_size
        if filedata_size//(1024*1024) < 1:
            definite_size=f"{filedata_size//(1024*1024)}MB"
        else:
            definite_size=f"{filedata_size//1024}KB"
        return definite_size
    
    @property
    def convertId(self):
        uuid = urlsafe_base64_encode(force_bytes(self.id))
        return uuid
<<<<<<< HEAD
=======

>>>>>>> origin/richie

class Folder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    folder = models.CharField(default='', blank=False, max_length=45)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.folder)


    @property
    def convertId(self):
        uuid = urlsafe_base64_encode(force_bytes(self.id))
        return uuid
    
    @property
    def get_associated_files(self):
        query_file = FileTable.objects.filter(user_id=self.user_id, associate_folder=self.folder)
        return query_file
    
    @property
    def get_sub_folders(self):
        query_sub_folders = SubFolder.objects.filter(user_id=self.user_id, parent_folder_id=self.id)
        return query_sub_folders

    
    @classmethod
    def search_folder(cls, user_id=None, folder=None):

        query = Q()

        if user_id is not None:
            query &= Q(user_id=user_id)

        if folder is not None:
            query &= Q(folder__icontains=folder)

        # Apply the filter and return the result
        return cls.objects.filter(query).order_by('-created')
    
    
    class Meta:
        ordering = ['-created']

class SubFolder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    parent_folder = models.ForeignKey(Folder, null=True, blank=True, on_delete=models.SET_NULL)
    folder = models.CharField(default='', blank=False, max_length=45)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str('%s%s%s' % (self.user, '-', self.folder))
    
    @property
    def convertId(self):
        uuid = urlsafe_base64_encode(force_bytes(self.id))
        return uuid
    
    @property
    def file_count(self):
        pass
    
def save_subfolder(data:dict):
    try:
        print(data["folder"])
        parent_folder = Folder.objects.get(user_id=int(data["user"]), folder=data["parent_folder"]).id
        sub_folder = SubFolder(
            user_id = int(data["user"]),
            folder = data["folder"],
            parent_folder_id=int(parent_folder),
        )
        sub_folder.save()
    except Exception as e:
        print(e)
        

    
    class Meta:
        ordering = ['-created']
        # constraints = [
        #         models.UniqueConstraint(fields=['parent_folder',], name='unique_folder_for_user')
        #     ]

# The Share class represents a sharing relationship between users, files, and folders in a system,
# with an access link and creation timestamp.
class Share(models.Model):
    sharer = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name="sharer", on_delete=models.SET_NULL)
    sharee = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,)
    file = models.ForeignKey(FileTable, null=True, blank=True, on_delete=models.CASCADE)
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

class Trash(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    file = models.ManyToManyField(FileTable)
    from_folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    from_sub_folder = models.ForeignKey(SubFolder, on_delete=models.CASCADE)
    deleted_on = models.DateTimeField(default=now)
    delete_on = models.DateField(default=timezone.now() + timedelta(days=30))
    
    def __str__(self) -> str:
        return super().__str__(self.user)

