# Generated by Django 3.2.12 on 2022-04-12 08:27

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import edtech_app.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('meta_tags', models.CharField(blank=True, max_length=2000)),
                ('meta_desc', models.TextField(blank=True, max_length=2000)),
                ('image', models.ImageField(upload_to='media/imageblog')),
                ('image_alt_name', models.CharField(blank=True, max_length=200)),
                ('desc', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('author', models.CharField(default='admin', max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('hit', models.PositiveIntegerField(default=0)),
                ('disc', models.BooleanField(default=False, verbose_name='discription')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('logo', models.ImageField(blank=True, help_text='Optional', null=True, upload_to='media/catlogo')),
                ('top_ten_cat', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('disc', models.BooleanField(default=False, verbose_name='Add In Disclaimer')),
            ],
        ),
        migrations.CreateModel(
            name='cours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('reqs', models.CharField(blank=True, max_length=2000)),
                ('image', models.ImageField(upload_to='media/image_cours')),
                ('image_alt_name', models.CharField(blank=True, max_length=200)),
                ('desciption', models.TextField(blank=True, null=True)),
                ('teacher', models.CharField(default='admin', max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('like', models.PositiveIntegerField(default=0)),
                ('price', models.PositiveIntegerField(default=0)),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edtech_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('langue', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='VideoCours',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('video', models.FileField(upload_to=edtech_app.models.cour_directory_path)),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('titre', models.CharField(blank=True, max_length=200)),
                ('chapitre', models.CharField(blank=True, max_length=200)),
                ('cour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edtech_app.cours')),
            ],
        ),
        migrations.CreateModel(
            name='Sujet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70)),
                ('reqs', models.CharField(blank=True, max_length=2000, verbose_name='description')),
                ('author', models.CharField(blank=True, max_length=100)),
                ('images', models.ImageField(blank=True, upload_to='media/image_sujet')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('follows', models.ManyToManyField(blank=True, related_name='sujet_follows', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='subcat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('disc', models.BooleanField(default=False, verbose_name='Add In Disclaimer')),
                ('parent', models.ForeignKey(blank=True, help_text='Select Only Sub Category', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcat', to='edtech_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=180)),
                ('resume', models.FileField(blank=True, null=True, upload_to='media/resume/')),
                ('follows', models.ManyToManyField(blank=True, related_name='followed_by', to='edtech_app.Student')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('question', models.TextField(blank=True, max_length=200)),
                ('author', models.CharField(default='guest', max_length=20)),
                ('sujet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edtech_app.sujet')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ordred', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edtech_app.cours')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cours',
            name='langue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edtech_app.language'),
        ),
        migrations.AddField(
            model_name='cours',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='cour_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='BlogComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edtech_app.blog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog', to='edtech_app.sujet'),
        ),
        migrations.AddField(
            model_name='blog',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='blog_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='annonce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('tags', models.CharField(blank=True, max_length=2000)),
                ('desc', models.TextField(blank=True, max_length=200)),
                ('author', models.CharField(default='student', max_length=20)),
                ('sujet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edtech_app.sujet')),
            ],
        ),
    ]