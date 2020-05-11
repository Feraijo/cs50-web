from django.db import models

class MenuName(models.Model):    
    name = models.CharField(max_length=128, unique=True)
    
    def __str__(self):
       return self.name

    class Meta:
        abstract = True

class MenuPrice(models.Model):
    price_large = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    price_small = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    class Meta:
        abstract = True

class Pizza(MenuPrice):
    name = models.CharField(max_length=128)
    number_of_toppings = models.PositiveSmallIntegerField(null=True, blank=True)   
    pizza_type = models.ForeignKey('PizzaType', on_delete=models.CASCADE)    
    
    class Meta:
        unique_together = (('name', 'pizza_type'),)

    def __str__(self):
       return f'{self.pizza_type} - {self.name}'

class Sub(MenuName, MenuPrice):
    pass

class DinnerPlatter(MenuName, MenuPrice):
    pass

class Pasta(MenuName, MenuPrice):
    pass
    
class Salad(MenuName, MenuPrice):
    pass   
    
class PizzaType(MenuName):
    pass

class SubAddition(MenuName, MenuPrice):
    pass

class Topping(MenuName):
    pass
