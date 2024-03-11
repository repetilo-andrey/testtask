from django.db import models

from mptt.models import MPTTModel, TreeForeignKey


class Coworker(MPTTModel):
    pib = models.CharField(max_length=254)
    position = models.CharField(max_length=254)
    start_date = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=254)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['pib']

    def serialize_short(self):
        data = {'id': self.id, 'pib': self.pib, 'position': self.position}
        return data

    def serialize(self):
        data = {'id': self.id, 'pib': self.pib, 'position': self.position,
                'start_date': self.start_date, 'email': self.email}
        if self.parent_id:
            data['headman'] = {'id': self.parent_id, 'pib': self.parent.pib}
        return data
