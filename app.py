from sanic import Sanic
from sanic.response import json
from sanic.response import text
import asyncio
import aiopg
import uvloop
import os
# import ssl

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

@app.route("/models", methods=["GET",])
async def handle(request):
  result = []
  async def test_select():
    async with aiopg.create_pool(connection) as pool:
      async with pool.acquire() as conn:
        async with conn.cursor() as cur:
          await cur.execute('SELECT id, name, attribute, created_at FROM models')
          async for row in cur:
            result.append({'id': row[0], 'name': row[1], 'attribute': row[2], 'created_at': row[3]})
  res = await test_select()
  return json({'data': result})
  
@app.route('/models', methods=['POST',])
async def handle(request):
  async with aiopg.create_pool(connection) as pool:
    async with pool.acquire() as conn:
      async with conn.cursor() as cur:
        await cur.execute("INSERT INTO models(name, attribute) VALUES(%s, %s)", (request.form.get('name'), request.form.get('attribute')))  
  return json({'received': True, 'form_data': request.form})
  
@app.route('/models/<id>', methods=["GET"])
async def handle(request, id):
  result = []
  async def select():
    async with aiopg.create_pool(connection) as pool:
      async with pool.acquire() as conn:
        async with conn.cursor() as cur:
          await cur.execute('SELECT id, name, attribute, created_at FROM models WHERE id=' + id)
          async for row in cur:
            result.append({'id': row[0], 'name': row[1], 'attribute': row[2], 'created_at': row[3]})
  res = await select()
  return json({'data': result})
  
@app.route('/models/<id>', methods=['PUT',])
async def handle(request, id):
  async with aiopg.create_pool(connection) as pool:
    async with pool.acquire() as conn:
      async with conn.cursor() as cur:
        await cur.execute("UPDATE models SET name=%s, attribute=%s WHERE id=%s", (request.form.get('name'), request.form.get('attribute'), id))  
  return json({'received': True, 'form_data': request.form})  
  
@app.route('/models/<id>', methods=['DELETE',])
async def handle(request, id):
  async with aiopg.create_pool(connection) as pool:
    async with pool.acquire() as conn:
      async with conn.cursor() as cur:
        await cur.execute("DELETE FROM models where id = " + id)  
  return json({'received': True})
  
# SSL= os.environ['SSL']

# context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)

# context.load_cert_chain(SSL + '/fullchain.pem', keyfile=SSL + '/privkey.pem')

if __name__ == '__main__':
  app.run(host="localhost", port=8000, debug=True)