# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_auto_20140620_0131'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoalScorer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('match', models.ForeignKey(to='website.Match', to_field='id')),
                ('goalscorer', models.ForeignKey(to='website.Player', to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
