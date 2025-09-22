from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_user_last_login_remove_user_password_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
