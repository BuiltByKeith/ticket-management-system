from django.db import models
from apps.offices.models import Office
from ulid import ULID

def generate_ulid():
    return str(ULID())


class System(models.Model):
    id = models.BigAutoField(primary_key=True)  # Internal primary key
    ulid = models.CharField(max_length=26, unique=True, default=generate_ulid, editable=False)  # Public identifier
    name = models.CharField(max_length=200)
    acronym = models.CharField(max_length=20, blank=True)
    office = models.ForeignKey(Office, on_delete=models.PROTECT, related_name='systems')
    tech_stack_used = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'systems'
        ordering = ['name']
        
    def __str__(self):
        return self.acronym or self.name