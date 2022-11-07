# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Category(models.Model):
    cate_id = models.AutoField(primary_key=True)
    cate_name = models.CharField(unique=True, max_length=30)

    class Meta:
        
        db_table = 'category'


class Debate(models.Model):
    db_id = models.AutoField(primary_key=True)
    db_topic = models.CharField(max_length=30, blank=True, null=True)
    db_positive_standpoint = models.CharField(max_length=50)
    db_negative_standpoint = models.CharField(max_length=50)
    db_positive_team = models.CharField(max_length=30, blank=True, null=True)
    db_negative_team = models.CharField(max_length=30, blank=True, null=True)
    db_winner = models.CharField(max_length=4, blank=True, null=True)
    db_date = models.DateField(blank=True, null=True)
    fig = models.ForeignKey('Figure', models.DO_NOTHING, blank=True, null=True)
    dbc = models.ForeignKey('DebateCompetition', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        
        db_table = 'debate'


class DebateCompetition(models.Model):
    dbc_id = models.AutoField(primary_key=True)
    dbc_name = models.CharField(unique=True, max_length=50)
    dbc_organizer = models.CharField(max_length=50, blank=True, null=True)
    dbc_detail = models.CharField(max_length=255, blank=True, null=True)
    dbc_first_date = models.DateField(blank=True, null=True)
    dbc_last_date = models.DateField(blank=True, null=True)

    class Meta:
        
        db_table = 'debate_competition'


class DebateFigure(models.Model):
    db_fig_id = models.AutoField(primary_key=True)
    db = models.ForeignKey(Debate, models.DO_NOTHING)
    fig = models.ForeignKey('Figure', models.DO_NOTHING)
    fig_position = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        
        db_table = 'debate_figure'


class Figure(models.Model):
    fig_id = models.AutoField(primary_key=True)
    fig_ch_name = models.CharField(max_length=50)
    fig_en_name = models.CharField(max_length=100, blank=True, null=True)
    fig_gender = models.CharField(max_length=10)
    fig_birthday = models.DateField(blank=True, null=True)
    fig_deathday = models.DateField(blank=True, null=True)
    fig_day_correction = models.IntegerField()
    fig_detail = models.CharField(max_length=255)
    fig_nationality = models.CharField(max_length=30, blank=True, null=True)
    fig_province = models.CharField(max_length=30, blank=True, null=True)
    fig_city = models.CharField(max_length=30, blank=True, null=True)
    fig_county = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        
        db_table = 'figure'


class FigureCategory(models.Model):
    fig_cate_id = models.AutoField(primary_key=True)
    fig = models.ForeignKey(Figure, models.DO_NOTHING)
    cate = models.ForeignKey(Category, models.DO_NOTHING)

    class Meta:
        
        db_table = 'figure_category'
        unique_together = (('cate', 'fig'),)


class Literature(models.Model):
    lit_id = models.AutoField(primary_key=True)
    lit_ch_title = models.CharField(max_length=50)
    lit_en_title = models.CharField(max_length=100, blank=True, null=True)
    lit_category = models.CharField(max_length=30)
    lit_published_date = models.DateField(blank=True, null=True)
    lit_detail = models.CharField(max_length=255)
    lit_read_times = models.IntegerField()
    lit_img_address = models.CharField(max_length=255, blank=True, null=True)
    fig = models.ForeignKey(Figure, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        
        db_table = 'literature'
