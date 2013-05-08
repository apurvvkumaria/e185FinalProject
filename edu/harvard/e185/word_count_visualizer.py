import pycassa
from pycassa.pool import ConnectionPool
from pycassa.system_manager import *


class WordCountVisualizer(object):
    COUNTER, INPUT_FILE_NAME = (0, 'wordcount')
    KEY_SPACE, COL_FAMILY, COL1, COL2 = ('Harvard', 'WordCount', 'word', 'count')

    def bootstrap(self):
        sys = SystemManager()
        sys.create_keyspace(self.KEY_SPACE, SIMPLE_STRATEGY, {'replication_factor': '1'})
        sys.create_column_family(self.KEY_SPACE, self.COL_FAMILY)
        sys.close()

    def read_data(self):
        col_family = self._column_family()
        num_rows = len(list(col_family.get_range()))
        for count in range(0, num_rows):
            print col_family.get('row' + str(count), columns=[self.COL1, self.COL2])

    def load_data(self):
        f = self._read_file()
        col_family = self._column_family()

        for line in f:
            data = line.split('\t')
            if self._valid_data(data):
                self._insert_data(col_family, data[0], data[1].strip('\n'))

    def _valid_data(self, result):
        return result is not None and len(result) is 2

    def _read_file(self):
        return open(self.INPUT_FILE_NAME, 'r')

    def _column_family(self):
        pool = ConnectionPool(self.KEY_SPACE)
        return pycassa.ColumnFamily(pool, self.COL_FAMILY)

    def _insert_data(self, col_family, text, count):
        col_family.insert('row' + str(self.COUNTER), {self.COL1: text, self.COL2: count})
        self.COUNTER += 1


def main():
    reader = WordCountVisualizer()
    reader.bootstrap()
    reader.load_data()
    reader.read_data()

if __name__ == "__main__":
    main()