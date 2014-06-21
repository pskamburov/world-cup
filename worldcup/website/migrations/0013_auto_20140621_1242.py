# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_auto_20140621_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='player',
            name='age',
            field=models.PositiveSmallIntegerField(),
        ),
    ]
