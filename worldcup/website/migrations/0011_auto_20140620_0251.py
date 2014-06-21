# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_auto_20140620_0229'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GoalScorer',
            new_name='Goal',
        ),
    ]
