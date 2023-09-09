from sqlalchemy import create_engine, text
engine = create_engine("sqlite:////Chinook.db")

# 查看所有的table
with engine.connect() as conn:
  sql = '''select name from sqlite_master where type = 'table' '''
  res = conn.execute(text(sql))
  for row in res:
    print(row)
