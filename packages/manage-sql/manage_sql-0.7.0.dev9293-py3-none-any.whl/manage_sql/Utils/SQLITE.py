import sqlite3 as sq
import os

try:
    from ..Utils.utils_sqlite import (
        Types,
        Table,
        Column,
        ColumnData,
        Filter,
        EncryptValue
    )

except:
    from .utils_sqlite import (
        Types,
        Table,
        Column,
        ColumnData,
        Filter,
        EncryptValue
    )

class SQLITE:
    def __init__(
        self,
        database: str,
        path: str = 'database'
    ):
        self.__database = database
        self.__path = path
        self.column_types = Types
        self.column = Column
        self.filter_by = Filter
        self.delete_by = Filter
        self.column_data = ColumnData
    
    @property
    def __connect(self) -> tuple[sq.Connection, sq.Cursor]:

        def create_connection() -> tuple[sq.Connection, sq.Cursor]:

            if not self.__path.endswith('.db'):
                self.__path = os.path.join(self.__path, f'{self.__database}.db')

            connection = sq.connect(self.__path)
            cursor = connection.cursor()

            return connection, cursor
        
        try:
            os.mkdir(path=self.__path)

            return create_connection()
        
        except Exception as e:
            if 'WinError 183' in str(e):
                return create_connection()
            
            else:
                self.__exception_error(message_error=e)
    
    @property
    def tables(self) -> list[Table]:
        
        connection, cursor = self.__connect
            
        tables = cursor.execute(
            'SELECT name FROM sqlite_master WHERE type = "table"'
        ).fetchall()

        db_tables: list[Table] = []

        for table in tables:
            if table[0] != 'sqlite_sequence':
                table_info = Table(name=table[0])
                columns = cursor.execute(
                    f'PRAGMA table_info({table[0]})'
                ).fetchall()

                for column in columns:
                    table_info.columns.append(
                        Column(
                            name=column[1],
                            column_type=self.column_types(value=column[2])
                        )
                    )
                
                db_tables.append(table_info)
        
        connection.close()

        return db_tables
    
    @property
    def drop_database(self) -> None:

        connection, _ = self.__connect
        connection.close()

        try:
            os.remove(self.__path)
        
        except Exception as e:
            self.__exception_error(message_error=e)
    
    def create_table(self, tablename: str, columns: list[Column]) -> None:
        try:
            columns_details: list[Column] = [
                Column(
                    name='id',
                    column_type=self.column_types.integer,
                    primary_key=True,
                    auto_increment=True
                ),
                *columns
            ]

            all_columns = ', '.join(column.column_parameters for column in columns_details)
            
            connection, cursor = self.__connect
            cursor.execute(
                f'CREATE TABLE IF NOT EXISTS {tablename} ({all_columns})'
            )

            connection.close()
        
        except Exception as e:
            self.__exception_error(message_error=e)
    
    def insert_data(self, tablename: str, insert_query: list[ColumnData]) -> None:

        columns: str = ', '.join([f'{edit.column}' for edit in insert_query])
        params: list = [edit.value for edit in insert_query]
        key: str = ', '.join('?' for _ in insert_query)

        try:
            connection, cursor = self.__connect

            cursor.execute(
                f'INSERT INTO {tablename} ({columns}) VALUES ({key})', tuple(params)
            )

            connection.commit()
            connection.close()
        
        except Exception as e:
            self.__exception_error(message_error=e)

    def detele_data(self, tablename: str, condition: Filter = None):
        connection, cursor = self.__connect

        if not condition:
            cursor.execute(f'DELETE FROM {tablename}')
        
        else:
            condition_query = condition._Filter__condition.strip()
            condition_params = condition._Filter__params

            cursor.execute(f'DELETE FROM {tablename} {condition_query}', tuple(condition_params))
        
        connection.commit()
        connection.close()
    
    def select_data(self, tablename: str, columns: list[str] = ['*'], condition: Filter = None):
        connection, cursor = self.__connect

        if not condition:
            cursor.execute(f'SELECT {', '.join(columns)} FROM {tablename}')

        else:
            condition_query: str = condition._Filter__condition.strip()
            condition_params: list = condition._Filter__params

            cursor.execute(f'SELECT {', '.join(columns)} FROM {tablename} {condition_query}', tuple(condition_params))

        dados = cursor.fetchall()

        connection.close()

        return dados
    
    def update_data(self, tablename: str, edit_query: list[ColumnData], condition: Filter = None):
        
        connection, cursor = self.__connect
        columns: str = ', '.join([f'{edit.column} = ?' for edit in edit_query])
        params: list = [edit.value for edit in edit_query]

        if not condition:
            cursor.execute(f"UPDATE {tablename} SET {columns}", tuple(params))
        
        else:
            condition_query: str = condition._Filter__condition.strip()
            params.extend(condition._Filter__params)

            cursor.execute(f"UPDATE {tablename} SET {columns} {condition_query}", tuple(params))
        
        connection.commit()
        connection.close()
    
    def add_column(self, tablename: str, column: Column):
        connection, cursor = self.__connect

        column_details = column.column_parameters
        cursor.execute(f'ALTER TABLE {tablename} ADD COLUMN {column_details}')

        connection.commit()
        connection.close()
    
    def drop_column(self, tablename: str, column_name: str):

        connection, cursor = self.__connect
        cursor.execute(f'ALTER TABLE {tablename} DROP COLUMN {column_name}')

        connection.commit()
        connection.close()
    
    def drop_table(self, tablename: str):

        connection, cursor = self.__connect

        cursor.execute(f'DROP TABLE IF EXISTS {tablename}')

        connection.commit()
        connection.close()
    
    def encrypt_value(self, value) -> str:
        return EncryptValue(value).value_hashed

    def __exception_error(self, message_error: str):
        print(f'Error: {message_error}')
        exit()