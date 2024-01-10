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
    gno = models.FloatField()
    credits_sum = models.FloatField()
    points_sum = models.FloatField()
    grad_year = models.IntegerField()
    grad_status = models.JSONField()

# student terms model
class Terms(models.Model):
    karne = models.OneToOneField(
        Karne,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    terms = models.JSONField()
 
# data index model
class YearIndex(models.Model):
    year = models.IntegerField()

class InternList(models.Model):
    student_id = models.IntegerField()
    name = models.CharField(max_length=100)
    major = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()
    intern_time = models.IntegerField()
    status = models.CharField(max_length=15)

class TermsList(models.Model):
    term = models.CharField(max_length=15)
    lecture_code = models.CharField(max_length=15)
    lecture_name = models.CharField(max_length=75)
    t = models.IntegerField()
    u = models.IntegerField()
    k = models.IntegerField()
    akts = models.IntegerField()
    
    
