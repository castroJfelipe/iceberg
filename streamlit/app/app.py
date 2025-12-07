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
        'empresa.id': st.checkbox("Empresa ID"),
        'empresa.name': st.checkbox("Empresa nombre"),
        'empresa.test': st.checkbox("Empresa de prueba"),
        'trabajador.id': st.checkbox("Empleado ID"),
        'trabajador.name': st.checkbox("Empleado nombre"),
        'contrato.id': st.checkbox("Contrato ID"),
        'contrato.contract_id': st.checkbox("Contrato código"),
        'contrato.since': st.checkbox("Contrato Desde"),
        'contrato.until': st.checkbox("Contrato Hasta"),
        'contrato.position': st.checkbox("Contrato Cargo"),
    }
    submitted = st.form_submit_button("Generar")
    if submitted:
        select = []
        columns = []
        for key in checkbox.keys():
            if checkbox[key]:
                select.append(key)
                columns.append(key)
        select = (',').join(select)

        cur = conn.cursor()
        cur.execute(
            f"select {select} "
            "from iceberg.nyc.company empresa, "
            "unnest(empresa.employee) trabajador,"
            "unnest(trabajador.contract) contrato "
        )
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=columns).drop_duplicates()

        st.dataframe(df)


