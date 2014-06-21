# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_auto_20140620_0225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='score_host',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='score_away',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
