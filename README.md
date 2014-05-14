ansible-plugins
===============

Ansible Plugins

## Lookup Plugins ##

### AWS Regions ###

Allows you to look up the available AWS Regions and then filters out any that contain
the string 'gov'

    - shell: echo region is =={{ item }}==
      with_items: lookup('aws_regions').split(',')

### Cloudformation ###

Allows you to look up Cloudformation stack output values.

The key should be structured like this:

    {{ lookup('cloudformation', 'region/stackname/output/outputname') }}

and an actual example:

    {{ lookup('cloudformation', 'eu-west-1/unixdaemon-natinstance/output/nat_group_id') }}


### Elasticache Replica Group ###

Allows you to look up the endpoint address and port of a given Elasticache Replica Groups

The key should be structured like this:

    {{ lookup('elasticache_replica_group', 'region/repl_group_name/query_value') }}

and some actual examples:

    {{ lookup('elasticache_replica_group', 'ap-southeast-1/locarch2-elastiredis/endpoint_address') }}

    {{ lookup('elasticache_replica_group', 'ap-southeast-1/locarch2-elastiredis/endpoint_port') }}
