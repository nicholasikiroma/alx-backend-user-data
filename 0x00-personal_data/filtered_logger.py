#!/usr/bin/env python3
"""Module for Log Filtering"""
import mysql.connector
import os
import logging
from typing import List
import re


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """formats log output"""
        return filter_datum(
            self.fields, self.REDACTION, super().format(record), self.SEPARATOR
        )


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """returns the log message obfuscated
    Args:
            - fields: a list of strings representing all fields to obfuscate
            - redaction: a string representing by what the field will
              be obfuscated
            - message: a string representing the log line
            - separator: a string representing by which character is
              separating all fields in the log line (message)
    """
    pattern = "|".join(fields)
    return re.sub(
        rf"({pattern})=.*?{re.escape(separator)}",
        rf"\1={redaction}{separator}",
        message,
    )


def get_logger() -> logging.Logger:
    """returns logger object"""
    log = logging.getLogger("user_data")
    log.setLevel(logging.INFO)
    log.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    log.addHandler(stream_handler)

    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    returns a MySQL Database connector
    """
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")

    connector = mysql.connector.connect(
        user=user, password=password, host=host, database=database
    )

    return connector


def main():
    """
    function that takes no arguments and
    returns nothing.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    for row in data:
        for coloumn in row:
            print(coloumn)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
