import secrets

from PIL import Image
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.timezone import now
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.files import File


class UserManager(BaseUserManager):
    def create_user(self, email, username, tel, full_name, ip, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            tel=tel,
            full_name=full_name,
            ip=ip,
            password=password
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, tel, full_name, ip, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            tel=tel,
            full_name=full_name,
            ip=ip,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, tel, full_name, ip, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            tel=tel,
            full_name=full_name,
            ip=ip,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    objects = UserManager()
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # COLLEGES = (
    #     ('SCIENCES', 'SCIENCES'),
    #     ('HEALTH SCIENCES', 'HEALTH SCIENCES'),
    #     ('SOCIAL SCIENCES', 'SOCIAL SCIENCES'),
    #     ('MANAGEMENT SCIENCES', 'MANAGEMENT SCIENCES'),
    #     ('ART', 'ART')
    # )
    # college = models.CharField(max_length=30, default='', choices=COLLEGES)
    username = models.CharField(default='', verbose_name='username', unique=True, null=False, blank=False,
                                max_length=30)
    tel = models.CharField(default='', null=True, blank=True, max_length=11)
    full_name = models.CharField(default='', blank=False, null=False, max_length=100)
    ip = models.CharField(default='', max_length=200, blank=True)
    active = models.BooleanField(default=True)
    auser = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name', 'tel', 'ip']  # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):  # __unicode__ on Python 2
        # concatenate = '%s %s' % (self.first_name, self.last_name)
        return self.username

    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_user(self):
        """Is it a user?"""
        return self.auser

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.staff

    @property
    def is_admin(self):
        """Is the user a admin member?"""
        return self.admin

    @property
    def is_active(self):
        """Is the user active?"""
        return self.active


class UserBio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    code = models.CharField(default='', blank=True, max_length=9)
    qrcode = models.ImageField(upload_to='user_QRC_auth/', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        concatenate = '%s%s%s' % (self.user, '-', self.code)
        return str(concatenate)

    def save(self, *args, **kwargs):
        qrcode_image = qrcode.make(f"Name: {self.user}\nAuthor: {self.code}")
        canvas = Image.new('RGB', (430, 430), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_image)
        fname = f"{'%s%s%s' % (self.user, '-', self.code)}.png"
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qrcode.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
