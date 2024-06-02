from django.db import models
from datetime import date


class journal_db(models.Model):
    FL="FLEFT"
    L="LEFT"
    C="CENTER"
    R="RIGHT"
    FR="FRIGHT"
    ORIENTATIONS=[
        (FL,"Far-Left")
        ,(L,"Left")
        ,(C,"Center")
        ,(R,"Right")
        ,(FR,"Far-Right")
    ]
    name=models.CharField(null=False)
    political = models.CharField(null=False,choices=ORIENTATIONS)


# Create your models here.
class article_db(models.Model):
    title= models.CharField("")
    journal= models.ForeignKey(journal_db, on_delete=models.CASCADE)
    condensed_text= models.CharField("")
    publication_date= models.DateField(default=date(1970,1,1))
    linked_article= models.ManyToManyField("article_db")

