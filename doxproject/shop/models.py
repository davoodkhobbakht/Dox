from functools import total_ordering
from django.db import DefaultConnectionProxy, models
from django.db.models.deletion import CASCADE
from django.db.models.enums import IntegerChoices
from django.db.models.fields import BooleanField, CharField, DateField, IntegerField
from django.db.models.fields import related
from django.db.models.fields.related import OneToOneField
from uuid import uuid4
from user.models import User

# Create your models here.
class Product(models.Model):



    RATE_CHOICES=(
        ("1","*"),
        ("2","**"),
        ("3","***"),
        ("4","****"),
        ("5","*****"),
    )
    AVAILABLE_CHOICES=(
        ("available",'available'),
        ("not_availabke", 'not available'),
        ("comming_soon", 'comming soon'),
    )
    name = CharField(max_length=40)
    image = CharField(default='path-to-defualt.jpg')
    price = models.PositiveIntegerField(blank=True,null=True)
    description = models.CharField(max_length = 350)
    available_number = models.models.PositiveIntegerField(Default = 0 ,blank = False, null = False)
    is_available = models.CharField(max_length = 20 ,choices = AVAILABLE_CHOICES)
    product_code =  models.CharField(unique=True, max_length=12,blank=True)
    category = models.ForeignKey(Category ,null = True,blank=True)
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

class  Cart(models.Model):
    user = OneToOneField(User,on_delete=CASCADE)
    product_list = CharField(max_length=300,blank=True,null=True)
    order_id = CharField(max_length=12)
    total_Price = IntegerField(default=0)
    
    def code_generate():# generate an uuid4 code for order_id
        code = str( uuid4()).replace('-','')[:12]
        return code

    def save(self, *args , **kwargs):
        self.order_id = self.code_generate()
        #fill total price
        total = 0
        for product_id in self.product_list.split(' '): 
            total += int(Product.objects.filter(product_code = product_id).price) #add up product_list prices
        self.total_Price = total 
        super().save(*args,**kwargs) 
    
    def __str__(self) -> str:#return a string that represents each object
        return f"{self.user}-{self.product_list}-{self.total_price}"
    
    def add_product(self,product_id):
        if Product.objects.filter(product_code = product_id).exists():
            self.product_list += " " + product_id
    
    def remove_product(self , product_id):
        if product_id in self.product_list:
           self.product_list = str(self.product_list).replace(product_id,'')
    
