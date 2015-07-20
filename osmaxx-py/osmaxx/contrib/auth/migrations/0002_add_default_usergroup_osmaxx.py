# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.conf import settings

OSMAXX_FRONTEND_USER = settings.OSMAXX_AUTHORIZATION['groups']['osmaxx_frontend_user']

def update_site_forward(apps, schema_editor):
    """Add group osmaxx."""
    Group = apps.get_model("auth", "Group")
    Group.objects.create(name=OSMAXX_FRONTEND_USER)


def update_site_backward(apps, schema_editor):
    """Revert add group osmaxx."""
    Group = apps.get_model("auth", "Group")
    Group.objects.get(name=OSMAXX_FRONTEND_USER).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_site_forward, update_site_backward),
    ]
