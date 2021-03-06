from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractUser


class Userprofile(AbstractUser):
    #自定义性别
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女'),
    )
    nick_name = models.CharField(max_length=20, verbose_name='昵称', default='')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    gender = models.CharField(
        max_length=6,
        verbose_name='性别',
        choices=GENDER_CHOICES,
        default= "female",
    )
    address = models.CharField(max_length=100, verbose_name='地址', default='')
    mobile = models.CharField(max_length=11, null=True, blank=True)
    image = models.ImageField(
        upload_to='image/%Y/%m',
        default='image/default.jpg',
        max_length=100,
    )

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    SEND_CHOICES = (
        ("register", "注册"),
        ("forget", "找回密码"),
    )
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name="邮箱")
    send_type = models.CharField(choices=SEND_CHOICES,max_length=10)
    # 这里的now得去掉(),不去掉会根据编译时间。而不是根据实例化时间。
    send_time = models.DateTimeField(default=datetime.now, verbose_name=u"发送时间")

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


# 轮播图model
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(
        upload_to="banner/%Y/%m",
        verbose_name=u"轮播图",
        max_length=100)
    url = models.URLField(max_length=200, verbose_name=u"访问地址")
    # 默认index很大靠后。想要靠前修改index值。
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name

    # 重载__str__方法使后台不再直接显示object
    def __str__(self):
        return '{0}(位于第{1}位)'.format(self.title, self.index)



# Create your models here.
