from django.db import models
from django.urls import reverse
from hashids import Hashids
import datetime
# Create your models here.
class LinkQuerySet(models.QuerySet):
    def decode_link(self, code):
        decode = Hashids(min_length=4,alphabet="abcdefghijklmnopqrstuvwxyz").decode(code)[0]
        self.filter(pk=decode).update(counter=models.F("counter") + 1)
        return self.filter(pk=decode).first().url
    
    def totalLinks(self):
        return self.count()
        
    def totalRedirections(self):
        return self.aggregate(redirections=models.Sum("counter"))
    
    def dates(self,pk):
        return self.values('date').annotate(month= models.Sum("counter", filter=models.Q(date__gte=datetime.datetime(2024,1,1)),date__lte=datetime.date(2024,1,31)) ).filter(pk=pk)

    
    
    
class Link(models.Model):
    url  = models.URLField()
    code = models.CharField( max_length=50, blank=True)
    date = models.DateField(auto_now_add=True)
    counter = models.PositiveIntegerField(default=0)
    links = LinkQuerySet.as_manager()
    
    class Meta:
        verbose_name_plural = "Links"

    def __str__(self):
        return f"URL:{self.url} Code: {self.code}"
    
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:
            self.code = Hashids(min_length=4,alphabet="abcdefghijklmnopqrstuvwxyz").encode(self.pk)
            self.save()
        
    def get_absolute_url(self):
        return reverse("core:details", kwargs={"pk": self.pk})