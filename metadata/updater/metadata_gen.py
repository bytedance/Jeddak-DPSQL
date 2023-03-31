import logging
from exception.enum.meradata_errors_enum import MetaDataErrors
from exception.errors import MetaDataError
from metadata.extractor.clickhouse import gen_meta_for_clickhouse
from metadata.extractor.hive import gen_meta_for_hive
from metadata.storage.metadata_bean_manager import add_db_table_name, add_columns_and_key_metas, update_meta_status, \
    update_meta, get_column, update_column
from metadata.storage.metadata_status import MetaStatus
from differential_privacy.accountant.budget import init_budget_info


def generate_meta_budget(param: dict, db_config: dict):
    """ Generate metadata and init budget table
        meta_type: what type of metadata need to generate, clickhouse or hive
        params:
            - the params of clickhouse/hive: ({'prefix': prefix, 'db_name': db_name, 'table_name': table_name,
            'db_type': db_type}, )
    """
    prefix = param['prefix']
    db_name = param['db_name']
    table_name = param['table_name']
    db_type = param['db_type']
    generate_meta(prefix, db_name, table_name, db_type, db_config)
    init_budget_info(prefix, db_name, table_name)


def generate_meta(prefix: str, db_name: str, table_name: str, db_type: str, db_config: dict) -> None:
    """
        generate the metadata of hive/clickhouse and add it to mysql
    """
    logging.info("dpaccess-internal generate_meta, prefix={}, db_name={}, table_name={}, db_type={}, db_config={}".
                 format(prefix, db_name, table_name, db_type, db_config))
    try:
        # add table_name to mysql first, and mark the status as 2 , which means the metadata is generating
        add_db_table_name(prefix, db_name, table_name, db_type)
        # gen meta
        logging.info("dpaccess-internal-gen_meta gen_meta started")
        if db_type == "hive":
            meta_dict = gen_meta_for_hive(db_name, table_name, db_config)
        elif db_type == "clickhouse":
            meta_dict = gen_meta_for_clickhouse(db_name, table_name, db_config)
        logging.info("dpaccess-internal-gen_meta gen_meta ended")
        # insert columns and key_metas of meta, and update status to 1, which means the metadata is generated
        add_columns_and_key_metas(prefix, db_name, table_name, meta_dict)
    except Exception as err:
        # if metadata generate failed, update status to -1
        update_meta_status(prefix, db_name, table_name, MetaStatus.GENERATING.value, MetaStatus.FAILED.value)
        logging.exception("dpaccess-internal-gen_meta Exception: \n" + str(err))
        raise MetaDataError(MetaDataErrors.TEA_APPID_ERROR.value,
                            "dpaccess-internal-gen_meta, Exception: {}\n prefix={}, db_name={}, "
                            "table_name={}".format(str(err), prefix, db_name, table_name))


def generate_update_meta(prefix: str, db_name: str, table_name: str, db_type: str, db_config: dict) -> None:
    """
        generate the metadata of hive/clickhouse and update it to mysql
    """
    logging.info("dpaccess-internal generate_update_meta, prefix={}, db_name={}, table_name={}, db_type={}, "
                 "db_config={}".format(prefix, db_name, table_name, db_type, db_config))
    try:
        if db_type == "hive":
            meta_dict = gen_meta_for_hive(db_name, table_name, db_config)
        elif db_type == "clickhouse":
            meta_dict = gen_meta_for_clickhouse(db_name, table_name, db_config)
        update_meta(prefix, db_name, table_name, meta_dict, db_type)
        return 1
    except Exception as err:
        logging.exception("dpaccess-internal gen_update_hive_meta:" + str(err))


def set_column_clipping(prefix: str, db_name: str, table_name: str, column_name: str, clipping_config: dict) -> None:
    """Set clipping info for column

    """
    logging.info("dpaccess-internal set_column_clipping, prefix={}, db_name={}, table_name={}, column_name={}, "
                 "clipping_config={}".format(prefix, db_name, table_name, column_name, clipping_config))
    column_info = get_column(prefix, db_name, table_name, column_name)
    column_info["clipping_flag"] = clipping_config.get("clipping_flag")
    column_info["clipping_upper"] = clipping_config.get("clipping_upper")
    column_info["clipping_lower"] = clipping_config.get("clipping_lower")
    update_column(prefix, db_name, table_name, column_info)
