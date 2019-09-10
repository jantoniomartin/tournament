# -*- coding: utf-8 -*-


from django.db import models, migrations
import tournament.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('condottieri_scenarios', '0001_initial'),
        ('machiavelli', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('finances', models.BooleanField(default=False, verbose_name='finances')),
                ('assassinations', models.BooleanField(default=False, help_text='will enable Finances', verbose_name='assassinations')),
                ('excommunication', models.BooleanField(default=False, verbose_name='excommunication')),
                ('special_units', models.BooleanField(default=False, help_text='will enable Finances', verbose_name='special units')),
                ('lenders', models.BooleanField(default=False, help_text='will enable Finances', verbose_name='money lenders')),
                ('unbalanced_loans', models.BooleanField(default=False, help_text='the credit for all players will be 25d', verbose_name='unbalanced loans')),
                ('conquering', models.BooleanField(default=False, verbose_name='conquering')),
                ('famine', models.BooleanField(default=False, verbose_name='famine')),
                ('plague', models.BooleanField(default=False, verbose_name='plague')),
                ('storms', models.BooleanField(default=False, verbose_name='storms')),
                ('strategic', models.BooleanField(default=False, verbose_name='strategic movement')),
                ('variable_home', models.BooleanField(default=False, help_text='conquering will be disabled', verbose_name='variable home country')),
                ('taxation', models.BooleanField(default=False, help_text='will enable Finances and Famine', verbose_name='taxation')),
                ('fow', models.BooleanField(default=False, help_text='each player sees only what happens near his borders', verbose_name='fog of war')),
                ('press', models.PositiveIntegerField(default=0, verbose_name='press', choices=[(0, 'Normal (private letters, anonymous gossip)'), (1, 'Gunboat diplomacy (no letters, no gossip)')])),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('joined_on', models.DateTimeField(auto_now_add=True, verbose_name='joined_on')),
                ('accepted', models.BooleanField(default=False, verbose_name='accepted')),
                ('eliminated', models.BooleanField(default=False, verbose_name='eliminated')),
            ],
            options={
                'verbose_name': 'participant',
                'verbose_name_plural': 'participants',
            },
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.PositiveIntegerField(null=True, verbose_name='score', blank=True)),
            ],
            options={
                'verbose_name': 'slot',
                'verbose_name_plural': 'slots',
            },
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('motto', models.CharField(max_length=200, verbose_name='motto')),
                ('banner', models.ImageField(upload_to=tournament.models.get_banner_upload_path, verbose_name='banner')),
                ('url', models.URLField()),
            ],
            options={
                'verbose_name': 'sponsor',
                'verbose_name_plural': 'sponsors',
            },
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveIntegerField(default=0, verbose_name='number')),
                ('size', models.PositiveIntegerField(default=0, verbose_name='size')),
                ('number_of_games', models.PositiveIntegerField(default=0, verbose_name='number of games')),
                ('started_on', models.DateTimeField(null=True, verbose_name='started on', blank=True)),
                ('finished_on', models.DateTimeField(null=True, verbose_name='finished on', blank=True)),
                ('time_limit', models.PositiveIntegerField(default=86400, help_text='seconds available to play a turn', verbose_name='time limit')),
                ('cities_to_win', models.PositiveIntegerField(default=15, help_text='cities that must be controlled to win a game', verbose_name='cities to win')),
                ('years_limit', models.PositiveIntegerField(default=0, help_text='the game finish after these years', verbose_name='years limit')),
                ('scenario', models.ForeignKey(to='condottieri_scenarios.Scenario', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'stage',
                'verbose_name_plural': 'stages',
            },
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=20, verbose_name='slug')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('deadline', models.DateTimeField(verbose_name='registration deadline')),
                ('admission_open', models.BooleanField(default=False, verbose_name='admission is open')),
                ('auto_accept', models.BooleanField(default=False, verbose_name='automatically accept participants')),
                ('minimum_users', models.PositiveIntegerField(default=0, verbose_name='minimum users')),
                ('title_en', models.CharField(max_length=100, null=True, verbose_name='title', blank=True)),
                ('title_es', models.CharField(max_length=100, null=True, verbose_name='title', blank=True)),
                ('title_ca', models.CharField(max_length=100, null=True, verbose_name='title', blank=True)),
                ('title_de', models.CharField(max_length=100, null=True, verbose_name='title', blank=True)),
                ('description_en', models.TextField(null=True, verbose_name='description', blank=True)),
                ('description_es', models.TextField(null=True, verbose_name='description', blank=True)),
                ('description_ca', models.TextField(null=True, verbose_name='description', blank=True)),
                ('description_de', models.TextField(null=True, verbose_name='description', blank=True)),
                ('prize_en', models.TextField(null=True, verbose_name='prize', blank=True)),
                ('prize_es', models.TextField(null=True, verbose_name='prize', blank=True)),
                ('prize_ca', models.TextField(null=True, verbose_name='prize', blank=True)),
                ('prize_de', models.TextField(null=True, verbose_name='prize', blank=True)),
                ('rules_en', models.URLField(null=True, verbose_name='rules', blank=True)),
                ('rules_es', models.URLField(null=True, verbose_name='rules', blank=True)),
                ('rules_ca', models.URLField(null=True, verbose_name='rules', blank=True)),
                ('rules_de', models.URLField(null=True, verbose_name='rules', blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                ('sponsors', models.ManyToManyField(to='tournament.Sponsor', blank=True)),
            ],
            options={
                'ordering': ['created_on'],
                'verbose_name': 'tournament',
                'verbose_name_plural': 'tournaments',
            },
        ),
        migrations.CreateModel(
            name='TournamentGame',
            fields=[
                ('game_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='machiavelli.Game', on_delete=models.CASCADE)),
                ('stage', models.ForeignKey(to='tournament.Stage', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'tournament game',
                'verbose_name_plural': 'tournament games',
            },
            bases=('machiavelli.game',),
        ),
        migrations.AddField(
            model_name='stage',
            name='tournament',
            field=models.ForeignKey(to='tournament.Tournament', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='stage',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='tournament.Slot'),
        ),
        migrations.AddField(
            model_name='slot',
            name='stage',
            field=models.ForeignKey(to='tournament.Stage', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='slot',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='participant',
            name='tournament',
            field=models.ForeignKey(to='tournament.Tournament', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='participant',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='configuration',
            name='stage',
            field=models.OneToOneField(editable=False, to='tournament.Stage', verbose_name='stage', on_delete=models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='stage',
            unique_together=set([('tournament', 'number')]),
        ),
        migrations.AlterUniqueTogether(
            name='slot',
            unique_together=set([('user', 'stage')]),
        ),
        migrations.AlterUniqueTogether(
            name='participant',
            unique_together=set([('user', 'tournament')]),
        ),
    ]
