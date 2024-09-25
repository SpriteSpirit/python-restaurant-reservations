# Generated by Django 5.1.1 on 2024-09-25 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_options_remove_user_username_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True,
                default="users/avatars/default.jpg",
                null=True,
                upload_to="users/avatars",
                verbose_name="Фото",
            ),
        ),
    ]