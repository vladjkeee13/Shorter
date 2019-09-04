import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Url(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    url = models.CharField(max_length=512)
    text = models.TextField(blank=True)
    clicks = models.PositiveSmallIntegerField(default=0)
    short_url = models.CharField(max_length=255, blank=True)
    created_date = models.DateTimeField()
    expiration_date = models.DateTimeField()

    __original_text = None

    def __init__(self, *args, **kwargs):
        super(Url, self).__init__(*args, **kwargs)
        self.__original_text = self.text

    def save(self, force_insert=False, force_update=False, *args, **kwargs):

        if not self.id:
            self.created_date = timezone.now()
            self.expiration_date = timezone.now() + datetime.timedelta(days=14)

        if self.text != self.__original_text:
            list_of_str = self.text.split()
            for elem in list_of_str:
                if len(elem) >= 6:
                    index = list_of_str.index(elem)
                    list_of_str[index] = elem + '™️'
            self.text = ' '.join(list_of_str)
            self.__original_text = self.text

        return super(Url, self).save(force_insert, force_update, *args, **kwargs)


class MyUser(AbstractUser):

    avatar = models.ImageField(blank=True, null=True, upload_to='avatars')
    date_of_birth = models.DateField(blank=True, null=True)
    personal_information = models.TextField(blank=True, null=True)
