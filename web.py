import streamlit as st
from sqlalchemy.sql import text

# Create the SQL connection to pets_db as specified in your secrets file.
conn = st.experimental_connection('kb_db', type='sql')

# Insert some data with conn.session.
with conn.session as s:
    s.execute(text('''CREATE TABLE IF NOT EXISTS documents
       (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
       title           TEXT    NOT NULL,
       content         TEXT     NOT NULL);'''))

tab1, tab2 = st.tabs(["Search", "Import"])

with tab1:
    with st.form("search"):
        keyword = st.text_input('keyword')

        # Every form must have a submit button.
        submitted = st.form_submit_button("Search")
        if submitted:
            documents = conn.query('SELECT * FROM documents WHERE content LIKE "%'
                                   + keyword + '%" ORDER BY id desc LIMIT 10;',
                                   ttl=0)
            st.dataframe(documents)

with tab2:
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
