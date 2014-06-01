# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20140601_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voting',
            name='vote',
            field=models.PositiveSmallIntegerField(choices=[(1, 'bad'), (2, 'medium'), (3, 'good'), (4, 'very good'), (5, 'excellent')], default=0),
        ),
    ]
