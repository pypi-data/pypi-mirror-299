from typing import Dict

from valkey.cluster import ValkeyCluster
from valkey.typing import KeyT, EncodableT

from django_valkey.base_client import BaseClient


class DefaultClusterClient(BaseClient[ValkeyCluster]):
    def readonly(self, target_nodes=None, client=None):
        client = self._get_client(write=True, client=client)
        return client.readonly(target_nodes)

    def readwrite(self, target_nodes=None, client=None):
        client = self._get_client(write=True, client=client)
        return client.readwrite(target_nodes)

    def keys(
        self,
        pattern="*",
        target_nodes=ValkeyCluster.DEFAULT_NODE,
        client=None,
        **kwargs
    ):
        client = self._get_client(client=client)
        return client.keys(pattern, target_nodes=target_nodes, **kwargs)

    def mset(
        self,
        data: Dict[KeyT, EncodableT],
        version=None,
        client=None,
        nx=False,
        atomic=True,
    ) -> None:
        """
        Access valkey's mset method.
        it is important to take care of cluster limitations mentioned here: https://valkey-py.readthedocs.io/en/latest/clustering.html#multi-key-commands
        """
        data = {
            self.make_key(k, version=version): self.encode(v) for k, v in data.items()
        }
        client = self._get_client(write=True, client=client)
        if not atomic:
            return client.mset_nonatomic(data)
        if nx:
            return client.msetnx(data)
        return client.mset(data)

    set_many = mset

    def msetnx(self, data: Dict[KeyT, EncodableT], version=None, client=None):
        return self.mset(data, version=version, client=client, nx=True)

    def mset_nonatomic(self, data: Dict[KeyT, EncodableT], version=None, client=None):
        return self.mset(data, version=version, client=client, atomic=False)

    def mget(self, keys, version=None, client=None):
        """
        Access valkey's mget method.
        it is important to take care of cluster limitations mentioned here: https://valkey-py.readthedocs.io/en/latest/clustering.html#multi-key-commands
        """
        return self.get_many(keys, version=version, client=client)

    def mget_nonatomic(self, keys, version=None, client=None):
        return self.get_many(keys, version=version, client=client, atomic=False)

    def keyslot(self, key, version=None, client=None):
        client = self._get_client(client=client)
        key = self.make_key(key, version=version)
        return client.keyslot(key)

    def flush_cache(self, client=None):
        client = self._get_client(client=client)
        return client.flush_cache()

    def invalidate_key_from_cache(self, client=None):
        client = self._get_client(client=client)
        return client.invalidate_key_from_cache()
