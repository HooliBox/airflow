from airflow.hooks.postgres_hook import PostgresHook
from .stringio import StringIteratorIO
from pandas import isnull
from contextlib import closing


class PostgresHookBulk(PostgresHook):
    '''designed specificed to work with copy dataframe to postgres database'''

    def __init__(self, *args, **kwargs):
        super(PostgresHookBulk, self).__init__(*args, **kwargs)
        self.schema = kwargs.pop("schema", None)

    def bulk_copy_df(self, dataframe, table_name):
        with closing(self.get_conn()) as conn:
            with closing(conn.cursor()) as cur:
                string_iterator = StringIteratorIO(
                    ('|'.join((str(c) for c in map(self.convert_none, row[1:]))) + '\n' for row in dataframe.itertuples())    
                )
                cur.copy_from(string_iterator, table_name, sep='|', size=78480, columns=df.columns)
                conn.commit()

    def convert_none(self, value):
        if isnull(value):
            return r'\N'
        return value