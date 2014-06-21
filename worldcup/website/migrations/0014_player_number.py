# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_auto_20140621_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='number',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
