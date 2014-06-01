# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('group', models.CharField(max_length=2)),
                ('info', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('host', models.ForeignKey(to_field='id', to='website.Team')),
                ('away', models.ForeignKey(to_field='id', to='website.Team')),
                ('score_host', models.PositiveSmallIntegerField()),
                ('score_away', models.PositiveSmallIntegerField()),
                ('schedule', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('team', models.ForeignKey(to_field='id', to='website.Team')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
