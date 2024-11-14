import sqlite3


class SqliteTool:
    def __init__(self, db_name='example.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        """
        创建表
        :param table_name: 表名
        :param columns: 列定义，例如 'id INTEGER PRIMARY KEY, name TEXT, age INTEGER'
        """
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})')
        self.conn.commit()
    
    def delete_table(self, table_name):
        """
        删除表
        :param table_name: 表名
        """
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.conn.commit()

    def insert(self, table_name, data):
        """
        插入数据
        :param table_name: 表名
        :param data: 数据，例如 {'name': 'John', 'age': 25}
        """
        columns = ', '.join(data.keys())
        values = ', '.join(['?'] * len(data))
        placeholders = tuple(data.values())
        self.cursor.execute(
            f"INSERT INTO {table_name} ({columns}) VALUES ({values})", placeholders)
        self.conn.commit()

    def update(self, table_name, data, condition):
        """
        更新数据
        :param table_name: 表名
        :param data: 更新数据，例如 {'name': 'John', 'age': 26}
        :param condition: 更新条件，例如 'id = 1'
        """
        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        placeholders = tuple(data.values())
        self.cursor.execute(
            f"UPDATE {table_name} SET {set_clause} WHERE {condition}", placeholders)
        self.conn.commit()

    def delete(self, table_name, condition):
        """
        删除数据
        :param table_name: 表名
        :param condition: 删除条件，例如 'id = 1'
        """
        self.cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
        self.conn.commit()

    def select(self, table_name, columns='*', condition=None):
        """
        查询数据
        :param table_name: 表名
        :param columns: 查询的列，例如 '*' 或 'id, name'
        :param condition: 查询条件，例如 'id = 1'
        :return: 查询结果
        """
        query = f"SELECT {columns} FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        """
        关闭连接
        """
        self.conn.close()


# 使用示例
if __name__ == "__main__":
    tool = SqliteTool('example.db')
    tool.create_table(
        'users', 'id INTEGER PRIMARY KEY, name TEXT, age INTEGER')
    tool.insert('users', {'name': 'John', 'age': 25})
    print(tool.select('users'))
    tool.update('users', {'age': 26}, 'name = "John"')
    print(tool.select('users'))
    tool.delete('users', 'name = "John"')
    print(tool.select('users'))
    tool.close()
