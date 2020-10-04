from django.db import models
from django.urls import reverse
from hashids import Hashids
import datetime


# Create your models here.

class EnlaceQuerySet(models.QuerySet):

    def decode_enlace(self, code):
        decode = Hashids(min_length=4, alphabet='abcdefghijklmnopqrstuvwxyz').decode(code)[0]
        self.filter(pk=decode).update(counter=models.F('counter') + 1)
        return self.filter(pk=decode)[:1].get().url

    def total_links(self):
        return self.count()

    def total_redirects(self):
        return self.aggregate(redirects=models.Sum('counter'))

    def fecha(self, pk):
        print('SELF: => ', self)
        print('PK: ==> ', pk)
        return self.values('date').annotate(
            july=models.Sum('counter', filter=models.Q(date__gte=datetime.date(2020, 10, 1),
                                                       date__lte=datetime.date(2020, 10, 31))
                            ).filter(pk=pk)
        )


class Enlace(models.Model):
    url = models.URLField()
    code = models.CharField(max_length=8, blank=True)
    date = models.DateField(auto_now_add=True)
    counter = models.PositiveBigIntegerField(default=0)

    links = EnlaceQuerySet.as_manager()

    class Meta:

        verbose_name_plural = 'Enlaces'

    def __str__(self):
        return f"URL: {self.url} Code {self.code}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.code:
            self.code = Hashids(min_length=4, alphabet='abcdefghijklmnopqrstuvwxyz').encode(self.pk)
            self.save()

    def get_absolute_url(self):
        return reverse('short:detail', kwargs={'pk': self.pk})
