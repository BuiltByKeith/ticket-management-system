from django.db import models
from ulid import ULID

def generate_ulid():
    return str(ULID())

class ConcernType(models.Model):
    id = models.BigAutoField(primary_key=True)  # Internal primary key
    ulid = models.CharField(max_length=26, unique=True, default=generate_ulid, editable=False)  # Public identifier
    
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        db_table = 'concern_types'
        ordering = ['name']
        
    def __str__(self):
        return self.name