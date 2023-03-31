# Copyright (2023) Beijing Volcano Engine Technology Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import redis
import uuid
import time
from utils.config.load_config import load_config


class Redis:
    """
        Provide redis client and refactor basic method for curd

    """

    def __init__(self, host, port, user, password):
        if user is not None and password is not None:
            author = user + '@' + password
        else:
            author = None
        self.client = redis.StrictRedis(host=host, port=port, password=author)

    def set(self, key, value, ex=None):
        return self.client.set(key, value, ex)

    def get(self, key):
        return self.client.get(key)

    def hset(self, key, kv_map):
        """
            set a set of key-value pairs to redis
        """
        return self.client.hmset(key, kv_map)

    def hget(self, key, hkeys):
        """
            get a list of value corresponding to the hash-keys
        """
        res = self.client.hmget(key, hkeys)
        values = [float(i.decode()) for i in res]
        return dict(zip(hkeys, values))

    def hgetall(self, key):
        """
            get a list of hash-key and value corresponding to the key
        """
        res = self.client.hgetall(key)
        return res

    def hincrby(self, key, kv_map):
        """
            add values to the original data
        """
        for k, v in kv_map.items():
            self.client.hincrby(key, k, v)

    def exists(self, key):
        return True if self.client.exists(key) == 1 else False

    def delete(self, key):
        return True if self.client.delete(key) == 1 else False

    def lock(self, lock_name, key, ex_time=1, timeout=10):
        """
            get distributed lock, set timeout and polling time
        """
        self.uuid = str(uuid.uuid4())
        start = time.time()
        end = start + timeout
        res = False
        # failed to get lock then polled until success or timeout
        while res is not True:
            res = self.client.set(lock_name + "_lock." + key, self.uuid, nx=True, ex=ex_time)
            if time.time() > end:
                break
        return res

    def unlock(self, lock_name, key):
        """
            using lua scripts to ensure atomicity of compare and delete operations
        """
        key = lock_name + "_lock." + key
        lua_script = """
            if redis.call("get", KEYS[1]) == ARGV[1] then
                return redis.call('del', KEYS[1])
            else
                return 0
            end
        """
        return True if self.client.eval(lua_script, 1, key, self.uuid) == 1 else False


redis_config = load_config("redis.ini", "redis")
redis_client = redis.StrictRedis(host=redis_config.get("host"), port=redis_config.get("port"),
                                 password=redis_config.get("pwd"))
