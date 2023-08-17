import streamlit as st
from sqlalchemy.sql import text

# Create the SQL connection to pets_db as specified in your secrets file.
conn = st.experimental_connection('kb_db', type='sql', ttl=0)

# Insert some data with conn.session.
with conn.session as s:
    s.execute(text('''CREATE TABLE IF NOT EXISTS documents
       (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
       title           TEXT    NOT NULL,
       content         TEXT     NOT NULL);'''))

with st.form("import document"):
    title = st.text_input('Title')
    content = st.text_area('Content')

    # Every form must have a submit button.
    submitted = st.form_submit_button("Save")
    if submitted:
        with conn.session as s:
            s.execute(text('''INSERT INTO documents (title, content)
                            VALUES (:title, :content);'''),
                      params=dict(title=title, content=content)
                      )
            s.commit()

# Query and display the data you inserted
documents = conn.query(
    'SELECT * FROM documents ORDER BY id desc LIMIT 10;',
    ttl=0)
st.dataframe(documents)
