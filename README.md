ansible-plugins
===============

Ansible Plugins

## Notification Plugins ##

### route53_zone_facts ###

Basic module to return information about a route53 hosted zone.

    - name: get route53 info
      route53_zone_facts: zone_name="example.org." region="eu-west-1"
      register: zone_info

    - debug: var=zone_info

The structure returned looks like this:

    "zone_info": {
      "changed": false,
      "invocation": {
        "module_args": "zone_name=\"example.org.\" region=\"eu-west-1\"",
        "module_name": "route53_zone_facts"
      },
      "name_servers": [
        "ns-fsfsff.awsdns-015.com.",
        "ns-dfsfsfs.awsdns-219.co.uk."
      ],
      "record_count": "2001",
      "zone_comment": "Public example.org. zone.",
      "zone_id": "ZLT8CAAHEM",
      "zone_name": "example.org.",
      "zone_type": "public"
    }


### changelog  ###

A simple notification plugin for the [Prezi Changelog](https://github.com/prezi/changelog)
event dashboard:

    - local_action: changelog message="Ansible playbook is running - 003"
      category=ansible


    - local_action: changelog
                    message="An issue was detected in our Ansible playbook!"
                    category=ansible
                    criticality=critical
                    host=changelog.example.org


## Lookup Plugins ##

Most of the AWS Lookup plugins contained here assume that you have a
correctly configured .aws/credentials file. This provides the credentials
for boto, the underlying AWS library used by Ansible.

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


### AWS Security Group ID ###

Allows you to look up the ID (something like sg-62f43457) of a remote security group.

    "{{ lookup('aws_sg_id', 'eu-west-1/my-stack-name') }}"

I wrote this to avoid adding lots of outputs to certain templates.


### AWS DefaultVPC ID ###

Allows you to look up the default VPC id for a given ec2 region.

    - debug: msg="The default vpc is {{ lookup('default_vpc', 'ap-southeast-1') }}"

Currently doesn't handle ec2classics.
