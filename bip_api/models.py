from django.db import models

# karne model
class Karne(models.Model):
    university = models.CharField(max_length=75)
    major = models.CharField(max_length=75)
    student_id = models.IntegerField()
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    signup_date = models.DateField()
    print_date = models.DateField()
    gno = models.CharField(max_length=10)
    credits_sum = models.CharField(max_length=10)
    points_sum = models.CharField(max_length=10)
    grad_year = models.IntegerField()

    def __str__(self):
        return self.name

# student terms model
class Terms(models.Model):
    terms = models.JSONField()
 
# data index model
class YearIndex(models.Model):
    year = models.IntegerField()
