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

with st.form("my_form"):
    st.write("Selecciona los campos:")
    checkbox = {
        'empresa.id': st.checkbox("empresa.id"),
        'empresa.name': st.checkbox("empresa.name"),
        'empresa.test': st.checkbox("empresa.test"),
        'trabajador.id': st.checkbox("trabajador.id"),
        'trabajador.name': st.checkbox("trabajador.name"),
        'contrato.id': st.checkbox("contrato.id"),
        'contrato.contract_id': st.checkbox("contrato.contract_id"),
        'contrato.since': st.checkbox("contrato.since"),
        'contrato.until': st.checkbox("contrato.until"),
        'contrato.position': st.checkbox("contrato.position"),
    }
    option = st.selectbox(
        "Filtro",
        ("empresa.id", "empresa.name", "empresa.test", "trabajador.id", 
         "trabajador.name", "trabajador.id", "contrato.id", "contrato.since",
         "contrato.until", "contrato.position")
    )
    operator = st.selectbox("operador", ("=", "<", ">", "<=", ">=", "<>"))
    if option in ["empresa.id", "trabajador.id", "contrato.id"]:
        input = st.number_input("")
    elif option in ["empresa.name", "trabajador.name", "contrato.position"]:
        input = st.text_input("")
    elif option in ["contrato.since", "contrato.until"]:
        input = st.date_input("")

    submitted = st.form_submit_button("Generar")
    if submitted:
        select = []
        columns = []
        for key in checkbox.keys():
            if checkbox[key]:
                select.append(key)
        select_comma = (',').join(select)
        where = f"and {option} {operator} {input}"
        cur = conn.cursor()
        cur.execute(
            f"select {select_comma} "
            "from iceberg.nyc.company empresa, "
            "unnest(empresa.employee) trabajador,"
            "unnest(trabajador.contract) contrato "
            "where 1=1 "
            f"{where}"
        )
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=select).drop_duplicates()

        st.dataframe(df)


