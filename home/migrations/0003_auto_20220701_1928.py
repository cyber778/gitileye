# Generated by Django 4.0.5 on 2022-07-01 19:28

from django.db import migrations

def create_admin(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    if not User.objects.filter(username='admin').exists():
        user = User.objects.create_user('admin', password='admin123')
        user.is_superuser=True
        user.is_staff=True
        user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_repoitem_created_repoitem_modified_and_more'),
    ]

    operations = [
        migrations.RunPython(create_admin),
    ]
