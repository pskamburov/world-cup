# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('vote', models.CharField(default='0', max_length=1, choices=[('1', 'bad'), ('2', 'medium'), ('3', 'good'), ('4', 'very good'), ('5', 'excellent')])),
                ('match', models.ForeignKey(to='website.Team', to_field='id')),
                ('player', models.ForeignKey(to='website.Player', to_field='id')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
