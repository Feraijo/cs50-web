import requests
import re

from bs4 import BeautifulSoup
from orders.models import *
from django.db import IntegrityError


def get_menu():
    r = requests.get('http://www.pinocchiospizza.net/menu.html')    
    soup = BeautifulSoup(r.content, 'html.parser')
    food = {}
    for row in soup.select('table.foodmenu tr'):
        section = row.select('a')
        if section:
            key = section[0].text
            food[key] = []
        vals = [x.text for x in row.select('td')]
        if vals and vals[0]:
            food[key].append(vals)        

    sub_add = [sub for sub in food['Subs'] if '+' in sub[1] or '+' in sub[2]]        
    for i, sub in enumerate(sub_add):
        food['Subs'].remove(sub)
        sub_add[i] = [s.replace('+', '').strip() for s in sub]
    food['SubAdditions'] = sub_add

    food['Toppings'] = [t.text for t in soup.select('table.toppingmenu td')]

    for dp in food['Dinner Platters']:        
        [dp.append(x) for x in re.findall('\d+\.\d+', dp[1])]
        dp.remove(dp[1])
    
    return food

def get_float_or_None(ft):
    return float(ft) if ft else None

def migrate_data():
    data = get_menu()

    class_map = {}
    for key in data:
        if key in ['Toppings', 'SubAdditions']:
            k = AddType(name=key)
        else:
            k = ItemType(name=key)
        k.save()
        class_map[key] = k
    
# 'Toppings': ['Pepperoni', 'Sausage', 'Mushrooms', 'Onions', 'Ham', 'Canadian Bacon', 'Pineapple', 'Eggplant', 'Tomato & Basil', 'Green Peppers', 'Hamburger', 'Spinach', 'Artichoke', 'Buffalo Chicken', 'Barbecue Chicken', 'Anchovies', 'Black Olives', 'Fresh Garlic', 'Zucchini']}
    for top in data['Toppings']:
        Addition(add_type=class_map['Toppings'], name=top).save()
    
# 'SubAdditions': [['Mushrooms', '0.50', '0.50'], ['Green Peppers', '0.50', '0.50'], ['Onions', '0.50', '0.50'], ['Extra Cheese on any sub', '0.50', '0.50']], 
    for sub_add in data['SubAdditions']:
        Addition(add_type=class_map['SubAdditions'], name=sub_add[0], price=get_float_or_None(sub_add[1])).save()

# 'Salads': [['Garden Salad', '6.25'], ['Greek Salad', '8.25'], ['Antipasto', '8.25'], ['Salad w/Tuna', '8.25']], 
# 'Pasta': [['Baked Ziti w/Mozzarella', '6.50'], ['Baked Ziti w/Meatballs', '8.75'], ['Baked Ziti w/Chicken', '9.75']], 
    for name in ['Salads', 'Pasta']:
        for item in data[name]:
            MenuItem(item_type=class_map[name], name=item[0], price_small=get_float_or_None(item[1])).save()            
    
# 'Subs': [['Cheese', '6.50', '7.95'], ['Italian', '6.50', '7.95'], ['Ham + Cheese', '6.50', '7.95'], ['Meatball', '6.50', '7.95'], ['Tuna', '6.50', '7.95'], ['Turkey', '7.50', '8.50'], ['Chicken Parmigiana', '7.50', '8.50'], ['Eggplant Parmigiana', '6.50', '7.95'], ['Steak', '6.50', '7.95'], ['Steak + Cheese', '6.95', '8.50'], ['Sausage, Peppers & Onions', '', '8.50'], ['Hamburger', '4.60', '6.95'], ['Cheeseburger', '5.10', '7.45'], ['Fried Chicken', '6.95', '8.50'], ['Veggie', '6.95', '8.50']], 
# 'Dinner Platters': [['Garden Salad', '40.00', '65.00'], ['Greek Salad', '50.00', '75.00'], ['Antipasto', '50.00', '75.00'], ['Baked Ziti', '40.00', '65.00'], ['Meatball Parm', '50.00', '75.00'], ['Chicken Parm', '55.00', '85.00']], 
    for name in ['Subs', 'Dinner Platters']:
        for item in data[name]:
            MenuItem(
                item_type=class_map[name],
                name=item[0], 
                price_small=get_float_or_None(item[1]), 
                price_large=get_float_or_None(item[2])
                ).save()
            
# 'Regular Pizza': [['Cheese', '12.70', '17.95'], ['1 topping', '13.70', '19.95'], ['2 toppings', '15.20', '21.95'], ['3 toppings', '16.20', '23.95'], ['Special', '17.75', '25.95']], 
# 'Sicilian Pizza': [['Cheese', '24.45', '38.70'], ['1 item', '26.45', '40.70'], ['2 items', '28.45', '42.70'], ['3 items', '29.45', '44.70'], ['Special', '30.45', '45.70']], 
    for name in ['Regular Pizza', 'Sicilian Pizza']:
        for item in data[name]:
            p = MenuItem(
                item_type=class_map[name],
                name=item[0], 
                price_small=get_float_or_None(item[1]), 
                price_large=get_float_or_None(item[2]),
                )
            r = re.match('\d+', item[0])
            if r:
                p.number_of_toppings = int(r.group(0))
            p.save()
            
if __name__ == '__main__':
    migrate_data()
    #print(get_menu())