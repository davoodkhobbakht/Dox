from django.db import DefaultConnectionProxy, models
from django.db.models.enums import IntegerChoices
from django.db.models.fields import BooleanField, CharField, IntegerField
from django.db.models.fields import related
from django.db.models.fields.related import OneToOneField
from uuid import uuid4

# Create your models here.
class Product(models.Model):
    RATE_CHOICES=(
        ("1","*"),
        ("2","**"),
        ("3","***"),
        ("4","****"),
        ("5","*****"),
    )
    RATE_CHOICES=(
        ("available",'available'),
        ("not_availabke", 'not available'),
        ("comming_soon", 'comming soon'),
    )
    name = CharField(max_length=40)

    image = CharField(default='path-to-defualt.jpg')
    price = models.PositiveIntegerField(blank=True,null=True)
    description = models.CharField(max_length = 350)
    available_number = models.models.PositiveIntegerField(Default = 0 ,blank = False, null = False)
    is_available = models.CharField(default= False)
    product_code =  models.CharField(unique=True, max_length=12,blank=True)
    category = models.CharField(max_length=30,blank=True)
    color = models.CharField(max_length=10,blank=True,default='#FFFFF')
    rate = models.CharField(choices= RATE_CHOICES)
    
    def code_generate():# generate an uuid4 code for product_code
        code = str( uuid4()).replace('-','')[:12]
        return code
    def __str__(self) -> str:#return a string that represents each object
        return f"{self.name}-{self.product_code}-{self.price}"
    def save(self, *args , **kwargs):
        try: #create product code
            if self.product_code == "":
                code = self.code_generate()
                self.product_code = code
            super().save(*args,**kwargs) 
        except:
            self.save() #create another code