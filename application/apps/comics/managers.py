from django.db import models
from django.db.models import Count


class LikesDislikesManager(models.Manager):

    def likes(self):
        return self.get_queryset().filter(vote=1)

    def dislikes(self):
        return self.get_queryset().filter(vote=0)
