# coding:utf-8

from PyQt4.QtCore import QProcess,QStringList,QString,QRegExp
import json,subprocess,os

CURRENT_VERSION = 1

class Process():

    def __init__(self):
        self.config = {}
        self.config['version'] = CURRENT_VERSION
        self.config['name'] = 'None'
        self.config['desc'] = ''
        self.config['envs'] = {}
        self.config['exe'] = ''
        self.config['args'] = ''
        self.config['inherit_sys_envs'] = True

    def setIsInherit(self,inherit):
        self.config['inherit_sys_envs'] = inherit

    def getIsInherit(self):
        return self.config['inherit_sys_envs']

    def setName(self,name):
        self.config['name'] = name

    def getName(self):
        return self.config['name']

    def getDesc(self):
        return self.config['desc']

    def setDesc(self,desc):
        self.config['desc'] = desc

    def setExe(self,exePath):
        self.config['exe'] = exePath

    def getExe(self):
        return self.config['exe']

    def setArgs(self,args):
        self.config['args'] = args

    def getArgs(self):
        return self.config['args']

    def getEnvs(self):
        return self.config['envs']

    def setEnvs(self,envs):
        self.config['envs'] = envs

    def addEnv(self,key,value):
        self.config['envs'][key] = value

    def removeEnv(self,key):
        self.config['envs'].pop(key)

    def load(self,content):
        config = json.loads(content)
        if isinstance(config,dict) and config.has_key('version') and config['version'] == CURRENT_VERSION:
            #self.config['version'] = config.get('version',-1)
            self.config['name'] = config.get('name','None')
            self.config['desc'] = config.get('desc','')
            self.config['envs'] = config.get('envs',{})
            self.config['exe'] = config.get('exe','')
            self.config['args'] = config.get('args','')
            self.config['inherit_sys_envs'] = config.get('inherit_sys_envs',True)
            return True
        return False

    def save(self):
        return json.dumps(self.config)

    def start(self):
        if len(self.getExe()) == 0:
            return False
        if self.getIsInherit():
            envs = os.environ.copy()
        else:
            envs = {}
        custom_envs = self.getEnvs()
        for key in custom_envs.keys():
            envs[key.encode('utf-8')] = custom_envs[key].encode('utf-8')
        command = '%s %s' % (self.getExe(),self.getArgs())
        command = command.encode('utf-8')
        subprocess.Popen(command,shell=True,env=envs)
        return True