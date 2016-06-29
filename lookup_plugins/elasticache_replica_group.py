# (c) 2014, Dean Wilson <dean.wilson(at)gmail.com>
# this is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from ansible.plugins.lookup import LookupBase
from ansible import errors

try:
    import boto
    import boto.elasticache
except ImportError:
    raise errors.AnsibleError(
        "Can't LOOKUP(elasticache_replica_group): boto is not installed")


class ElasticacheReplicaGroup(object):

    def __init__(self, region, replica_group):
        self.region = region
        self.replica_group = replica_group
        self.meta = self.get_metadata()

        # short cut to reduce duplication in the methods.
        self.groups = self.meta['DescribeReplicationGroupsResponse']['DescribeReplicationGroupsResult']['ReplicationGroups'][0]

    def get_metadata(self):
        conn = boto.elasticache.connect_to_region(self.region)
        self.meta = conn.describe_replication_groups(self.replica_group)

        return self.meta

    def primary_endpoint_address(self):
        return self.groups['NodeGroups'][0]['PrimaryEndpoint']['Address']

    def primary_endpoint_port(self):
        return self.groups['NodeGroups'][0]['PrimaryEndpoint']['Port']


class LookupModule(LookupBase):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms, inject=None, **kwargs):

        region, repl_group, query_type = terms[0].split('/')

        self.erg = ElasticacheReplicaGroup(region, repl_group)

        value = False
        if query_type == 'endpoint_address':
            value = [self.erg.primary_endpoint_address()]
        elif query_type == 'endpoint_port':
            value = [str(self.erg.primary_endpoint_port())]

        return value
