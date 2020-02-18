# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from .postgres_bulk_hook import PostgresHookBulk
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults


class PostgresOperatorBulk(BaseOperator):
    """
    Executes sql code in a specific Postgres database

    :param sql: the sql code to be executed. (templated)
    :type sql: Can receive a str representing a sql statement,
        a list of str (sql statements), or reference to a template file.
        Template reference are recognized by str ending in '.sql'
    :param postgres_conn_id: reference to a specific postgres database
    :type postgres_conn_id: str
    :param autocommit: if True, each command is automatically committed.
        (default value: False)
    :type autocommit: bool
    :param parameters: (optional) the parameters to render the SQL query with.
    :type parameters: mapping or iterable
    :param database: name of database which overwrite defined one in connection
    :type database: str
    """

    @apply_defaults
    def __init__(
            self, 
            source_task_data,
            table_name,
            postgres_conn_id='postgres_default', 
            autocommit=False,
            parameters=None,
            database=None,
            *args, **kwargs):
        super(PostgresOperatorBulk, self).__init__(*args, **kwargs)
        self.source_task_data = source_task_data
        self.table_name = table_name
        self.postgres_conn_id = postgres_conn_id
        self.autocommit = autocommit
        self.parameters = parameters
        self.database = database

    def execute(self, context):
        for k, v in context.items():
            print(k, v)
        df = context['task_instance'].xcom_pull(self.source_task_data)
        self.log.info('Executing: %s', self.table_name)
        self.hook = PostgresHookBulk(postgres_conn_id=self.postgres_conn_id,
                                    schema=self.database)

        self.hook.bulk_copy_df(df, self.table_name)
        for output in self.hook.conn.notices:
            self.log.info(output)
