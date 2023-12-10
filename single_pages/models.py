from django.contrib.auth.models import User
from django.db import models

# Create your models here.


# 유저에 전공부분 추가를 위해 설정
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    major = models.TextField(max_length=15)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_who = models.BooleanField(default=False)
