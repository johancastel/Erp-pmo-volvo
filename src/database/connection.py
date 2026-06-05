# src/database/connection.py
import os
import sqlite3
import pymysql
import streamlit as st
from src.config.settings import (
    DEFAULT_DB_HOST, DEFAULT_DB_USER, DEFAULT_DB_PASSWORD, 
    DEFAULT_DB_NAME, DEFAULT_DB_PORT
)

class ConnectionManager:
    def __init__(self):
        self._db_type = None
        self.sqlite_path = os.path.join(os.getcwd(), "erp_pmo.db")
        self._db_initialized = False

    def get_connection(self, host=DEFAULT_DB_HOST, user=DEFAULT_DB_USER, password=DEFAULT_DB_PASSWORD, db_name=DEFAULT_DB_NAME, port=DEFAULT_DB_PORT):
        """
        Retrieves a database connection (MySQL or SQLite fallback).
        Uses a connection pool/cache for the connection type to avoid network latency.
        """
        # 1. If SQLite was already selected, use it directly
        if self._db_type == "SQLite":
            conn = sqlite3.connect(self.sqlite_path)
            conn.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            return conn, "SQLite"

        # 2. If MySQL was already selected, try to connect, fallback on failure
        if self._db_type == "MySQL":
            try:
                conn = pymysql.connect(
                    host=host,
                    user=user,
                    password=password,
                    port=int(port),
                    database=db_name,
                    cursorclass=pymysql.cursors.DictCursor,
                    connect_timeout=3
                )
                return conn, "MySQL"
            except Exception:
                self._db_type = "SQLite"
                conn = sqlite3.connect(self.sqlite_path)
                conn.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
                return conn, "SQLite"

        # 3. Initial connection type check
        try:
            conn = pymysql.connect(
                host=host,
                user=user,
                password=password,
                port=int(port),
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=3
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            cursor.close()
            
            conn.select_db(db_name)
            self._db_type = "MySQL"
            return conn, "MySQL"
        except Exception:
            self._db_type = "SQLite"
            conn = sqlite3.connect(self.sqlite_path)
            conn.row_factory = lambda cursor, row: {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
            return conn, "SQLite"

    def clear_db_type_cache(self):
        self._db_type = None
        self._db_initialized = False

@st.cache_resource
def get_connection_manager():
    return ConnectionManager()
