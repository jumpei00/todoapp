import configparser


conf = configparser.ConfigParser()
conf.read('config.conf')

db_name = conf['db']['name']
db_test_name = conf['db']['test_name']
db_driver = conf['db']['driver']

web_ip = conf['web']['ip']
web_port = int(conf['web']['port'])
