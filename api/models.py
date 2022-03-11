from django.db import models

# Create your models here.
class Promotion(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    prizes = models.ManyToManyField('Prize', related_name='promotions')
    participants = models.ManyToManyField('Participant', related_name='promotions')

class Prize(models.Model):
    description = models.TextField()

class Participant(models.Model):
    name = models.CharField(max_length=80)

class Result(models.Model):
    winner = models.ForeignKey('Participant', related_name='winners', on_delete=models.CASCADE)
    prize = models.ForeignKey('Prize', on_delete=models.CASCADE)
