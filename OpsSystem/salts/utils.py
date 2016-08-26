# -*- coding=UTF-8 -*-
import urllib,urllib2,json
import re

try:
    from salt.client import LocalClient
    from salt.wheel import Wheel
    from salt.config import master_config
except:
    print 'please install salt!!!   commands: pip install salt '
    exit(1)

class SaltByWebApi(object):
    '''
    SaltApi class,使用saltapi Restful获取数据
    '''
    def __init__(self,url,user,password):
	self.headers={'Accept':'application/json'}
	self.auth_params={'username':user,'password':password,'eauth':'pam'}
	self.url=url.rstrip('/')
	self.user=user
	self.password=password
        self.token=self.get_token_id()
	self.headers['X-Auth-Token']=self.token

    def get_token_id(self):
	body=urllib.urlencode(self.auth_params)
	request=urllib2.Request(self.url+'/login',body,self.headers)
	try:
	    response=urllib2.urlopen(request)
	except Exception as e:
	    print 'Error: %s ' %e
            exit(1)
        result=json.load(response)
	return result['return'][0]['token']
    def get_minion_info(self,pre):
	self.auth_params.update({'tgt':'*','fun':'key.list_all','client':'local'})
	body=urllib.urlencode(self.auth_params);
	print self.auth_params
	request=urllib2.Request(self.url+pre,body,self.headers)
	response=urllib2.urlopen(request)
	j=json.load(response)
        print j

class SaltByLocalApi(object):
    '''
    Saltapi class 通过salt本地接口调用,需和salt-master服务在同一台机器
    '''
    def __init__(self,main_config):
	self.opts=master_config(main_config)
	self.wheel=Wheel(self.opts)
	self.client=LocalClient()
	# the code(next line) no error,but i dont't know my environment or verison has two salt
	self.connected_minions_list = self.wheel.call_func('minions.connected')
	self.key_dict=self.wheel.call_func('key.list_all')
	self.total=len(self.key_dict['minions'])+len(self.key_dict['minions_pre'])+len(self.key_dict['minions_denied'])+len(self.key_dict['minions_rejected'])
    def get_minions_key_status(self):
	reject=len(self.key_dict['minions_rejected'])
	unaccept=len(self.key_dict['minions_pre'])
	accept=len(self.key_dict['minions'])
	return [accept,reject,unaccept]
    def get_minions_status(self):
        return [self.total,len(self.connected_minions_list),self.total-len(self.connected_minions_list)]

    def get_host_info(self):
	#minions=self.connected_minions_list #because no data,i use next methon
	minions=self.key_dict['minions']
	ret=self.client.cmd(minions,'grains.item',['mem_total',
	    'osfullname',
	    'host',
	    'osrelease',
	    'num_cpus',
	    'ipv4',
	    'group',
	    'area',
	    'usage'],expr_form='list')
        host_info_dict={}
	for k,v in ret.iteritems():
	    v['ipv4'].remove('127.0.0.1')
	    ips='/'.join(v['ipv4']) if len(v['ipv4'])>1 else v['ipv4'][0]
	    values=[v['host'],
		    ips,
		    v['osfullname']+v['osrelease'],
		    str(v['num_cpus'])+' cores',
		    str(v['mem_total'])+' MB',
		    v['group'],
		    v['area'],
		    v['usage']]
	    host_info_dict[k]=values
        return host_info_dict
    def get_master_config(self):
	return self.opts
    def get_grains(self):
	if self.connected_minions_list is None or len(self.connected_minions_list)<1:
	    return None
	return self.client.cmd(self.connected_minions_list[0],'grains.items',[])



def parse_target_params(target,match):
    '''
    处理应用部署参数
    Args:
       target: 匹配目标
       match: 匹配模式
    Returns:
        返回一个元组: 第一个元素为布尔值,标志正确与否,第二个为错误信息 
    '''
    saltapi=SaltByLocalApi('/etc/salt/master')
    active_minion_list=saltapi.connected_minions_list
    nodegroup_list=[]
    t_list=[]
    target=target.replace(' ','')
    for key in saltapi.get_master_config()['nodegroups'].iterkeys():
	nodegroup_list.append(key)
    if match == 'list':
	L=target.split(',')
	t_list=[x for x in L if x !='']
        for v in t_list:
	    if v not in active_minion_list:
		return None,'do not exists the minion: %s' %v
	return True,','.join(t_list)
    elif match == 'glob':
	if target == '*':
	    pass
	elif target not in active_minion_list:
	    return None,'illegal hostname: %s ' %target
    elif match == 'grain':
        grains=saltapi.get_grains().values()[0]
	if grains is None:
	    return None,'do not exists online monions'
        var_list=target.split(':')
	length=len(var_list)
	if length<2:
	    return None,'illegal grains'
        g_var=var_list[length-1]
	g_key=var_list[:length-1]
	for k in g_key:
	    if k not in grains:
		return None,'bad grains key : %s' %k
            grains=grains[k] 
    elif match == 'nodegroup':
	if target not in nodegroup_list:
	    return None,'do not exist nodegroup: %s' %target
    elif match =='pcre':
	pass
    return True,target
def juge_danger_cmd(cmd):
    cmd=cmd.rstrip(' ').lstrip(' ')
    danger_cmd=['init','rm','shutdown','halt','reboot','dd',r':(){:|:&};:','poweroff',r':(){::&};:']
    for v in danger_cmd:
	if re.search(v,cmd):
	    return True
    return False


def test_cmd():
    client=SaltByLocalApi('/etc/salt/master')
    cmd='ls /root'
    output=client.client.cmd('self','state.sls',['php.install'],expr_form='glob')
    for k,v in output.iteritems():
	print k
	for i,j in v.iteritems():
	    print i
	    print j


if __name__=='__main__':
    #salt=SaltApi('http://10.117.74.247:8080','salt','hoover123')
    #salt.get_minion_info('/run')
    #local=SaltByLocalApi('/etc/salt/master')
    #print parse_target_params('supply_webs','nodegroup')
    test_cmd()
