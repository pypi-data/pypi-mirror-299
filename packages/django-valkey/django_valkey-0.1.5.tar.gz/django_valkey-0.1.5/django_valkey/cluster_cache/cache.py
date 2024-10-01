from valkey.cluster import ValkeyCluster

from django_valkey.base import BaseValkeyCache
from django_valkey.cache import omit_exception, CONNECTION_INTERRUPTED
from django_valkey.cluster_cache.client import DefaultClusterClient


class ClusterValkeyCache(BaseValkeyCache[DefaultClusterClient, ValkeyCluster]):
    DEFAULT_CLIENT_CLASS = "django_valkey.cluster_cache.client.DefaultClusterClient"

    @omit_exception
    def set(self, *args, **kwargs):
        return self.client.set(*args, **kwargs)

    @omit_exception
    def incr_version(self, *args, **kwargs):
        return self.client.incr_version(*args, **kwargs)

    @omit_exception
    def add(self, *args, **kwargs):
        return self.client.add(*args, **kwargs)

    def get(self, key, default=None, version=None, client=None):
        value = self._get(key, default, version, client)
        if value is CONNECTION_INTERRUPTED:
            value = default

        return value

    @omit_exception
    def _get(self, key, default=None, version=None, client=None):
        return self.client.get(key, default, version, client)

    @omit_exception
    def delete(self, *args, **kwargs):
        result = self.client.delete(*args, **kwargs)
        return bool(result)

    @omit_exception
    def delete_pattern(self, *args, **kwargs):
        kwargs.setdefault("itersize", self._default_scan_itersize)
        return self.client.delete_pattern(*args, **kwargs)

    @omit_exception
    def delete_many(self, *args, **kwargs):
        return self.client.delete_many(*args, **kwargs)

    @omit_exception
    def clear(self):
        return self.client.clear()

    @omit_exception
    def get_many(self, *args, **kwargs):
        return self.client.get_many(*args, **kwargs)

    mget = get_many

    @omit_exception
    def mget_nonatomic(self, *args, **kwargs):
        return self.client.mget_nonatomic(*args, **kwargs)

    get_many_nonatomic = mget_nonatomic

    @omit_exception
    def set_many(self, *args, **kwargs):
        return self.client.set_many(*args, **kwargs)

    @omit_exception
    def mset(self, *args, **kwargs):
        return self.client.mset(*args, **kwargs)

    @omit_exception
    def mset_nonatomic(self, *args, **kwargs):
        return self.client.mset_nonatomic(*args, **kwargs)
