import hashlib as sh
import json

class EncryptValue:
    def __init__(
        self,
        value
    ):
        hash = sh.sha512()
        hash.update(value.encode('UTF-8'))
        self.value_hashed = hash.hexdigest()

class Types:
    class __Integer:
        @property
        def tinyint(self) -> str:
            return 'TINYINT'
        
        @property
        def smallint(self) -> str:
            return 'SMALLINT'
        
        @property
        def mediumint(self) -> str:
            return 'MEDIUMINT'
        
        @property
        def integer(self) -> str:
            return 'INTEGER'
        
        @property
        def bigint(self) -> str:
            return 'BIGINT'
    
    class Decimal:
        def __init__(
            self,
            max_digit: int,
            float_digit: int
        ):
            self.__max_digit = max_digit
            self.__float_digit = float_digit
        
        @property
        def decimal(self) -> str:
            return f'DECIMAL({self.__max_digit}, {self.__float_digit})'
        
        @property
        def float(self) -> str:
            return f'DECIMAL({self.__max_digit}, {self.__float_digit})'
        
        @property
        def double(self) -> str:
            return f'DECIMAL({self.__max_digit}, {self.__float_digit})'
    
    class __Text:
        @property
        def tinytext(self) -> str:
            return 'TINYTEXT'
        
        @property
        def text(self) -> str:
            return 'TEXT'
        
        @property
        def mediumtext(self) -> str:
            return 'MEDIUMTEXT'
        
        @property
        def longtext(self) -> str:
            return 'LONGTEXT'
    
    class Char:
        def __init__(
            self,
            length: int
        ):
            self.__length = length
        
        @property
        def char(self) -> str:
            return f'CHAR({self.__length})'
        
        @property
        def varchar(self) -> str:
            return f'VARCHAR({self.__length})'
    
    class Binary:
        def __init__(
            self,
            length: int
        ):
            self.__length = length
        
        @property
        def binary(self) -> str:
            return f'BINARY({self.__length})'
        
        @property
        def varbinary(self) -> str:
            return f'VARBINARY({self.__length})'
    
    class __Blob:
        @property
        def tinyblob(self) -> str:
            return 'TINYBLOB'
        
        @property
        def blob(self) -> str:
            return 'BLOB'
        
        @property
        def mediumblob(self) -> str:
            return 'MEDIUMBLOB'
        
        @property
        def longblob(self) -> str:
            return 'LONGBLOB'
    
    class __DateTime:
        @property
        def datetime(self) -> str:
            return 'DATETIME'
        
        @property
        def date(self) -> str:
            return 'DATE'
        
        @property
        def hour(self) -> str:
            return 'HOUR'
        
        @property
        def timestamp(self) -> str:
            return 'TIMESTAMP'
        
        @property
        def year(self) -> str:
            return 'YEAR'
    
    def Enum(self, values: tuple[str]) -> str:
        return f'ENUM({', '.join(values)})'
    
    def Set(self, values: tuple[str]) -> str:
        return f'SET({', '.join(values)})'
    
    Integer = __Integer()
    Text = __Text()
    DateTime = __DateTime()
    Blob = __Blob()

class Column:
    def __init__(
        self,
        name: str,
        column_type: Types,
        primary_key: bool = False,
        auto_increment: bool = False,
        unique: bool = False,
        not_null: bool = False,
        default_value = None,
        unsigned: bool = False,
        on_update: str = None
    ):
        self.name = name
        self.type = column_type
        self.column_parameters = f'{name} {column_type}'

        self.__primary_key: bool = primary_key
        self.__auto_increment: bool = auto_increment
        self.__unique: bool = unique
        self.__not_null: bool = not_null
        self.__default_value = default_value
        self.__unsigned: bool = unsigned
        self.__on_update: str = on_update

        
        if primary_key == True:
            self.column_parameters += f' PRIMARY KEY'
        
        if auto_increment == True:
            self.column_parameters += f' AUTO_INCREMENT'
        
        if unique == True:
            self.column_parameters += f' UNIQUE'
        
        if not_null == True:
            self.column_parameters += f' NOT NULL'
        
        if unsigned == True:
            self.column_parameters += f' UNSIGNED'
        
        if default_value != None:
            self.column_parameters += f' DEFAULT {default_value}'
        
        if on_update != None:
            self.column_parameters += f' ON UPDATE {on_update}'
    
    def __to_dict(self):
        """Converte a coluna para um dicionário."""
        return {
            "name": self.name,
            "type": self.type,
            "primary_key":  self.__primary_key,
            "auto_increment": self.__auto_increment,
            "unique":  self.__unique,
            "not_null":  self.__not_null,
            "default_value": self.__default_value,
            "unsigned":  self.__unsigned,
            "on_update": self.__on_update
        }
    
    def to_json(self):
        return json.dumps(self.__to_dict(), indent=4)

class Table:
    def __init__(
        self,
        name: str
    ):
        self.columns: list[Column] = []
        self.name = name
    
    def __to_dict(self):
        """Converte a tabela e suas colunas para um dicionário."""
        return {
            'table_name': self.name,
            'columns': [column._Column__to_dict() for column in self.columns]
        }

    def to_json(self):
        return json.dumps(self.__to_dict(), indent=4)

class Filter:
    def __init__(
        self,
        column: str
    ):
        self.column_name = column
        self.__condition: str = f"WHERE {column} "
        self.__params: list = []
    
    def filterby(self, column):
        self.__condition += f'{column} '
        return self

    @property
    def OR(self):
        self.__condition += "OR "
        return self
    
    @property
    def AND(self):
        self.__condition += "AND "
        return self
    
    def EQUAL(self, value):
        self.__add_filter(condition='=', value=value)
        return self
    
    def GATHER_THAN(self, value):
        self.__add_filter(condition='>', value=value)
        return self
    
    def GATHER_OR_EQUAL(self, value):
        self.__add_filter(condition='>=', value=value)
        return self
    
    def LESS_THAN(self, value):
        self.__add_filter(condition='<', value=value)
        return self
    
    def LESS_OR_EQUAL(self, value):
        self.__add_filter(condition='<=', value=value)
        return self
    
    def CONTAIN(self, value):
        self.__add_filter(condition='LIKE', value=f'%{value}%')
        return self
    
    def __add_filter(self, condition: str, value):
        self.__params.append(value)
        self.__condition += f'{condition} %s '

class ColumnData:
    def __init__(
        self,
        column,
        value
    ):
        self.column = column
        self.value = value