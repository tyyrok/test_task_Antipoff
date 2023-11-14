from django.db import models

class CadastralNumber(models.Model):
    """Simple model for cadastral number"""
    number = models.CharField(max_length=16)
    long = models.CharField(max_length=9)
    alt = models.CharField(max_length=9)

class History(models.Model):
    """Model for store user's requests history"""
    REQUEST_TYPES = [
        ('query', 'Query'),
        ('result', 'Result query'),
        ('history', 'History query')
    ]
    request_type = models.CharField(
        max_length=7, choices=REQUEST_TYPES, blank=True
    )
    response = models.BooleanField(blank=True)
    number = models.ForeignKey(to=CadastralNumber, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(blank=True)