# Generated by Django 2.0.1 on 2018-11-07 12:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='Org',
            new_name='org',
        ),
        migrations.AddField(
            model_name='courseorg',
            name='category',
            field=models.CharField(choices=[('pxjg', '培训机构'), ('gx', '高校'), ('gr', '个人')], default='pxjg', max_length=20, verbose_name='机构类别'),
        ),
        migrations.AddField(
            model_name='courseorg',
            name='course_nums',
            field=models.IntegerField(default=0, verbose_name='课程数'),
        ),
        migrations.AddField(
            model_name='courseorg',
            name='students',
            field=models.IntegerField(default=0, verbose_name='学习人数'),
        ),
        migrations.AddField(
            model_name='courseorg',
            name='tag',
            field=models.CharField(default='国内名校', max_length=10, verbose_name='机构标签'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='age',
            field=models.IntegerField(default=18, verbose_name='年龄'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='', upload_to='teacher/%Y/%m', verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='citydict',
            name='desc',
            field=models.CharField(max_length=200, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='citydict',
            name='name',
            field=models.CharField(max_length=20, verbose_name='城市'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='address',
            field=models.CharField(max_length=150, verbose_name='机构地址'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='desc',
            field=models.TextField(verbose_name='机构描述'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='image',
            field=models.ImageField(upload_to='org/%Y/%m', verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='name',
            field=models.CharField(max_length=50, verbose_name='机构名称'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='name',
            field=models.CharField(max_length=50, verbose_name='教师名称'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='points',
            field=models.CharField(max_length=50, verbose_name='教学特点'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='work_company',
            field=models.CharField(max_length=50, verbose_name='就职公司'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='work_position',
            field=models.CharField(max_length=50, verbose_name='公司职位'),
        ),
    ]
