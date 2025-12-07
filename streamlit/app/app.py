import pandas as pd
import trino
import streamlit as st
import json

conn = trino.dbapi.connect(
    host='http://iceberg-trino',
    port=8070,
    user='jcastro',
    catalog='iceberg'
)

cur = conn.cursor()
cur.execute(
    "select cmp.id, cmp.name, cmp.test, "
    "   emp.id employee_id, emp.name employee_name, "
    "   ctc.id contract_id, ctc.contract_id contract_contract_id, "
    "   ctc.since contract_since, ctc.until contract_until, "
    "   ctc.position contract_position "
    "from iceberg.nyc.company cmp, "
    "unnest(cmp.employee) emp,"
    "unnest(emp.contract) ctc "
)
rows = cur.fetchall()
df = pd.DataFrame(rows)
print(df.head(2))
st.dataframe(df)