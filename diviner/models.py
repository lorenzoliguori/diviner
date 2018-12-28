from django.db import models

# Create your models here.

class InvestChoice(models.Model):
    #question = models.ForeignKey(Question, on_delete=models.CASCADE)
    initial_investment = models.FloatField()
    annual_investment = models.FloatField()
    years = models.FloatField()
    annual_interest_rate = models.FloatField()

class RetireChoice(models.Model):
    #question = models.ForeignKey(Question, on_delete=models.CASCADE)
    initial_investment = models.FloatField()
    annual_investment = models.FloatField()
    income_for_life = models.FloatField()
    annual_interest_rate = models.FloatField()

class CommitChoice(models.Model):
    #question = models.ForeignKey(Question, on_delete=models.CASCADE)
    initial_investment = models.FloatField()
    income_for_life = models.FloatField()
    years = models.FloatField()
    annual_interest_rate = models.FloatField()

