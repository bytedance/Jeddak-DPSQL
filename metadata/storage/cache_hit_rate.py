from metadata.storage.metadata_bean_manager import scache_match_table, scache_match_key_meta


def get_match_table_hit_rate():
    """
        Records the cache hit ratio of match_table
    """
    hit = scache_match_table.hits()
    return hit


def get_match_key_meta_hit_rate():
    """
        Records the cache hit ratio of match_key_meta
    """
    hit = scache_match_key_meta.hits()
    return hit
