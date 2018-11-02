#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from moretime.tool import db

engine, session_maker = db.conn("dev")

sql = """
SELECT user_id, city_id, sum(end_ts-start_ts) AS time FROM time_sharing
WHERE city_id IS NOT NULL
GROUP BY user_id, city_id
ORDER BY time DESC
LIMIT 30 OFFSET 0
"""
db = session_maker()
result = db.execute(sql).fetchall()
print(result)

df = pd.DataFrame(result, columns=["user_id", "city_id", "share_time"])
print(df)

city_ids = df.city_id.unique()
for city_id in city_ids:
    print(city_id)
    ranked = df[df.city_id == city_id]\
        .sort_values(by=['share_time'], ascending=False)
    print(list(ranked["user_id"]))

grouped = dict(list(df.groupby("city_id")))
