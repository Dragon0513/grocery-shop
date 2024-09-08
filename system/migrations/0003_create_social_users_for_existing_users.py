from django.conf import settings
from django.db import migrations


def create_social_users(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    SocialUser = apps.get_model("system", "SocialUser")

    for user in User.objects.all():
        if not SocialUser.objects.filter(user=user).exists():
            SocialUser.objects.create(user=user)


class Migration(migrations.Migration):

    dependencies = [
        ("system", "0002_socialuser"),
    ]

    operations = [
        migrations.RunPython(create_social_users),
    ]
