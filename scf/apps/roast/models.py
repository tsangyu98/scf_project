from django.db import models

# Create your models here.
from datetime import datetime


class Spit(models.Model):
    content = models.TextField(max_length=10000, verbose_name="吐槽内容")  # 吐槽内容
    publishtime = models.DateTimeField(default=datetime.utcnow)  # 发布日期
    userid = models.CharField(max_length=100, verbose_name="发布人id")  # 发布人ID
    nickname = models.CharField(max_length=100, verbose_name="发布人昵称")  # 发布人昵称
    visits = models.IntegerField(default=0, verbose_name="浏览量")  # 浏览量
    thumbup = models.IntegerField(default=0, verbose_name="点赞数")  # 点赞数
    comment = models.IntegerField(default=0, verbose_name="回复数")  # 回复数
    avatar = models.CharField(max_length=100, verbose_name="用户的头像")  # 用户的头像
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, related_name='subs', null=True, blank=True,
                               verbose_name='被吐槽的吐槽')  # 上级ID
    collected = models.BooleanField(default=False)  # 是否收藏
    hasthumbup = models.BooleanField(default=False)  # 是否点赞
