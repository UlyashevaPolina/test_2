from main import *
l = ['2025-03-27 12:36:45,000 INFO django.request: GET /api/v1/checkout/ 201 OK [192.168.1.62]\n', '2025-03-27 12:35:19,000 WARNING django.security: SuspiciousOperation: Invalid HTTP_HOST header\n']
l_2 = [['2025-03-27','12:36:45,000','INFO','django.request:','GET','/api/v1/checkout/', '201', 'OK', '[192.168.1.62]\n'], 
      ['2025-03-27', '12:35:19,000', 'WARNING', 'django.security:', 'SuspiciousOperation:', 'Invalid', 'HTTP_HOST', 'header\n']]
level_dict = {'HANDLER':''}

def test_create_dict():
    assert create_dict(l,level_dict) == ({'/api/v1/checkout/':{}},{'HANDLER':'','INFO':0,'WARNING':0}, l_2 )

def test_count():
    assert count('INFO', l_2, '/api/v1/checkout/') == 1

def test_create_level_dict():
    assert create_level_dict(l_2,level_dict) == ({'HANDLER':'','INFO':1,'WARNING':0},{'/api/v1/checkout/':{'INFO':1, 'WARNING': 0}})

