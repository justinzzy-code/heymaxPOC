from django.contrib.auth.models import User
from django.db import models
import datetime

class Book(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=200, null=False)
    avaliable_to_give = models.BooleanField(default=False) #Whether book is avaliable to exchange/trade
    image = models.ImageField(upload_to='uploads/', blank=True)
    genre = models.CharField(max_length=200, null=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, default=User, null=False)




STATUS_CHOICES = (("PENDING","PENDING"),
                  ("DENIED","DENIED"), 
                  ("APPROVED","APPROVED"), 
                  ("CANCELLED", "CANCELLED"),
                  ("TERMINATED","TERMINATED"),
                  ("COMPLETED","COMPLETED")
                  )

class ExchangeRequest(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    #requested_book = models.ForeignKey(to=Book, on_delete=models.CASCADE, null=False)
    start_date = models.DateTimeField(max_length=200)
    end_date = models.DateTimeField(max_length=200)
    book_id = models.PositiveIntegerField(default = 0, null=False, blank=False) 
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    