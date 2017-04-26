#!/usr/bin/python

try:
    import boto3
    from botocore.exceptions import ClientError
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

def add_permission(module, client, **args):
    try:
        res = client.add_permission(**args)
    except Exception as e:
        module.exit_json(msg="Statement ID already exists.", changed=False)

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(
        dict(
            function_name=dict(required=False, default=None, aliases=['function', 'name']),
            statement_id=dict(required=False, default=None),
            action=dict(required=False, default=None),
            principal=dict(required=False, default=None),
            source_arn=dict(required=False, default=None)
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    try:
        region, endpoint, aws_connect_kwargs = get_aws_connection_info(module, boto3=True)
        aws_connect_kwargs.update(dict(region=region,
                                       endpoint=endpoint,
                                       conn_type='client',
                                       resource='lambda'
                                       ))
        client = boto3_conn(module, **aws_connect_kwargs)
    except ClientError as e:
        module.fail_json(msg="Can't authorize connection - {0}".format(e))

    add_permission_kwargs = {}
    add_permission_kwargs.update(dict(FunctionName=module.params['function_name'],
                                      StatementId=module.params['statement_id'],
                                      Action=module.params['action'],
                                      Principal=module.params['principal'],
                                      SourceArn=module.params['source_arn']
                                      ))

    results = dict(arn=add_permission(module, client, **add_permission_kwargs), changed=True)
    module.exit_json(**results)

from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *

if __name__ == '__main__':
    main()
