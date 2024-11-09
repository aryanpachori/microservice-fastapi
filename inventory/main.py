from fastapi import FastAPI
from redis_om import get_redis_connection , HashModel
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, world!"}

redis = get_redis_connection(
   host='redis-14199.c261.us-east-1-4.ec2.redns.redis-cloud.com',
   port=14199,
   password='CXCcgCTFyPThUI4BkJp4kSofBeK0kFbh'
)

class Product(HashModel):
    name : str
    price : float
    quantity : int

    class Meta:
        database = redis

@app.get('/products')
def all():
   return [getAll(pk) for pk in Product.all_pks()]
def getAll(pk : str):
    product  = Product.get(pk)
    return{
        'id' : product.pk,
        'name' : product.name,
        'price' : product.price,
        'quantity' : product.quantity
        
    }

@app.post('/create')
def create(product : Product):
   return product.save() 

@app.get('/products/{pk}')
def get(pk : str):
    return Product.get(pk)

@app.delete('/products/{pk}')
def delete(pk : str):
   return  Product.delete(pk)