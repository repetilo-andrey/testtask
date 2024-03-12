from django.db import models
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey


class Coworker(MPTTModel):
    pib = models.CharField(max_length=254)
    position = models.CharField(max_length=254)
    start_date = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=254)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['pib']

    def __str__(self):
        return self.pib

    def serialize_short(self):
        data = {'id': self.id, 'pib': self.pib, 'position': self.position}
        return data

    def serialize(self, editable=False):
        pib = self.pib
        if editable:
            link = reverse('coworker_edit_view', args=[self.id])
            pib += '<a class="edit-link" href="%s">Edit</a>' % link
        data = {'pib': pib, 'position': self.position, 'start_date': self.start_date, 'email': self.email,
                'parent': self.parent.pib if self.parent_id else ''}
        return data
