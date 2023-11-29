from django.db import models
from django.core.exceptions import ValidationError


def validate_col_amount(value):
    if value != 10:
        raise ValidationError('Column is not equal to 10', code='col_amount')
def validate_row_amount(value):
    if value != 10:
        raise ValidationError('Row is not equal to 10', code='row_amount')
def validate_col_range(value):
    if value < 1  or value > 10:
        raise ValidationError('Column out of range', code='col_value')
def validate_row_range(value):
    if value < 1 or value > 10:
        raise ValidationError('Row out of range', code='row_range')
def validate_unique_tag(value):
    players = Player.objects.filter(tag=value)
    if len(players) != 0:
        raise ValidationError('Tag already taken', code='duplicate')

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=1,unique =True, validators=[validate_unique_tag])
    row = models.IntegerField(validators=[validate_row_range])
    col = models.IntegerField(validators=[validate_col_range])
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} @({self.row},{self.col},{self.score})'


class Board(models.Model):
    label = models.CharField(max_length=1, default='*')
    row = models.IntegerField(validators=[validate_row_amount])
    column = models.IntegerField(validators=[validate_col_amount])
    value = models.IntegerField(default=0)  # Provide a default value here

    def __str__(self):
        return f'{self.label}'


