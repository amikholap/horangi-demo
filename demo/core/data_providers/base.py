import cassandra.cluster

from demo.util import import_class


class BaseDataProvider:

    @classmethod
    def from_settings(cls, dp_settings):
        provider_class = import_class(dp_settings['class'])
        provider = provider_class(**dp_settings['params'])
        return provider


class BaseCassandraDataProvider(BaseDataProvider):

    def __init__(self, hosts, keyspace):
        self._cluster = cassandra.cluster.Cluster(hosts)
        self._session = self._cluster.connect()
        self._session.set_keyspace(keyspace)
