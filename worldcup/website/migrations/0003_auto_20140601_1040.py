# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_voting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voting',
            name='match',
            field=models.ForeignKey(to='website.Match', to_field='id'),
        ),
    ]
