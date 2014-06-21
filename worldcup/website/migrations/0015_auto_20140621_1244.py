# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_player_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='number',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
