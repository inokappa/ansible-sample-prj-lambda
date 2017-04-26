# -*- coding: utf-8 -*-

import sys

sys.path.append("./site-packages")

def sample_handler(event, context):
    print(u'Ansible 徹底入門、絶賛販売中!!')
    message = 'Ansible 徹底入門、絶賛販売中!!'
    return { 
        'message' : message
    }
