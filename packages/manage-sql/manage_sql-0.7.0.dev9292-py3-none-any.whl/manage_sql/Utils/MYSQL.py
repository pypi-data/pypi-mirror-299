import mysql.connector as mysql
try:
    from Utils.utils_mysql import (
        Types,
        Table,
        Column,
        ColumnData,
        Filter,
        EncryptValue
    )

except:
    from utils_mysql import (
        Types,
        Table,
        Column,
        ColumnData,
        Filter,
        EncryptValue
    )

class MYSQL:
    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        database: str = None,
        port: int = 3306
    ):
        self.__host = host
        self.__username = username
        self.__password = password
        self.__database = database
        self.__port = port
        self.column_types = Types()
        self.column = Column
        self.filter_by = Filter
        self.delete_by = Filter
        self.column_data = ColumnData
        self.CURRENT_TIMESTAMP = 'CURRENT_TIMESTAMP'
    
    @property
    def __connect(self):

        def connect_without_database():
            connection = mysql.connect(
                host = self.__host,
                port = self.__port,
                user = self.__username,
                password = self.__password
            )

            return connection
        
        def connect_with_database():
            connection = mysql.connect(
                host = self.__host,
                port = self.__port,
                database = self.__database,
                user = self.__username,
                password = self.__password
            )

            return connection
            
        if not self.__database:
            connection = connect_without_database()
        
        else:
            try:
                connection = connect_with_database()
            
            except:
                try:
                    connection = connect_without_database()
                    connection.cursor().execute(f'CREATE DATABASE IF NOT EXISTS {self.__database}')

                    connection = connect_with_database()
                
                except Exception as e:
                    connection.close()
                    self.__exception_error(message_error=e)

        cursor = connection.cursor()

        return connection, cursor
    
    @property
    def tables(self) -> list[Table]:
        
        connection, cursor = self.__connect
            
        cursor.execute(
            'SHOW TABLES'
        )

        tables = cursor.fetchall()

        db_tables: list[Table] = []

        for table in tables:
            if table[0] != 'sqlite_sequence':
                table_info = Table(name=table[0])
                cursor.execute(
                    f'SHOW COLUMNS FROM {table[0]}'
                )

                columns = cursor.fetchall()

                for column in columns:
                    table_info.columns.append(
                        Column(
                            name = column[0],
                            column_type = column[1],
                            primary_key = column[3],
                            auto_increment = True if "auto_increment" in column[5] else False,
                            unique = True if "unique" in column[5] else False,
                            not_null = True if column[2]=='YES' else False,
                            default_value = True if "DEFAULT_GENERATED" in column[5] else False,
                            unsigned = True if "unsigned" in column[5] else False,
                            on_update = column[5].split(' ')[column[5].split(' ').index('update') + 1] if "on update" in column[5] else None
                        )
                    )
                
                db_tables.append(table_info)
        
        connection.close()

        return db_tables
    
    @property
    def drop_database(self) -> None:
        connection, cursor = self.__connect

        try:
            cursor.execute(f'DROP DATABASE {self.__database}')
        
        finally:
            connection.close()
    
    def create_table(self, tablename: str, columns: list[Column]) -> None:
        try:
            columns_details: list[Column] = [
                Column(
                    name='id',
                    column_type=self.column_types.Integer.integer,
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
        key: str = ', '.join('%s' for _ in insert_query)

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
        columns: str = ', '.join([f'{edit.column} = %s' for edit in edit_query])
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

        try:
            connection, cursor = self.__connect
            column_details = column.column_parameters
            cursor.execute(f'ALTER TABLE {tablename} ADD COLUMN {column_details}')

            connection.commit()
        
        except:
            pass
        
        finally:
            connection.close()
    
    def drop_column(self, tablename: str, column_name: str):

        try:
            connection, cursor = self.__connect
            cursor.execute(f'ALTER TABLE {tablename} DROP COLUMN {column_name}')

            connection.commit()
        
        except:
            pass
        
        finally:
            connection.close()
    
    def drop_table(self, tablename: str):

        connection, cursor = self.__connect

        cursor.execute(f'DROP TABLE IF EXISTS {tablename}')

        connection.commit()
        connection.close()
    
    def encrypt_value(self, value) -> str:
        return EncryptValue(value).value_hashed

    def execute_query(self, query: str):

        try:
            connection, cursor = self.__connect

            cursor.execute(query)

            return cursor.fetchall()
        
        finally:
            connection.close()
    
    def __exception_error(self, message_error: str):
        print(f'Error: {message_error}')
        exit()