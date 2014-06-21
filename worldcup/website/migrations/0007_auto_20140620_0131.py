# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20140620_0126'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Points',
            new_name='Point',
        ),
    ]
