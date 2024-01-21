import pandas as pd
import os
import sqlite3


class DBConnectionManager:
    db_directory = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')),
                                "MFA_analysis.db")

    @staticmethod
    def start():
        DBConnectionManager.conn = sqlite3.connect(directory)

    """
    Example usage:
    table_name = "organisms"
    columns = ["name", "GCF"]
    data = [("Organism1", "123"), ("Organism2", "456")]
    """
    @staticmethod
    def insert(table_name, columns: list, data: list):
        query = f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({", ".join(["?"] * len(columns))})'
        cursor = DBConnectionManager.conn.cursor()
        cursor.executemany(query, data)
        conn.commit()

    @staticmethod
    def extract_all(table_name):
        query = f"SELECT * FROM {table_name};"
        cursor.execute(query)
        rows = cursor.fetchall()

        if not rows:
            return None

        columns = [col[0] for col in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        return df

    @staticmethod
    def extract_by_target(table_name, column, target):
        query = f"SELECT * FROM {table_name} WHERE {column} = ?;"
        cursor.execute(query, (target,))
        rows = cursor.fetchall()

        if not rows:
            return None

        columns = [col[0] for col in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        return df

    @staticmethod
    def close():
        DBConnectionManager.conn.close()
