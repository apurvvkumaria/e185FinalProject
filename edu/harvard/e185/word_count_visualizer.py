import pycassa
from pycassa.pool import ConnectionPool
from pycassa.system_manager import *


class WordCountVisualizer(object):
    INPUT_FILE, OUTPUT_FILE = ('wordcount', 'wordcount.jsonp')
    KEY_SPACE, COL_FAMILY, COL1, COL2 = ('Harvard', 'WordCount', 'word', 'count')
    EXCLUDED_WORDS = ['the', 'nbsp', 'to', 'est', 'in', 'and', 'of', 'nd', 'a', 'by', 'for', 'or', 'with', 'km', 'm']

    def bootstrap(self):
        sys = SystemManager()
        sys.create_keyspace(self.KEY_SPACE, SIMPLE_STRATEGY, {'replication_factor': '1'})
        sys.create_column_family(self.KEY_SPACE, self.COL_FAMILY)
        sys.close()

    def transform_data(self):
        col_family = self._column_family()
        columns = list(col_family.xget('row_key'))
        self._write_data(columns)

    def _write_data(self, columns):
        f = self._output_file()
        f.write('wordcountdata=[')
        for column in columns:
            if not self._excluded_word(column[0]):
                f.write('{"word":"%s", "count":%s},' % (column[0], column[1]))
        f.write(']')
        f.close()

    def load_data(self):
        col_family = self._column_family()
        self._read_data(col_family)

    def _excluded_word(self, word):
        return word in self.EXCLUDED_WORDS

    def _write(self, val1, val2, f):
        f.write('{"word":%s", "count":"%s"},\n' % (val1, val2))

    def _read_data(self, col_family):
        f = self._input_file()
        for line in f:
            data = line.split('\t')
            if self._valid_data(data):
                self._insert_data(col_family, data[0], data[1].strip('\n'))
        f.close()

    def _valid_data(self, result):
        return result is not None and len(result) is 2

    def _input_file(self):
        return open(self.INPUT_FILE, 'r')

    def _output_file(self):
        return open(self.OUTPUT_FILE, 'w')

    def _column_family(self):
        pool = ConnectionPool(self.KEY_SPACE)
        return pycassa.ColumnFamily(pool, self.COL_FAMILY)

    def _insert_data(self, col_family, text, count):
        col_family.insert('row_key', {text: count})


def main():
    reader = WordCountVisualizer()
    reader.bootstrap()
    reader.load_data()
    reader.transform_data()

if __name__ == "__main__":
    main()