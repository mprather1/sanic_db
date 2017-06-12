from sanic import Sanic
import ssl
from sanic.response import json
from sanic.response import text
import os
import asyncio
import aiopg
import uvloop

database_name = os.environ['DATABASE_NAME']
database_host = os.environ['DATABASE_HOST']
database_user = os.environ['DATABASE_USER']
database_password = os.environ['DATABASE_PASSWORD']

connection = 'postgres://{0}:{1}@{2}/{3}'.format(database_user,
                                                 database_password, 
                                                 database_host,
                                                 database_name)
                                                 
async def get_pool():
  return await aiopg.create_pool

app = Sanic()

@app.route("/models")
async def handle(request):
  result = []
  async def test_select():
    async with aiopg.create_pool(connection) as pool:
      async with pool.acquire() as conn:
        async with conn.cursor() as cur:
          await cur.execute('SELECT name, attribute, created_at FROM models')
          async for row in cur:
            result.append({'name': row[0], 'attribute': row[1], 'created_at': row[2]})
  res = await test_select()
  return json({'data': result})
  
@app.route('/create_model', methods=['POST',])
async def create_model(request):
  print(request.body)
  async with aiopg.create_pool(connection) as pool:
    async with pool.acquire() as conn:
      async with conn.cursor() as cur:
        await cur.execute("INSERT INTO models(name, attribute) VALUES(%s, %s)", (request.form.get('name'), request.form.get('attribute')))  
  return json({'received': True, 'form_data': request.form, 'name': request.form.get('name'), 'attribute': request.form.get('attribute')})
  
# SSL= os.environ['SSL']

# context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)

# context.load_cert_chain(SSL + '/fullchain.pem', keyfile=SSL + '/privkey.pem')  
if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8000, debug=True)