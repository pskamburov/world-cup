# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_auto_20140620_0251'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='age',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='position',
            field=models.CharField(max_length=3, default=''),
            preserve_default=True,
        ),
    ]
