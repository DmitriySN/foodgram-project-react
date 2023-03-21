import json
import sqlite3

conn = sqlite3.connect("../backend/db.sqlite3")

newegg_json = json.load(open("../data/ingredients.json", encoding="utf-8-sig"))

columns = []
column = []
for data in newegg_json:
    column = list(data.keys())
    for col in column:
        if col not in columns:
            columns.append(col)
# print(columns)
value = []
values = []
num = 1
for data in newegg_json:
    value.append(int(num))
    for i in columns:
        value.append(str(dict(data).get(i)))
    values.append(list(value))
    value.clear()
    num += 1

# create_query = 'create table if not exists table_newegg
# (id, name, measurement_unit)'
insert_query = "insert into recipes_ingredient values (?,?,?)"
c = conn.cursor()
# c.execute(create_query)
c.executemany(insert_query, values)
conn.commit()
c.close()
