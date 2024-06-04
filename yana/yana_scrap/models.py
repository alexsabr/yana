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
    def model_to_dict(self)->dict:
        return {
            "name": self.name,
            "political":self.political,
        }


# Create your models here.
class article_db(models.Model):
    title= models.CharField("")
    journal= models.ForeignKey(journal_db, on_delete=models.CASCADE)
    condensed_text= models.CharField("")
    publication_date= models.DateField(default=date(1970,1,1))
    linked_article= models.ManyToManyField("article_db")
    
    def model_to_dict(self,recursive=False)->dict:
        thelinked_articles :list["article_db"] = self.linked_article.all()
        article_array=[ artic.model_to_dict(False) for artic in thelinked_articles] if recursive else []
        return {
            "title":self.title,
            "journal":self.journal.model_to_dict(),
            "condensed_text":self.condensed_text,
            "publication_date":self.publication_date,
            "linked_article":  article_array,
        }