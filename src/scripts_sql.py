sql_create_templates_table = """
CREATE TABLE IF NOT EXISTS templates (
    id INTEGER PRIMARY KEY,
    template_name TEXT NOT NULL UNIQUE,
    content TEXT
);
"""

sql_create_sent_messages_table = """
CREATE TABLE IF NOT EXISTS sent_messages (
    id INTEGER PRIMARY KEY,
    sent_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    phone TEXT NOT NULL,
    name TEXT NOT NULL,
    message TEXT NOT NULL
);
"""

sql_create_scheduled_messages_table = """
CREATE TABLE IF NOT EXISTS scheduled_messages (
    id INTEGER PRIMARY KEY,
    phone TEXT NOT NULL,
    message_content TEXT NOT NULL,
    scheduled_time TIMESTAMP NOT NULL
);
"""


sql_query_count_templates = """SELECT count(*) FROM templates"""

sql_query_all_templates = """SELECT * FROM templates ORDER BY template_name"""

