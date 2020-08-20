
# Plan to pass dicts to jsonb.JSONField() where keys is an odd
# option *ex:'over'/'under' and values is a numeric equivalent
# of odd coefficient *ex:-115/245.
# Field *ex: field_name = {'over': -115, 'under': 245}.
#
# Number of fields and odds changes in real time so there are many
# fields with blank=True option.
# -----------------------------------------------------------------


from django.db import models
from django.contrib.postgres.fields import jsonb


class Group(models.Model):
    """Groups of commands by parts of the world"""
    name = models.CharField('Group', max_length=30, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'


class League(models.Model):
    """Sport leagues"""
    name = models.CharField('League', max_length=50, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'League'
        verbose_name_plural = 'Leagues'


class Map(models.Model):
    """One map object with own odds"""
    group = models.ForeignKey(
        Group, on_delete=models.PROTECT,
        verbose_name='Group'
    )
    league = models.ForeignKey(
        League, on_delete=models.PROTECT,
        verbose_name='League'
    )
    number = models.PositiveIntegerField(verbose_name='Map number')
    team_1 = models.CharField(max_length=50, verbose_name='Team 1')
    team_2 = models.CharField(max_length=50, verbose_name='Team 2')
    knife_kill = jsonb.JSONField(
        verbose_name='Will there be a knife kill?', blank=True
    )
    over_27dot5 = jsonb.JSONField(
        verbose_name='(alingment: home) win and over 27.5 rounds', blank=True
    )
    over_25dot5 = jsonb.JSONField(
        verbose_name='(alingment: home) win and over 25.5 rounds', blank=True
    )
    overtime = jsonb.JSONField(
        verbose_name='Will there be overtime?', blank=True
    )
    total_r_odd_even = jsonb.JSONField(
        verbose_name='Total rounds Odd/Even', blank=True
    )
    ace = jsonb.JSONField(verbose_name='Will there be an ace?', blank=True)
    r1_to_r5 = jsonb.JSONField(verbose_name='1st to 5 rounds', blank=True)
    winner_r1 = jsonb.JSONField(verbose_name='1st Round Winner', blank=True)
    winning_margin = jsonb.JSONField(verbose_name='Winning Margin', blank=True)
    r16_winner = jsonb.JSONField(verbose_name='16th Round Winner', blank=True)
    date_time = models.DateTimeField(verbose_name='Matchup date and time')

    def __str__(self):
        return f'{self.team_1} - {self.team_2} | Map:{self.number}'

    class Meta:
        verbose_name = 'Map'
        verbose_name_plural = 'Maps'


class TeamLine(models.Model):
    """
    Сomplex abstraction which contains all maps played between two teams in one event
    store all information about event and team-line odds
    """
    group = models.ForeignKey(
        Group, on_delete=models.PROTECT, verbose_name='Group'
    )
    league = models.ForeignKey(
        League, on_delete=models.PROTECT, verbose_name='League'
    )
    map_1 = models.OneToOneField(
        Map, on_delete=models.PROTECT,
        blank=True, verbose_name='Map 1'
    )
    map_2 = models.OneToOneField(
        Map, on_delete=models.PROTECT,
        blank=True, verbose_name='Map 2'
    )
    map_3 = models.OneToOneField(
        Map, on_delete=models.PROTECT,
        blank=True, verbose_name='Map 3'
    )
    map_4 = models.OneToOneField(
        Map, on_delete=models.PROTECT,
        blank=True, verbose_name='Map 4'
    )
    map_5 = models.OneToOneField(
        Map, on_delete=models.PROTECT,
        blank=True, verbose_name='Map 5'
    )
    win_one_map_home = jsonb.JSONField(
        verbose_name='(alingment: home) win at least one map?', blank=True
    )
    win_one_map_away = jsonb.JSONField(
        verbose_name='(alingment: away) win at least one map?', blank=True
    )
    correct_score = jsonb.JSONField(verbose_name='Correct Score')

    def __str__(self):
        return f'Teamline {self.sport}:{self.league}'

    class Meta:
        verbose_name = 'Teamline'
        verbose_name_plural = 'Teamlines'
