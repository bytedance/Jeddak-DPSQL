import logging
import re
import time
from metadata.converter.clickhouse import ClickhouseTypeConverter
from metadata.converter.hive import HiveTypeConverter
from metadata.storage.metadata_status import MetaStatus
from datetime import datetime
from exception.enum.meradata_errors_enum import MetaDataErrors
from exception.errors import MetaDataError
from cachetools import cached, TTLCache
import cachetools
import CacheToolsUtils as ctu
from metadata.storage.mysql_client import mysql_client
from utils.redis_client import redis_client

rclient = redis_client
ct_base_match_table = cachetools.TTLCache(maxsize=64, ttl=60 * 60 * 24)
ct_base_match_key_meta = cachetools.TTLCache(maxsize=512, ttl=60 * 60 * 24)
redis_cache = ctu.RedisCache(rclient, ttl=60 * 60 * 24)
two_level_cache_match_table = ctu.TwoLevelCache(ct_base_match_table, redis_cache)
two_level_cache_match_key_meta = ctu.TwoLevelCache(ct_base_match_key_meta, redis_cache)
scache_match_table = ctu.StatsCache(two_level_cache_match_table)
scache_match_key_meta = ctu.StatsCache(two_level_cache_match_key_meta)


def store_meta(prefix, dbname, table_name, metadata, db_type=None):
    """
        Store a complete metadata into mysql
    """
    logging.info("dpaccess-internal-store_meta: prefix=%s, dbname=%s, table_name=%s, db_type=%s", prefix, dbname,
                 table_name, db_type)

    conn = mysql_client.get_connection()
    cur = conn.cursor()
    try:
        if if_exist_meta_without_cache(prefix, dbname, table_name):
            raise MetaDataError(MetaDataErrors.GET_MAPKEY_ERROR.value, "Add failed, the metadata already exists!")
        else:
            # Query whether (prefix, dbname) already exists in the table metadata_db
            db_id = get_db_id(prefix, dbname)
            if not db_id:
                if not db_type:
                    db_type = metadata.get('engine', None)
                if not db_type:
                    raise MetaDataError(MetaDataErrors.DB_TYPE_NONE.value, "Add failed, db_type can not be none!")
                # Insert (prefix, dbname) into table metadata_db
                insert_db_sql = """insert into metadata_db(prefix, db_name, db_type, create_time, status)
                values (%s, %s, %s, %s, %s)
                """
                insert_db_num = cur.execute(insert_db_sql, (prefix, dbname, db_type, time.time(), 1))
                if insert_db_num == 1:
                    logging.info("dpaccess-internal-store_meta: metadata_db 添加成功")
                    query_db_sql = """select id from metadata_db where prefix = %s and db_name = %s and status = 1"""
                    cur.execute(query_db_sql, (prefix, dbname))
                    res = cur.fetchone()
                    if res:
                        db_id = res[0]
                    else:
                        logging.error("dpaccess-internal-store_meta: query_db_sql 查询失败")
                        raise MetaDataError("1026", "query_db_sql execute failed!")
                else:
                    logging.error("dpaccess-internal-store_meta: metadata_db 添加失败")
                    raise MetaDataError("1026", "insert_db_sql execute failed!")

            # Insert (table_name, db_id) into table metadata_table
            insert_table_sql = """insert into metadata_table(table_name, db_id, create_time, status)
            values (%s, %s, %s, %s)
            """
            insert_table_num = cur.execute(insert_table_sql, (table_name, db_id, time.time(), 1))
            if insert_table_num == 1:
                logging.info("dpaccess-internal-store_meta: metadata_table 添加成功")
                query_table_sql = """select id from metadata_table where table_name = %s and db_id = %s and status = 1"""
                cur.execute(query_table_sql, (table_name, db_id))
                res = cur.fetchone()
                if res:
                    table_id = res[0]
                else:
                    logging.error("dpaccess-internal-store_meta: query_table_sql 查询失败")
                    raise MetaDataError("1026", "query_table_sql execute failed!")
            else:
                logging.error("dpaccess-internal-store_meta: metadata_table 添加失败")
                raise MetaDataError("1026", "insert_table_sql execute failed!")

            # Traversing Columns
            columns = metadata['tables'][0]['columns']
            for k, v in columns.items():
                column_name = k
                column_type = v['type']
                lower = v.get('lower', None)
                upper = v.get('upper', None)
                max_fre = v.get('max_fre', None)
                # Insert (column_name, table_id) into table metadata_column
                insert_column_sql = """insert into metadata_column(column_name, type, lower, upper, max_fre, table_id,
                create_time, status)
                values (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                insert_column_num = cur.execute(insert_column_sql, (
                    column_name, column_type, lower, upper, max_fre, table_id, time.time(), 1))
                if insert_column_num == 1:
                    logging.info("dpaccess-internal-store_meta: metadata_column 添加成功")
                    query_column_sql = """select id from metadata_column where column_name = %s and type = %s
                    and table_id = %s and status = 1
                    """
                    cur.execute(query_column_sql, (k, column_type, table_id))
                    res = cur.fetchone()
                    if res:
                        column_id = res[0]
                    else:
                        logging.error("dpaccess-internal-store_meta: query_column_sql 查询失败")
                        raise MetaDataError("1026", "query_column_sql execute failed!")
                else:
                    logging.error("dpaccess-internal-store_meta: metadata_column 添加失败")
                    raise MetaDataError("1026", "insert_column_sql execute failed!")

                # If it is a map type, determine whether there is a key_metas
                if column_type.startswith('Map'):
                    key_type = column_type[4: len(column_type) - 1].split(',')[0]
                    value_type = column_type[4: len(column_type) - 1].split(',')[1].lstrip()
                    key_metas = v.get('key_metas', None)
                    # If there is key_metas, traverse each event information + column_id of key_metas, and insert it into the table metadata_key_metas
                    if key_metas:
                        for key_meta in key_metas:
                            event_name = key_meta.get('event', None)
                            if event_name:
                                event_name = event_name.replace("\'", "\\\'")
                            insert_key_meta_sql = """insert into metadata_column_map_key_metas(key_type, value_type,
                            event_name, event_lower, event_upper, name, column_id, create_time, status)
                            values
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """
                            insert_key_meta_num = cur.execute(insert_key_meta_sql, (key_type, value_type, event_name,
                                                                                    key_meta.get('lower', None),
                                                                                    key_meta.get('upper', None),
                                                                                    key_meta['name'], column_id,
                                                                                    time.time(), 1))
                            if insert_key_meta_num == 1:
                                logging.info("dpaccess-internal-store_meta: metadata_column_map_key_metas 添加成功")
                            else:
                                logging.error("dpaccess-internal-store_meta: metadata_column_map_key_metas 添加失败")
                                raise MetaDataError("1026", "insert_key_meta_sql execute failed!")
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        logging.exception("dpaccess-internal-store_meta Exception: \n" + str(e))
        raise MetaDataError("1034",
                            "Add meta failed, Exception: {}\n prefix={}, db_name={}, table_name={}".format(str(e),
                                                                                                           prefix,
                                                                                                           dbname,
                                                                                                           table_name))
    finally:
        cur.close()
        conn.close()


def add_db_table_name(prefix, db_name, table_name, db_type):
    logging.info("dpaccess-internal-add_db_table_name: prefix=%s, db_name=%s, table_name=%s, db_type=%s", prefix,
                 db_name, table_name, db_type)

    conn = mysql_client.get_connection()
    cur = conn.cursor()

    table_info = get_table_info(prefix, db_name, table_name)
    if table_info:
        meta_status = table_info.get("status")
        if meta_status == MetaStatus.FINISHED.value:
            raise MetaDataError("1017", "Add failed-add_db_table_name_to_rds, the metadata already exists!")
        elif meta_status == MetaStatus.GENERATING.value:
            table_info = get_table_info(prefix, db_name, table_name)
            last_update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(table_info.get("last_update_time")))
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            format_last_update_time = datetime.strptime(last_update_time, "%Y-%m-%d %H:%M:%S")
            format_now = datetime.strptime(now, "%Y-%m-%d %H:%M:%S")
            sub_res = (format_now - format_last_update_time).total_seconds() / 60
            if sub_res > 30:
                return
            else:
                raise MetaDataError("1032", "Add failed-add_db_table_name_to_rds, the metadata is generating!")
        elif meta_status == MetaStatus.FAILED.value:
            logging.info("dpaccess-internal-add_db_table_name_to_rds: transform status from -1 to 2")
            update_meta_status(prefix, db_name, table_name, MetaStatus.FAILED.value, MetaStatus.GENERATING.value)
            return
        elif meta_status == MetaStatus.DELETED.value:
            logging.info("dpaccess-internal-add_db_table_name_to_rds: transform status from 0 to 2")
            update_meta_status(prefix, db_name, table_name, MetaStatus.DELETED.value, MetaStatus.GENERATING.value)
            return
    else:
        try:
            db_id = get_db_id(prefix, db_name)
            if not db_id:
                insert_db_sql = """insert into metadata_db(prefix, db_name, db_type, create_time, status)
                                values (%s, %s, %s, %s, %s)
                                """
                insert_db_num = cur.execute(insert_db_sql, (prefix, db_name, db_type, time.time(), 1))
                if insert_db_num == 1:
                    query_db_sql = """select id from metadata_db where prefix = %s and db_name = %s and status = 1"""
                    cur.execute(query_db_sql, (prefix, db_name))
                    db_res = cur.fetchone()
                    if db_res:
                        db_id = db_res[0]
                    else:
                        logging.error("dpaccess-internal-add_db_table_name_to_rds: insert_db_sql query failed!")
                        raise MetaDataError("1026", "insert_db_sql execute failed!")
                else:
                    logging.error("dpaccess-internal-add_db_table_name_to_rds: metadata_db add failed!")
                    raise MetaDataError("1026", "insert_db_sql execute failed!")

            insert_table_sql = """insert into metadata_table(table_name, last_update_time, db_id, create_time, status)
                            values (%s, %s, %s, %s, %s)
                            """
            insert_table_num = cur.execute(insert_table_sql, (
                table_name, time.time(), db_id, time.time(), MetaStatus.GENERATING.value))
            if insert_table_num != 1:
                logging.error("dpaccess-internal-add_db_table_name_to_rds: metadata_table add failed!")
                raise MetaDataError("1026", "insert_table_sql execute failed!")
            conn.commit()
        except Exception as e:
            logging.exception("dpaccess-internal-add_db_table_name_to_rds Exception: \n" + str(e))
            raise MetaDataError("1026",
                                "add_db_table_name_to_rds failed, Exception: {}\n, prefix={}, db_name={}, table_name={}".format(
                                    str(e), prefix, db_name, table_name))
        finally:
            cur.close()
            conn.close()


def add_columns_and_key_metas(prefix, db_name, table_name, metadata):
    logging.info("dpaccess-internal-add_columns_and_keymets: prefix=%s, db_name=%s, table_name=%s", prefix, db_name,
                 table_name)

    conn = mysql_client.get_connection()
    cur = conn.cursor()

    query_table_id_sql = """select metadata_table.id
                            from metadata_db
                            join metadata_table
                            where metadata_db.prefix = %s
                            and metadata_db.db_name = %s
                            and metadata_table.table_name = %s
                            and metadata_db.status = %s
                            and metadata_table.status = %s
                            and metadata_db.id = metadata_table.db_id
                            """
    cur.execute(query_table_id_sql,
                (prefix, db_name, table_name, MetaStatus.FINISHED.value, MetaStatus.GENERATING.value))
    res = cur.fetchone()
    if res:
        table_id = res[0]
    else:
        logging.error("dpaccess-internal-add_columns_and_key_metas: query_table_id_sql query failed!")
        raise MetaDataError("1026", "query_table_id_sql execute failed!")

    try:
        columns = metadata['tables'][0]['columns']
        for k, v in columns.items():
            column_name = k
            column_type = v['type']
            lower = v.get('lower', None)
            upper = v.get('upper', None)
            max_fre = v.get('max_fre', None)
            # insert table metadata_column
            insert_column_sql = """insert into metadata_column(column_name, type, lower, upper, max_fre, table_id,
                        create_time, status)
                        values (%s, %s, %s, %s, %s, %s, %s, %s)
                        """
            insert_column_num = cur.execute(insert_column_sql, (
                column_name, column_type, lower, upper, max_fre, table_id, time.time(), 1))
            if insert_column_num == 1:
                logging.info("dpaccess-internal-add_columns_and_key_metas: metadata_column add successfully")
                query_column_sql = """select id from metadata_column where column_name = %s and type = %s
                            and table_id = %s and status = %s
                            """
                cur.execute(query_column_sql, (k, column_type, table_id, MetaStatus.FINISHED.value))
                res = cur.fetchone()
                if res:
                    column_id = res[0]
                else:
                    logging.error("dpaccess-internal-add_columns_and_key_metas: query_column_sql query failed!")
                    raise MetaDataError("1026", "query_column_sql execute failed!")
            else:
                logging.error("dpaccess-internal-add_columns_and_key_metas: insert_column_sql add failed!")
                raise MetaDataError("1026", "insert_column_sql execute failed!")

            if column_type.startswith('Map'):
                key_type = column_type[4: len(column_type) - 1].split(',')[0]
                value_type = column_type[4: len(column_type) - 1].split(',')[1].lstrip()
                key_metas = v.get('key_metas', None)
                if key_metas:
                    for key_meta in key_metas:
                        insert_key_meta_sql = """insert into metadata_column_map_key_metas(key_type, value_type,
                        event_lower, event_upper, name, column_id, create_time, status)
                                    values (%s, %s, %s, %s, %s, %s, %s, %s)
                                    """
                        insert_key_meta_num = cur.execute(insert_key_meta_sql, (key_type, value_type,
                                                                                key_meta.get('lower', None),
                                                                                key_meta.get('upper', None),
                                                                                key_meta['name'], column_id,
                                                                                time.time(), 1))
                        if insert_key_meta_num == 1:
                            logging.info("dpaccess-internal-add_columns_and_key_metas: metadata_column_map_key_metas "
                                         "add successfully")
                        else:
                            logging.error("dpaccess-internal-add_columns_and_key_metas: metadata_column_map_key_metas "
                                          "add failed!")
                            raise MetaDataError("1026", "insert_key_meta_sql execute failed!")

        update_status_sql = """
            update metadata_table
            set status = %s
            where id in
            (
                select id
                from
                (
                    select metadata_table.id
                    from metadata_db
                    join metadata_table
                    on metadata_db.id = metadata_table.db_id
                    where metadata_db.prefix = %s and metadata_db.db_name = %s and metadata_db.status = 1
                    and metadata_table.table_name = %s and metadata_table.status = %s
                ) as t
            )
            """
        cur.execute(update_status_sql,
                    (MetaStatus.FINISHED.value, prefix, db_name, table_name, MetaStatus.GENERATING.value))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        logging.exception("dpaccess-internal-add_columns_and_key_metas Exception: \n" + str(e))
        raise MetaDataError("1034", "Add meta failed-add_columns_and_key_metas, Exception: {}\n prefix={}, db_name={}, "
                                    "table_name={}".format(str(e), prefix, db_name, table_name))
    finally:
        cur.close()
        conn.close()


def delete_meta(prefix, db_name, table_name):
    """
        Delete a complete metadata
    """
    logging.info("dpaccess-internal-delete_meta: prefix=%s, db_name=%s, table_name=%s", prefix, db_name, table_name)

    if not if_exist_meta(prefix, db_name, table_name):
        raise MetaDataError("1023", "Delete failed，the metadata doesn't exist!")
    else:
        conn = mysql_client.get_connection()
        cur = conn.cursor()
        try:
            # remove key-metas
            delete_key_metas_sql = """
            update metadata_column_map_key_metas
            set status = 0
            where id in
            (
                select id
                from
                (
                    select metadata_column_map_key_metas.id
                    from
                    (   select metadata_column.id
                        from
                        (   select metadata_table.id
                            from metadata_db
                            join metadata_table
                            on metadata_db.id = metadata_table.db_id
                            where metadata_db.prefix = %s and metadata_db.db_name = %s and metadata_db.status = 1
                            and metadata_table.table_name = %s and metadata_table.status = 1
                        ) as d_t
                        join
                        metadata_column
                        on d_t.id = metadata_column.table_id
                        where metadata_column.type like %s and metadata_column.status = 1
                    ) as d_t_c
                    join  metadata_column_map_key_metas
                    on d_t_c.id = metadata_column_map_key_metas.column_id
                    where metadata_column_map_key_metas.status = 1
                ) as t
            )
            """
            cur.execute(delete_key_metas_sql, (prefix, db_name, table_name, 'Map%'))
            logging.info("dpaccess-internal-delete_meta: key_metas deleted successfully")

            # delete all columns
            delete_columns_sql = """
            update metadata_column
            set status = 0
            where id in
            (
                select id
                from
                (
                    select metadata_column.id
                    from
                    (   select metadata_table.id
                        from metadata_db
                        join metadata_table
                        on metadata_db.id = metadata_table.db_id
                        where metadata_db.prefix = %s and metadata_db.db_name = %s and metadata_db.status = 1
                        and metadata_table.table_name = %s and metadata_table.status = 1
                    ) d_t
                    join
                    metadata_column
                    on d_t.id = metadata_column.table_id
                    where metadata_column.status = 1
                ) as t
            )
            """
            cur.execute(delete_columns_sql, (prefix, db_name, table_name))
            logging.info("dpaccess-internal-delete_meta: columns deleted successfully")

            # delete table name
            delete_table_sql = """
            update metadata_table
            set status = 0
            where id in
            (
                select id
                from
                (
                    select metadata_table.id
                    from metadata_db
                    join metadata_table
                    on metadata_db.id = metadata_table.db_id
                    where metadata_db.prefix = %s and metadata_db.db_name = %s and metadata_db.status = 1
                    and metadata_table.table_name = %s and metadata_table.status = 1
                ) as t
            )
            """
            cur.execute(delete_table_sql, (prefix, db_name, table_name))
            logging.info("dpaccess-internal-delete_meta: table deleted successfully")
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            logging.exception("dpaccess-internal-delete_meta Exception: \n" + str(e))
            raise MetaDataError("1029",
                                "Delete meta failed, Exception: {}\n, prefix={}, db_name={}, table_name={}".format(
                                    str(e), prefix, db_name, table_name))
        finally:
            cur.close()
            conn.close()


def update_meta_status(prefix, db_name, table_name, status, new_status):
    """ Update the metadata generated state

    """
    logging.info(
        "dpaccess-internal-update_meta_status: prefix=%s, db_name=%s, table_name=%s, status=%s, new_status=%s",
        prefix, db_name, table_name, status, new_status)

    conn = mysql_client.get_connection()
    cur = conn.cursor()
    try:
        update_status_sql = """
            update metadata_table
            set status = %s
            where id in
            (
                select id
                from
                (
                    select metadata_table.id
                    from metadata_db
                    join metadata_table
                    on metadata_db.id = metadata_table.db_id
                    where metadata_db.prefix = %s and metadata_db.db_name = %s and metadata_db.status = 1
                    and metadata_table.table_name = %s and metadata_table.status = %s
                ) as t
            )
            """
        cur.execute(update_status_sql, (new_status, prefix, db_name, table_name, status))
        conn.commit()
    except Exception as e:
        logging.exception("dpaccess-internal-update_meta_status Exception: \n" + str(e))
        raise MetaDataError("1024", "update_meta_status failed, Exception: {}\n, prefix={}, db_name={}, "
                                    "table_name={}, status={}, new_status={}".format(str(e), prefix, db_name,
                                                                                     table_name, status, new_status))
    finally:
        cur.close()
        conn.close()


def check_map_type(db_col_type, type_converter):
    """
        Check whether the value type of db_col_type is int or float
    """
    pattern = re.compile(r"Map\((.*)\)")
    result = pattern.search(db_col_type)
    if result is not None:
        pure_type = result.group(1)
        key_val_db_type = re.split(r"[,\s]+", pure_type)
        key_db_type, val_db_type = key_val_db_type[0], key_val_db_type[-1]
        key_type = type_converter.dbtype_to_type(key_db_type)
        val_type = type_converter.dbtype_to_type(val_db_type)
        if key_type in ["string"] and val_type in ['int', 'float']:
            return True
        else:
            return False
    else:
        raise MetaDataError("1035", "cannot check the map type!")


def get_update_info(prefix, db_name, table_name, new_meta, db_type):
    """
        Gets the difference between the new meta and the old meta
    """
    logging.info("dpaccess-internal-get_update_info: prefix=%s, db_name=%s, table_name=%s", prefix, db_name, table_name)
    old_meta = query_meta(prefix, db_name, table_name)
    # Maintain the add, update, delete list of columns
    add_columns_list = []
    update_columns_list = []
    delete_columns_list = []

    # Maintain the add, update, delete list of key_metas
    add_key_metas_list = []
    update_key_metas_list = []
    delete_key_metas_list = []

    # GetTheConverterConverter
    if db_type == "clickhouse":
        converter = ClickhouseTypeConverter()
    elif db_type == "hive":
        converter = HiveTypeConverter()
    else:
        raise MetaDataError("1004", "type converter of %s engine is not implemented" % (db_type))

    # Compare and see which col_name, key-meta need to be added or modified;
    old_columns = old_meta['tables'][0]['columns']
    new_columns = new_meta['tables'][0]['columns']
    for new_col_name, new_col in new_columns.items():
        new_col_db_type = new_col.get('type')
        new_col_type = converter.dbtype_to_type(new_col_db_type)
        old_col = old_columns.get(new_col_name)
        if not old_col:
            add_columns_list.append(new_col_name)
        else:
            # Whether the comparison type is consistent
            if new_col_db_type != old_col.get('type'):
                update_columns_list.append(new_col_name)
            elif new_col_type in ['int', 'float']:
                # If it is int or float, you need to compare lower, upper, max_fre
                if not (new_col.get('upper') == old_col.get('upper') and new_col.get('lower') == old_col.get('lower')
                        and new_col.get("max_fre") == old_col.get("max_fre")):
                    update_columns_list.append(new_col_name)
            elif new_col_type in ["map"] and check_map_type(new_col_db_type, converter):
                new_key_metas = new_col.get("key_metas")
                old_key_metas = old_col.get("key_metas")
                key_type = new_col_db_type[4: len(new_col_db_type) - 1].split(',')[0]
                value_type = new_col_db_type[4: len(new_col_db_type) - 1].split(',')[1].lstrip()
                # Traversing new_key_metas to collect key_meta information that needs to be added and updated
                for new_key_meta in new_key_metas:
                    tag = 0
                    new_name = new_key_meta.get("name")
                    new_key_meta_lower = new_key_meta.get("lower")
                    new_key_meta_upper = new_key_meta.get("upper")
                    for old_key_meta in old_key_metas:
                        if old_key_meta.get("name") == new_name:
                            # have the name
                            tag = 1
                            if not (old_key_meta.get("lower") == new_key_meta_lower and old_key_meta.get(
                                    "upper") == new_key_meta_upper):
                                # The lower and upper of the name need to be updated
                                update_key_metas_list.append(
                                    [new_col_name, new_name, new_key_meta_lower, new_key_meta_upper, key_type,
                                     value_type])
                                break
                    # The name does not exist in the old key metas
                    if tag == 0:
                        add_key_metas_list.append(
                            [new_col_name, new_name, new_key_meta_lower, new_key_meta_upper, key_type, value_type])

                # Traverse old_key_metas to collect key_meta information that needs to be deleted
                for old_key_meta in old_key_metas:
                    tag = 0
                    old_name = old_key_meta.get("name")
                    for new_key_meta in new_key_metas:
                        if new_key_meta.get("name") == old_name:
                            tag = 1
                            break
                    if tag == 0:
                        delete_key_metas_list.append([new_col_name, old_name])

    # Compare to see which columns need to be deleted
    for old_col_name, old_col in old_columns.items():
        new_col = new_columns.get(old_col_name)
        if not new_col:
            delete_columns_list.append(old_col_name)
    return add_columns_list, update_columns_list, delete_columns_list, add_key_metas_list, update_key_metas_list, delete_key_metas_list


def update_meta(prefix, db_name, table_name, new_meta, db_type):
    logging.info("dpaccess-internal-update_meta: prefix=%s, db_name=%s, table_name=%s, db_type=%s", prefix, db_name,
                 table_name, db_type)
    add_columns_list, update_columns_list, delete_columns_list, add_key_metas_list, update_key_metas_list, delete_key_metas_list = get_update_info(
        prefix, db_name, table_name, new_meta, db_type)
    table_info = get_table_info(prefix, db_name, table_name)
    table_id = table_info.get("table_id")
    conn = mysql_client.get_connection()
    cur = conn.cursor()
    try:
        # add columns
        if add_columns_list and len(add_columns_list) > 0:
            for column_name in add_columns_list:
                col_info = new_meta['tables'][0]['columns'].get(column_name)
                column_type = col_info.get("type")
                lower = col_info.get('lower', None)
                upper = col_info.get('upper', None)
                max_fre = col_info.get('max_fre', None)
                insert_column_sql = """insert into metadata_column(column_name, type, lower, upper, max_fre, table_id,
                                create_time, status)
                                values (%s, %s, %s, %s, %s, %s, %s, %s)
                                """
                insert_column_num = cur.execute(insert_column_sql, (
                    column_name, column_type, lower, upper, max_fre, table_id, time.time(), 1))
                if insert_column_num == 1:
                    logging.info("dpaccess-internal-update_meta: insert_column_num 添加成功")
                else:
                    logging.error("dpaccess-internal-update_meta: insert_column_num 添加失败")
                    raise MetaDataError("1026", "insert_key_meta_sql execute failed!")

                # If it is a map type, determine whether there is a key_metas
                if column_type.startswith('Map'):
                    query_column_sql = """select id from metadata_column where column_name = %s and table_id = %s
                    and status = 1"""
                    cur.execute(query_column_sql, (column_name, table_id))
                    res = cur.fetchone()
                    if res:
                        column_id = res[0]
                    else:
                        logging.error("dpaccess-internal-update_meta: query_column_sql 查询失败")
                        raise MetaDataError("1026", "query_column_sql execute failed!")
                    key_type = column_type[4: len(column_type) - 1].split(',')[0]
                    value_type = column_type[4: len(column_type) - 1].split(',')[1].lstrip()
                    key_metas = col_info.get('key_metas', None)
                    # If there is key_metas, traverse each event information + column_id of key_metas, and insert it
                    # into the table metadata_key_metas
                    if key_metas:
                        for key_meta in key_metas:
                            insert_key_meta_sql = """insert into metadata_column_map_key_metas(key_type, value_type,
                                            event_lower, event_upper, name, column_id, create_time, status)
                                            values
                                            (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                            """
                            insert_key_meta_num = cur.execute(insert_key_meta_sql, (key_type, value_type,
                                                                                    key_meta.get('lower', None),
                                                                                    key_meta.get('upper', None),
                                                                                    key_meta['name'], column_id,
                                                                                    time.time(), 1))
                            if insert_key_meta_num == 1:
                                logging.info(
                                    "dpaccess-internal-update_meta: metadata_column_map_key_metas added successfully")
                            else:
                                logging.error(
                                    "dpaccess-internal-update_meta: metadata_column_map_key_metas add failed")
                                raise MetaDataError("1026", "insert_key_meta_sql execute failed!")

        # update columns
        if update_columns_list and len(update_columns_list) > 0:
            for column_name in update_columns_list:
                col_info = new_meta['tables'][0]['columns'].get(column_name)
                column_type = col_info.get("type")
                lower = col_info.get('lower', None)
                upper = col_info.get('upper', None)
                max_fre = col_info.get('max_fre', None)
                update_column_sql = """
                    update metadata_column
                    set type = %s,
                    lower = %s,
                    upper = %s,
                    max_fre = %s
                    where table_id = %s and column_name = %s and status = 1
                """
                update_column_num = cur.execute(update_column_sql,
                                                (column_type, lower, upper, max_fre, table_id, column_name))
                if update_column_num == 1:
                    logging.info("dpaccess-internal-update_meta: update_column_num added successfully")
                else:
                    logging.error("dpaccess-internal-update_meta: update_column_num add failed")
                    raise MetaDataError("1026", "update_column_num execute failed!")

        # delete columns
        if delete_columns_list and len(delete_columns_list) > 0:
            for column_name in delete_columns_list:
                delete_column_sql = """
                                update metadata_column
                                set status = 0
                                where table_id = %s and column_name = %s and status = 1
                            """
                delete_column_num = cur.execute(delete_column_sql, (table_id, column_name))
                if delete_column_num == 1:
                    logging.info("dpaccess-internal-update_meta: delete_column_num added successfully")
                else:
                    logging.error("dpaccess-internal-update_meta: delete_column_num add failed")
                    raise MetaDataError("1026", "delete_column_num execute failed!")

        # add key_metas
        # add_key_metas_list struct: [['metric_data', 'accumulate_convert_cnt']]
        if add_key_metas_list and len(add_key_metas_list) > 0:
            for item in add_key_metas_list:
                column_name = item[0]
                name = item[1]
                lower = item[2]
                upper = item[3]
                key_type = item[4]
                value_type = item[5]
                column_id = get_column_id(column_name, table_id)
                insert_key_meta_sql = """insert into metadata_column_map_key_metas(key_type, value_type,
                                                        event_lower, event_upper, name, column_id, create_time, status)
                                                        values
                                                        (%s, %s, %s, %s, %s, %s, %s, %s)
                                                        """
                insert_key_meta_num = cur.execute(insert_key_meta_sql, (key_type, value_type, lower, upper,
                                                                        name, column_id,
                                                                        time.time(), 1))
                if insert_key_meta_num == 1:
                    logging.info("dpaccess-internal-update_meta: insert_key_meta_num added successfully")
                else:
                    logging.error("dpaccess-internal-update_meta: insert_key_meta_num add failed")
                    raise MetaDataError("1026", "insert_key_meta_sql execute failed!")

        # update key_metas
        if update_key_metas_list and len(update_key_metas_list):
            for item in update_key_metas_list:
                column_name = item[0]
                name = item[1]
                lower = item[2]
                upper = item[3]
                key_type = item[4]
                value_type = item[5]
                column_id = get_column_id(column_name, table_id)
                update_key_meta_sql = """
                    update metadata_column_map_key_metas
                    set event_lower = %s, event_upper = %s, key_type = %s, value_type =%s
                    where column_id = %s and name = %s"""
                update_key_meta_num = cur.execute(update_key_meta_sql,
                                                  (lower, upper, key_type, value_type, column_id, name))
                if update_key_meta_num == 1:
                    logging.info("dpaccess-internal-update_meta: update_key_meta_num added successfully")
                else:
                    logging.error("dpaccess-internal-update_meta: update_key_meta_num add failed")
                    raise MetaDataError("1026", "update_key_meta_sql execute failed!")

        # delete key_metas
        if delete_key_metas_list and len(delete_key_metas_list):
            for item in delete_key_metas_list:
                column_name = item[0]
                name = item[1]
                column_id = get_column_id(column_name, table_id)
                delete_key_meta_sql = """
                                update metadata_column_map_key_metas
                                set status = 0
                                where column_id = %s and name = %s"""
                delete_key_meta_num = cur.execute(delete_key_meta_sql, (column_id, name))
                if delete_key_meta_num == 1:
                    logging.info("dpaccess-internal-update_meta: delete_key_meta_num added successfully")
                else:
                    logging.error("dpaccess-internal-update_meta: delete_key_meta_num add failed")
                    raise MetaDataError("1026", "update_key_meta_sql execute failed!")

        # update last_update_time of metadata_table
        update_last_time_sql = """
            update metadata_table
            set last_update_time = UNIX_TIMESTAMP(now())
            where id = %s"""
        update_last_time_num = cur.execute(update_last_time_sql, table_id)
        if update_last_time_num == 1:
            logging.info("dpaccess-internal-update_meta: update_last_time_sql added successfully")
        else:
            logging.error("dpaccess-internal-update_meta: update_last_time_sql add failed")
            raise MetaDataError("1026", "update_key_meta_sql execute failed!")

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        logging.exception("dpaccess-internal-update_meta Exception: \n" + str(e))
        raise MetaDataError("1029",
                            "update meta failed, Exception: {}\n prefix={}, db_name={}, table_name={}, db_type={}"
                            .format(str(e), prefix, db_name, table_name, db_type))
    finally:
        cur.close()
        conn.close()


def update_column(prefix, db_name, table_name, column):
    """ Update a complete single column record

    """
    logging.info(
        "dpaccess-internal-update_column: prefix=%s, db_name=%s, table_name=%s", prefix, db_name, table_name)

    conn = mysql_client.get_connection()
    cur = conn.cursor()
    try:
        update_column_sql = """
                update metadata_column
                set column_name = %s, type = %s, lower = %s, upper = %s, max_fre = %s, clipping_flag = %s
                , clipping_upper = %s, clipping_lower = %s, status = %s
                where id =
                (
                    select id from
                      ( select metadata_column.id
                        from
                          (
                              select metadata_table.id
                              from metadata_table
                              join metadata_db
                              on metadata_db.prefix = %s
                              and metadata_db.db_name = %s
                              and metadata_table.table_name = %s

                          ) tb_table_id
                          join
                             metadata_column
                          on tb_table_id.id = metadata_column.table_id
                          and column_name = %s
                      ) as tx_column_id
                )
                """
        cur.execute(update_column_sql, (column["column_name"], column["type"], column["lower"], column["upper"],
                                        column["max_fre"], column["clipping_flag"], column["clipping_upper"],
                                        column["clipping_lower"], column["status"], prefix, db_name, table_name,
                                        column["column_name"]))
        conn.commit()
    except Exception as e:
        logging.exception("dpaccess-internal-update_column Exception: \n" + str(e))
        raise MetaDataError("1024", "update_column failed, Exception: {}\n, prefix={}, db_name={}, "
                                    "table_name={}, column={}".format(str(e), prefix, db_name, table_name, column))
    finally:
        cur.close()
        conn.close()


# @cachetools.cached(scache_match_table)
def get_match_table_meta(prefix, db_name, table_name):
    """
        get all columns of metadata for rangers
    """
    logging.info("dpaccess-internal-get_match_table_meta: prefix=%s, db_name=%s, table_name=%s", prefix, db_name,
                 table_name)

    columns = {}
    table = {'tablename': table_name, 'columns': columns}
    tables = [table]
    meta_dict = {'database': db_name, 'tables': tables}

    conn = mysql_client.get_connection()
    cur = conn.cursor()
    try:
        # 查询 db_type
        query_db_type_sql = """
                    select metadata_db.db_type
                    from  metadata_db
                    where metadata_db.prefix = %s and metadata_db.db_name = %s and metadata_db.status = 1
                    """
        cur.execute(query_db_type_sql, (prefix, db_name))
        res = cur.fetchone()
        if res:
            db_type = res[0]
            meta_dict['engine'] = db_type
        else:
            logging.exception("dpaccess-internal-get_match_table_meta Exception: can not get the db_type!")
            raise MetaDataError(MetaDataErrors.MATCH_META_ERROR.value,
                                "dpaccess-internal-get_match_table_meta, can not get the db_type!")
        # 查询 columns
        query_columns_sql = """
                select metadata_column.id, column_name, type, lower, upper, max_fre, clipping_flag, clipping_upper, clipping_lower
                from
                (   select metadata_table.id
                    from metadata_db
                    join metadata_table
                    on metadata_db.id = metadata_table.db_id
                    where metadata_db.prefix = %s and metadata_db.db_name = %s and metadata_db.status = 1
                    and metadata_table.table_name = %s and metadata_table.status = 1
                ) d_t
                join
                metadata_column
                on d_t.id = metadata_column.table_id
                where metadata_column.status = 1
                """
        cur.execute(query_columns_sql, (prefix, db_name, table_name))
        res = cur.fetchall()
        if res:
            for row in res:
                column_name = row[1]
                column_type = row[2]
                col_items = {"type": column_type}
                # lower upper max_fre
                # Here the null value is checked out row[3], row[4], row[5] will be the string 'None'
                if row[3] and row[3] != 'None':
                    col_items['lower'] = row[3]
                if row[4] and row[4] != 'None':
                    col_items['upper'] = row[4]
                if row[5] and row[5] != 'None':
                    col_items['max_fre'] = row[5]
                if row[6] and row[6] != 'None':
                    col_items['clipping_flag'] = row[6]
                if row[7] and row[7] != 'None':
                    col_items['clipping_upper'] = row[7]
                if row[8] and row[8] != 'None':
                    col_items['clipping_lower'] = row[8]

                # not query key_metas here
                if column_type.startswith('Map'):
                    col_items['key_metas'] = []
                columns[column_name] = col_items
        else:
            logging.exception("dpaccess-internal-get_match_table_meta Exception: can not get the columns!")
            raise MetaDataError(MetaDataErrors.MATCH_META_ERROR.value,
                                "dpaccess-internal-query_meta: can not get the columns!")
    except Exception as e:
        logging.exception("dpaccess-internal-get_match_table_meta Exception: \n" + str(e))
        raise MetaDataError(MetaDataErrors.MATCH_TABLE_EXCEPTION.value,
                            "dpaccess-internal-get_match_table_meta Exception: \n" + str(e))
    finally:
        cur.close()
        conn.close()
    return meta_dict


@cachetools.cached(scache_match_key_meta)
def get_match_key_meta(prefix, db_name, table_name, column_name, event, name):
    """
        get key_meta of metadata for rangers
    """
    logging.info(
        "dpaccess-internal-get_match_key_meta: prefix=%s, db_name=%s, table_name=%s, column_name=%s, event=%s, name=%s",
        prefix, db_name, table_name, column_name, event, name)

    key_meta = {}
    if not if_exist_meta(prefix, db_name, table_name):
        raise MetaDataError(MetaDataErrors.MATCH_TABLE_EXCEPTION.value, "Query failed，the metadata doesn't exist!")
    else:
        conn = mysql_client.get_connection()
        cur = conn.cursor()
        try:
            query_key_meta_sql = """
            select metadata_column_map_key_metas.id, event_name, event_lower, event_upper, name
            from
            (
                select metadata_column.id
                from
                (   select metadata_table.id
                    from metadata_db
                    join metadata_table
                    on metadata_db.id = metadata_table.db_id
                    where metadata_db.prefix = %s and metadata_db.db_name = %s and metadata_db.status = 1
                    and metadata_table.table_name = %s and metadata_table.status = 1
                ) d_t
                join
                metadata_column
                on d_t.id = metadata_column.table_id
                where metadata_column.column_name = %s and metadata_column.status = 1
            ) t
            join
            metadata_column_map_key_metas
            on t.id = metadata_column_map_key_metas.column_id
            where metadata_column_map_key_metas.status = 1 and metadata_column_map_key_metas.name = %s
            and metadata_column_map_key_metas.event_name = %s
            """
            cur.execute(query_key_meta_sql, (prefix, db_name, table_name, column_name, name, event))
            res = cur.fetchone()
            if not res:
                raise MetaDataError(MetaDataErrors.MATCH_META_ERROR.value, "The queried key_meta does not exist")
            key_meta['id'] = res[0]
            key_meta['event'] = res[1]
            key_meta['lower'] = res[2]
            key_meta['upper'] = res[3]
            key_meta['name'] = res[4]
        except Exception as e:
            logging.exception("dpaccess-internal-get_match_key_meta Exception: \n" + str(e))
            raise MetaDataError(MetaDataErrors.MATCH_TABLE_EXCEPTION.value,
                                "dpaccess-internal-get_match_key_meta Exception: \n" + str(e))
        finally:
            cur.close()
            conn.close()
        return key_meta


@cached(cache=TTLCache(maxsize=64, ttl=10))
def if_exist_meta(prefix, db_name, table_name):
    """
        Check whether metadata exists
    """
    logging.info("dpaccess-internal-if_exist_meta: prefix=%s, db_name=%s, table_name=%s", prefix, db_name, table_name)

    conn = mysql_client.get_connection()
    cur = conn.cursor()
    try:
        sql = """select metadata_db.id
                    from metadata_db
                    join metadata_table
                    on metadata_db.id = metadata_table.db_id
                    and metadata_db.prefix = %s
                    and metadata_db.db_name = %s
                    and metadata_db.status = 1
                    and metadata_table.table_name = %s
                    and metadata_table.status =1"""
        cur.execute(sql, (prefix, db_name, table_name))
        res = cur.fetchone()
    except Exception as e:
        logging.exception("dpaccess-internal-if_exist_meta Exception: \n" + str(e))
        raise MetaDataError(MetaDataErrors.MATCH_TABLE_EXCEPTION.value,
                            "dpaccess-internal-if_exist_meta Exception: \n" + str(e))
    finally:
        cur.close()
        conn.close()
    return True if res else False


def if_exist_meta_without_cache(prefix, db_name, table_name):
    """
        for metadata crud unit
    """
    logging.info("dpaccess-internal-if_exist_meta_without_cache: prefix=%s, db_name=%s, table_name=%s", prefix, db_name,
                 table_name)

    conn = mysql_client.get_connection()
    cur = conn.cursor()
    try:
        sql = """select metadata_db.id
                    from metadata_db
                    join metadata_table
                    on metadata_db.id = metadata_table.db_id
                    and metadata_db.prefix = %s
                    and metadata_db.db_name = %s
                    and metadata_db.status = 1
                    and metadata_table.table_name = %s
                    and metadata_table.status =1"""
        cur.execute(sql, (prefix, db_name, table_name))
        res = cur.fetchone()
    except Exception as e:
        logging.exception("dpaccess-internal-if_exist_meta_without_cache Exception: \n" + str(e))
        raise MetaDataError("1022", "dpaccess-internal-if_exist_meta_without_cache Exception: \n" + str(e))
    finally:
        cur.close()
        conn.close()
    return True if res else False


def get_column_id(column_name, table_id):
    logging.info("dpaccess-internal-get_column_id: column_name=%s, table_id=%s", column_name, table_id)
    conn = mysql_client.get_connection()
    cur = conn.cursor()
    try:
        query_column_id_sql = """select id from metadata_column where column_name = %s and table_id = %s and status = 1"""
        cur.execute(query_column_id_sql, (column_name, table_id))
        res = cur.fetchone()
        if res:
            column_id = res[0]
            return column_id
        return None
    except Exception as e:
        logging.exception("dpaccess-internal-get_column_id Exception: \n" + str(e))
        raise MetaDataError(MetaDataErrors.MATCH_TABLE_EXCEPTION.value,
                            "dpaccess-internal-get_column_id Exception: \n" + str(e))
    finally:
        cur.close()
        conn.close()


def get_db_id(prefix, db_name):
    """
        query db_id
    """
    logging.info("dpaccess-internal-get_db_id: prefix=%s, dbname=%s", prefix, db_name)
    conn = mysql_client.get_connection()
    cur = conn.cursor()
    try:
        sql = """select id from metadata_db where prefix = %s and db_name = %s and status = 1"""
        cur.execute(sql, (prefix, db_name))
        db_res = cur.fetchone()
        if db_res:
            return db_res[0]
        return None
    except Exception as e:
        conn.rollback()
        logging.exception("dpaccess-internal-get_db_id Exception: \n" + str(e))
        raise MetaDataError(MetaDataErrors.GET_DB_ID_ERROR.value,
                            "get_db_id failed, Exception: {}\n prefix={}, db_name={}".format(str(e), prefix, db_name))
    finally:
        cur.close()
        conn.close()


def query_meta(prefix, db_name, table_name):
    """
        Query a complete metadata
    """
    logging.info("dpaccess-internal-query_meta: prefix=%s, db_name=%s, table_name=%s", prefix, db_name, table_name)

    columns = {}
    table = {'tablename': table_name, 'columns': columns}
    tables = [table]
    meta_dict = {'database': db_name, 'tables': tables}

    if not if_exist_meta(prefix, db_name, table_name):
        raise MetaDataError("1022", "Query failed，the metadata: doesn't exist!")
    else:
        conn = mysql_client.get_connection()
        cur = conn.cursor()
        try:
            # query db_type
            query_db_type_sql = """
                        select metadata_db.db_type
                        from  metadata_db
                        where metadata_db.prefix = %s and metadata_db.db_name = %s and metadata_db.status = 1
                        """
            cur.execute(query_db_type_sql, (prefix, db_name))
            res = cur.fetchone()
            if res:
                db_type = res[0]
                meta_dict['engine'] = db_type
            else:
                logging.error("dpaccess-internal-query_meta: query_db_type_sql 查询失败")
                raise MetaDataError("1026", "query_db_type_sql execute failed!")
            # query columns
            query_columns_sql = """
                    select metadata_column.id, column_name, type, lower, upper, max_fre, clipping_flag, clipping_upper,
                    clipping_lower
                    from
                    (   select metadata_table.id
                        from metadata_db
                        join metadata_table
                        on metadata_db.id = metadata_table.db_id
                        where metadata_db.prefix = %s and metadata_db.db_name = %s and metadata_db.status = 1
                        and metadata_table.table_name = %s and metadata_table.status = 1
                    ) d_t
                    join
                    metadata_column
                    on d_t.id = metadata_column.table_id
                    where metadata_column.status = 1
                    """
            cur.execute(query_columns_sql, (prefix, db_name, table_name))
            res = cur.fetchall()
            if res:
                for row in res:
                    column_id = row[0]
                    column_name = row[1]
                    column_type = row[2]
                    col_items = {"type": column_type}
                    # lower upper max_fre
                    # The row[3], row[4], row[5] detected by the null value here will be the string 'None'
                    if row[3] and row[3] != 'None':
                        col_items['lower'] = row[3]
                    if row[4] and row[4] != 'None':
                        col_items['upper'] = row[4]
                    if row[5] and row[5] != 'None':
                        col_items['max_fre'] = row[5]
                    if row[6] and row[6] != 'None':
                        col_items['clipping_flag'] = row[6]
                    if row[7] and row[7] != 'None':
                        col_items['clipping_upper'] = row[7]
                    if row[8] and row[8] != 'None':
                        col_items['clipping_lower'] = row[8]

                    # key_metas
                    if column_type.startswith('Map'):
                        query_key_metas_sql = """
                        select event_name, event_lower, name, event_upper, key_type, value_type
                        from metadata_column
                        join
                        metadata_column_map_key_metas
                        on metadata_column.id = metadata_column_map_key_metas.column_id
                        where metadata_column.status = 1 and metadata_column_map_key_metas.status = 1
                        and metadata_column.id = %s
                        """
                        cur.execute(query_key_metas_sql, column_id)
                        res = cur.fetchall()
                        if res:
                            key_metas = []
                            for item in res:
                                key_meta = {"event": item[0], "lower": item[1], "name": item[2], "upper": item[3]}
                                key_metas.append(key_meta)
                            col_items['key_metas'] = key_metas
                    columns[column_name] = col_items
            else:
                logging.error("dpaccess-internal-query_meta: query_columns_sql 查询失败")
                raise MetaDataError("1026", "query_columns_sql execute failed!")
        except Exception as e:
            logging.exception("dpaccess-internal-query_meta Exception: \n" + str(e))
            raise MetaDataError("1022", "dpaccess-internal-query_meta Exception: \n" + str(e))
        finally:
            cur.close()
            conn.close()
        return meta_dict


def get_table_info(prefix, db_name, table_name):
    logging.info("dpaccess-internal-get_table_info: prefix=%s, dbname=%s, table_name=%s", prefix, db_name, table_name)
    conn = mysql_client.get_connection()
    cur = conn.cursor()
    try:
        query_table_id_sql = """
            select metadata_table.id, metadata_table.last_update_time, metadata_table.status
            from metadata_table
            join metadata_db
            where metadata_db.prefix = %s
            and metadata_db.db_name = %s
            and metadata_db.status = 1
            and metadata_table.table_name = %s
            and metadata_table.db_id = metadata_db.id
        """
        cur.execute(query_table_id_sql, (prefix, db_name, table_name))
        res = cur.fetchone()
        if res:
            return {"table_id": res[0], "last_update_time": res[1], "status": res[2]}
        else:
            return None
    except Exception as e:
        logging.exception("dpaccess-internal-get_table_info Exception: \n" + str(e))
        raise MetaDataError("1022", "dpaccess-internal-get_table_info Exception: \n" + str(e))
    finally:
        cur.close()
        conn.close()


# TODO plus cache
def get_match_key_meta_of_hive(prefix, db_name, table_name, column_name, keyname):
    logging.info(
        "dpaccess-internal-get_match_olap_key_meta: prefix=%s, db_name=%s, table_name=%s, column_name=%s, name=%s",
        prefix, db_name, table_name, column_name, keyname)

    key_meta = {}
    conn = mysql_client.get_connection()
    cur = conn.cursor()
    try:
        query_key_meta_sql = """
           select event_lower, event_upper, name
           from
           (
               select metadata_column.id
               from
               (   select metadata_table.id
                   from metadata_db
                   join metadata_table
                   on metadata_db.id = metadata_table.db_id
                   where metadata_db.prefix = %s and metadata_db.db_name = %s and metadata_db.status = 1
                   and metadata_table.table_name = %s and metadata_table.status = 1
               ) d_t
               join
               metadata_column
               on d_t.id = metadata_column.table_id
               where metadata_column.column_name = %s and metadata_column.status = 1
           ) t
           join
           metadata_column_map_key_metas
           on t.id = metadata_column_map_key_metas.column_id
           where metadata_column_map_key_metas.status = 1 and metadata_column_map_key_metas.name = %s
           """

        cur.execute(query_key_meta_sql, (prefix, db_name, table_name, column_name, keyname))
        res = cur.fetchone()
        if not res:
            logging.exception(MetaDataError("1026", "The queried key_meta does not exist"))
            return None
        key_meta['lower'] = res[0]
        key_meta['upper'] = res[1]
        key_meta['name'] = res[2]
    except Exception as e:
        logging.exception("dpaccess-internal-get_match_olap_key_meta Exception: \n" + str(e))
        raise MetaDataError("1022", "dpaccess-internal-get_match_olap_key_meta Exception: \n" + str(e))
    finally:
        cur.close()
        conn.close()
    return key_meta


def get_column(prefix, db_name, table_name, column_name):
    logging.info("dpaccess-internal-get_column: prefix=%s, db_name=%s, table_name=%s", prefix, db_name, table_name)
    conn = mysql_client.get_connection()
    cur = conn.cursor()
    try:
        query_column_sql = """
            select * from metadata_column
            where id =
                  ( select metadata_column.id from
                      (
                          select metadata_table.id
                          from metadata_table
                          join metadata_db
                          on metadata_db.prefix = %s
                          and metadata_db.db_name = %s
                          and metadata_table.table_name = %s

                      ) tb_table_id
                      join
                         metadata_column
                      on tb_table_id.id = metadata_column.table_id
                      and column_name = %s
                      )
        """
        cur.execute(query_column_sql, (prefix, db_name, table_name, column_name))
        res = cur.fetchone()
        column = {}
        if res:
            column["create_time"] = res[0]
            column["status"] = res[1]
            column["id"] = res[2]
            column["column_name"] = res[3]
            column["type"] = res[4]
            column["lower"] = res[5]
            column["upper"] = res[6]
            column["max_fre"] = res[7]
            column["table_id"] = res[8]
            column["clipping_flag"] = res[9]
            column["clipping_upper"] = res[10]
            column["clipping_lower"] = res[11]
            return column
        return None
    except Exception as e:
        logging.exception("dpaccess-internal-get_column Exception: \n" + str(e))
        raise MetaDataError(MetaDataErrors.MATCH_TABLE_EXCEPTION.value,
                            "dpaccess-internal-get_column Exception: \n" + str(e))
    finally:
        cur.close()
        conn.close()
