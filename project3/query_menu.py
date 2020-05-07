import requests
import re

from bs4 import BeautifulSoup
from orders.models import *
from django.db import IntegrityError


def get_menu():
    r = requests.get('http://www.pinocchiospizza.net/menu.html')    
    soup = BeautifulSoup(r.content, 'html.parser')
    food = {}
    food['Sizes'] = []
    for row in soup.select('table.foodmenu tr'):
        section = row.select('a')
        if section:
            key = section[0].text
            food[key] = []
        vals = [x.text for x in row.select('td')]
        if vals and vals[0]:
            food[key].append(vals)
        elif not food['Sizes'] and vals and not vals[0]:
            food['Sizes'] = [vals[1], vals[2]]

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

def migrate_data():
    data = get_menu()

    s_small = Size(name=data['Sizes'][0])
    s_small.save()
    s_large = Size(name=data['Sizes'][1])
    s_large.save()
    sizes = [s_small, s_large]

    for top in data['Toppings']:
        Topping(name=top).save()
    
    class_map = {
        'SubAdditions':SubAddition,
        'Salads':Salad,
        'Pasta': Pasta,
    }
    for name in class_map:
        for item in data[name]:
            class_map[name](name=item[0], price=float(item[1])).save()
    
    class_map = {
        'Subs': (SubName, Sub),
        'Dinner Platters': (DinnerPlatterName, DinnerPlatter),
    }
    for name in class_map:
        for row in data[name]:              
            item_name = class_map[name][0](name=row[0])
            item_name.save()
            for i in [0,1]:
                try:
                    class_map[name][1](name=item_name, \
                        price=float(row[i+1]), size=sizes[i]).save()
                except:
                    continue
        
    for name in ['Regular Pizza', 'Sicilian Pizza']:
        p_type = PizzaType(name=name)
        p_type.save()
        for row in data[name]:
            try:
                p_title = PizzaTitle(name=row[0])
                r = re.match('\d+', row[0])
                if r:
                    p_title.number_of_toppings = int(r.group(0))
                p_title.save()
            except IntegrityError as e:
                p_title = PizzaTitle.objects.get(name=row[0])
            for i in [0,1]:
                Pizza(pizza_type=p_type, pizza_title=p_title, 
                    price=float(row[i+1]), size=sizes[i]).save()
            
if __name__ == '__main__':
    migrate_data()