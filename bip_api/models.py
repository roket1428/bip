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
    terms = models.JSONField()
    grad_year = models.CharField(max_length=4)

    def __str__(self):
        return self.name

# data index model
class YearIndex(models.Model):
    year = models.CharField(max_length=4)
