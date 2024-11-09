
from main import Product , redis
import time

try:
    key = "order_completion"
    group = "inventory_group"
    redis.xgroup_create(key,group)
except:
    print("group already exists")
    
while(True):
   try:
     results  = redis.xreadgroup(group,key,{key : ">"},None)
     if results != []:
         for result in results:
             obj = result[1][0][1]
             product = Product.get(obj['product_id'])
             print(product)
             product.quantity = product.quantity - int(obj['quantity'])
             product.save()
     
   except Exception as e:
     print(str(e))  
   time.sleep(1)  