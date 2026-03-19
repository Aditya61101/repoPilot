import os
import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver

def get_checkpointer():
    os.makedirs("storage", exist_ok=True)
    conn = sqlite3.connect(
        "storage/checkpoints.db",
        check_same_thread=False
    )
    return SqliteSaver(conn)