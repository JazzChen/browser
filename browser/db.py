# -*- coding: utf-8 -*-

class Table(object):
    def __init__(self, conn, cache_size=100, ifcreate_table=True):
        self.conn = conn
        self.cache_size = cache_size
        self.data_cache = []

        cur = self.conn.cursor()
        if ifcreate_table:
            cur.execute(self.create_stmt)
        conn.commit()

    def insert(self, *args):
        self.data_cache.append(args)
        if len(self.data_cache) > self.cache_size:
            self.flush()

    def flush(self):
        cur = self.conn.cursor()
        cur.executemany(self.insert_stmt, self.data_cache)
        self.conn.commit()
        self.data_cache = []


class BrowserTable(Table):
    def __init__(self, conn, spider_name, cache_size=100, ifcreate_table=True):
        self.table_name = 'browser_history_content'
        self.create_stmt = '''CREATE TABLE IF NOT EXISTS {tablename}
                              (
                               `id` INT(11) NOT NULL AUTO_INCREMENT,
                               `account` VARCHAR(250), 
                               `deviceid` VARCHAR(250),
                               `title` VARCHAR(250), 
                               `idate` INT(20),
                               `importday` VARCHAR(15),
                               `html` TEXT,
                               `text` TEXT,
                                PRIMARY KEY(id)
                              );
                           '''.format(tablename = self.table_name)

        self.insert_stmt = '''INSERT INTO {tablename} 
                              VALUES 
                              (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                           '''.format(tablename = self.table_name)
        Table.__init__(self, conn, cache_size=cache_size, ifcreate_table=ifcreate_table)
