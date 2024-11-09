from fastapi import FastAPI
from redis_om import get_redis_connection , HashModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
import requests
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"message": "Hello, world!"}

redis = get_redis_connection(
   host='redis-14199.c261.us-east-1-4.ec2.redns.redis-cloud.com',
   port=14199,
   password='CXCcgCTFyPThUI4BkJp4kSofBeK0kFbh',
   decode_responses = True
)

class Order(HashModel):
    product_id : str
    price : float
    fee : float
    total : float
    quantity: int
    status : str
    
    class Meta:
        database = redis
        

@app.post("/orders")
async def create(request : Request):
    body =await request.json()
    
    req = requests.get('http://localhost:8000/products/%s'% body['id'])
       
  
    
    order = Order(
        product_id = body['id'],
        price = body['price'],
        fee = 0.2*body['price'],
        total = 1.2*body['price'],
        quantity = body['quantity'],
        status = "pending"
    )
    order.save()
    
    
    return order