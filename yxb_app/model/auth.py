from django.db import models
from django.contrib.auth.models import User
import hashlib


def password_hashlib(password):
    if isinstance(password, str):
        password = password.encode('utf-8')
    return hashlib.md5(password).hexdigest().upper()


class ClientUser(models.Model):
    # username,password
    username = models.CharField(max_length=20, null=True, unique=True)
    password = models.CharField(max_length=255, null=True)
    head_portrait = models.CharField(max_length=255, unique=False)
    gender = models.CharField(max_length=20, default='')
    birthday = models.DateTimeField(null=True, default=None, blank=True)
    status = models.BooleanField(default=True, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"username:{self.username}"

    @classmethod
    def add(cls, username, password, head_portrait='', gender='', birthday=None):
        return cls.objects.create(
            username=username,
            password=password_hashlib(password),
            head_portrait=head_portrait,
            gender=gender,
            birthday=birthday,
            status=True,
        )

    @classmethod
    def get_user(cls, username, password):
        try:
            user = cls.objects.get(
                username=username,
                password=password_hashlib(password)
            )
            return user
        except:
            return None

    def update_password(self, new_password, old_password):
        old_password = password_hashlib(old_password)
        if self.password != old_password:
            return False
        new_password = password_hashlib(new_password)
        self.password = new_password
        self.save()
        return True

    def update_status(self):
        self.status = not self.status
        self.save()
        return True
