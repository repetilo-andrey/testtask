from django.db import models
from django.utils import timezone

from mptt.models import TreeForeignKey


class Coworker(models.Model):
    pib = models.CharField(max_length=254)
    position = models.CharField(max_length=254)
    start_date = models.DateTimeField(default=timezone.now)
    email = models.EmailField(max_length=254)
    headman = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def serialize(self):
        data = {'id': self.id, 'pib': self.pib, 'position': self.position,
                'start_date':self.start_date, 'email': self.email}
        if self.headman_id:
            data['headman'] = {'id': self.headman_id, 'pib': self.headman.pib}
        return data
