import pandas as pd
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import InternList, TermsList
from pathlib import Path

@receiver(post_migrate)
def on_post_migrate(sender, **kwargs):
    if not TermsList.objects.all().exists():
        path = Path(__file__).parent / "initial_data/lecture_list.csv"
        print(path)
        termsList = pd.read_csv(path)
        for _, v in termsList.iterrows():
            TermsList.objects.create(
                term=v['term'],
                lecture_code=v['lecture_code'],
                lecture_name=v['lecture_name'],
                t=v['t'],
                u=v['u'],
                k=v['k'],
                akts=v['akts']
            )

    if not InternList.objects.all().exists():
        path = Path(__file__).parent / "initial_data/intern_list.csv"
        print(path)
        internList = pd.read_csv(path)
        for _, v in internList.iterrows():
            InternList.objects.create(
                student_id=v['student_id'],
                name=v['name'],
                major=v['major'],
                start_date=v['start_date'],
                end_date=v['end_date'],
                intern_time=v['intern_time'],
                status=v['status']
            )