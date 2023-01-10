import os
import sys

import mysql.connector


def main(config):
    output = []
    db = mysql.connector.Connect(**config)
    cursor = db.cursor()

    # Select it again and show it
    stmt_select = "SHOW ENGINES"
    cursor.execute(stmt_select)
    rows = cursor.fetchall()

    for row in rows:
        output.append(repr(row))

    db.close()
    return output


if __name__ == "__main__":

    config = {
        "host": "127.0.0.1",
        "port": 3306,
        "database": "db_gerenciador",
        "user": "root",
        "password": "12345",
        "charset": "utf8",
    }

    out = main(config)
    print("\n".join(out))