#!/usr/bin/python

try:
    import boto3
    from botocore.exceptions import ClientError
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

def get_iam_role_arn(role_name, client):
    res = client.get_role(
        RoleName=role_name
    )
    return res['Role']['Arn']

def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(
        dict(
            role_name=dict(required=False, default=None, aliases=['role', 'name'])
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    try:
        region, endpoint, aws_connect_kwargs = get_aws_connection_info(module, boto3=True)
        aws_connect_kwargs.update(dict(region=region,
                                       endpoint=endpoint,
                                       conn_type='client',
                                       resource='iam'
                                       ))
        client = boto3_conn(module, **aws_connect_kwargs)
    except ClientError as e:
        module.fail_json(msg="Can't authorize connection - {0}".format(e))

    role_name = module.params['role_name']
    results = dict(arn=get_iam_role_arn(role_name, client), changed=False)
    module.exit_json(**results)

from ansible.module_utils.basic import *
from ansible.module_utils.ec2 import *

if __name__ == '__main__':
    main()
