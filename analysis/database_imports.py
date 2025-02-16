# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: python_recommender
#     language: python
#     name: python3
# ---

# %%
import psycopg2

# %%
conn_string = "host='localhost' dbname='winedb' user='petedavis'"
conn = psycopg2.connect(conn_string)

# %%
cur = conn.cursor()

# %%
conn.rollback()

# %%
,country,description,designation,points,price_dollars,province,region,title,variety,winery

# %%
cur.execute('''CREATE TABLE winemag (
    country VARCHAR(100),
    description TEXT,
    designation VARCHAR(255),
    points INT,
    price_dollars NUMERIC(10, 2),
    province VARCHAR(100),
    region VARCHAR(100),
    "title" VARCHAR(255),
    variety VARCHAR(100),
    winery VARCHAR(255)
);''')

# %%
sql_copy = '''COPY winemag(country, description, designation, points, price_dollars,\
    province, region, title, variety, winery) 
FROM '/Users/petedavis/davis/repos/wine-recommendations/assets/winemag_processed.csv' 
DELIMITER ',' 
CSV HEADER;
'''

# %%
cur.execute(sql_copy)

# %%
test = ''' select * from winemag'''

# %%
cur.execute(test)

# %%
for i in cur.fetchall():
    print(i)

# %%
conn.commit()
# Close cursor and communication with the database
cur.close()

# %%



