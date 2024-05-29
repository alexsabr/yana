from django.db import models
from datetime import date


class journal_db(models.Model):
    ORIENTATION=["Far-Left","Left","Center","Right","Far-Right"]
    name=models.CharField(null=False)
    political = models.CharField(null=False,choices=ORIENTATION)


# Create your models here.
class article_db(models.Model):
    title= models.CharField("")
    journal= models.ForeignKey(journal_db, on_delete=models.CASCADE)
    condensed_text= models.CharField("")
    publication_date= models.DateField(default=date(1970,1,1))

