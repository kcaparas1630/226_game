from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=1,unique =True)
    row = models.IntegerField()
    col = models.IntegerField()
    score = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name} @({self.row},{self.col},{self.score})'


class Board(models.Model):
    label = models.CharField(max_length=1, default='*')
    row = models.IntegerField()
    column = models.IntegerField()
    value = models.IntegerField(default=0)  # Provide a default value here

    def __str__(self):
        return f'{self.label}'
