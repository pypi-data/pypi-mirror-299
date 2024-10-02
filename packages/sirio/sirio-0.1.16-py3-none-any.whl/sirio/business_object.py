import requests
from enum import Enum
import tempfile
import base64
import json
from sirio.utility import *

class TypeValue(Enum):
    string = 1
    date = 2
    numeric = 3

class Object:
    id = ""
    extension = ""
    name = ""
    key = ""
    base64 = ""
    params = []
    def __init__(self, key, name, id='', extension='', params: list = []):
        self.id = id
        self.name = name
        self.extension = extension
        self.key = key
        self.params = params
        

    def createByJson(self, str_son):
        ENCODING = 'utf-8'
        self.extension = 'json'
        with tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8') as json_file:
            json.dump(str_son, json_file, ensure_ascii=False, indent=4)
            json_file.flush()  

        with open(json_file.name, 'rb') as json_file:
            encoded = base64.b64encode(json_file.read())
        self.base64 = encoded.decode(ENCODING)

class BusinessObject:
    jsonComplete = {}
    businessObject = {}
    businessKey =  ""
    subject = ""
    description = ""
    urlGetBO = ""
    urlComplete = ""
    def __init__(self, businessKey: str, urlGetBO: str, urlComplete: str):
        self.jsonComplete = {"businessKey": businessKey}
        self.objects = []
        self.data = {}
        self.urlGetBO = urlGetBO
        self.urlComplete = urlComplete
        try:
            response = requests.get(urlGetBO.replace('{businessKey}', businessKey))
            if response.status_code == 200:
                self.businessObject = response.json()
                self.description = self.businessObject['description']
                self.subject = self.businessObject['subject']
            else:
                self = None
        except Exception as ex:
            self.businessObject = self.jsonComplete
            raise Exception('Eccezione nel recupero del businessObject: {}'.format(ex))

    def getValue(self, bind:str, id:str):
        valReturn = ''
        try:
            if existsJsonPath(self.businessObject,['data',bind, id, 'value', 'value']):# 'data' in self.businessObject['data'] and bind in self.businessObject['data'] and id in self.businessObject['data'][bind] and 'value' in self.businessObject['data'][bind][id] and 'value' in self.businessObject['data'][bind][id]['value']:
                valReturn = self.businessObject['data'][bind][id]['value']['value']
        except Exception as ex:
            print("Eccezione su getValue [{}][{}] - {}".format(bind, id, ex))
        return valReturn
    
    def setValue(self, bind: str, id: str, value, typeValue=TypeValue.string, descriprion=''):
        if 'data' not in self.jsonComplete:
            self.jsonComplete['data'] = {}
        if bind not in self.jsonComplete['data']:
            self.jsonComplete['data'][bind] = {}
        if id not in self.jsonComplete['data'][bind]:
            self.jsonComplete['data'][bind][id] =  {"dataType": typeValue.name,  "description": descriprion,   "value": {"value": value }, "extendedValue": [] }
        elif self.jsonComplete['data'][bind][id]['value']['value'] != value:
            self.jsonComplete['data'][bind][id]['value']['value'] = value

        if 'data' not in self.businessObject:
            self.businessObject['data'] = {}
        if bind not in self.businessObject['data']:
            self.businessObject['data'][bind] = {}
        if id not in self.businessObject['data'][bind]:
            self.businessObject['data'][bind][id] = {"dataType": typeValue.name,  "description": descriprion,   "value": {"value": value }, "extendedValue": [] }
        elif self.businessObject['data'][bind][id]['value']['value'] != value:
            self.businessObject['data'][bind][id]['value']['value'] = value
    
    def getProcessData(self, id:str):
        valReturn = ''
        try:
            if existsJsonPath(self.businessObject,['processData',id]):
                valReturn = self.businessObject['processData'][id]
        except Exception as ex:
            print("Eccezione su getProcessData [{}] - {}".format(id, ex))
        return valReturn
    
    def deleteProcessData(self, id:str):
        try:
            if existsJsonPath(self.businessObject,['processData',id]):
                self.businessObject['processData'].pop(id)
            if existsJsonPath(self.jsonComplete,['processData',id]):
                self.jsonComplete['processData'].pop(id)
        except Exception as ex:
            print("Eccezione su deleteProcessData [{}] - {}".format(id, ex))
        
    
    def setProcessData(self, id: str, value):
        if 'processData' not in self.jsonComplete:
            self.jsonComplete['processData'] = {}
        if id not in self.jsonComplete['processData']:
            self.jsonComplete['processData'][id] =  value
        elif self.jsonComplete['processData'][id] != value:
            self.jsonComplete['processData'][id] = value

        if 'processData' not in self.businessObject:
            self.businessObject['processData'] = {}
        if id not in self.businessObject['processData']:
            self.businessObject['processData'][id] = value
        elif self.businessObject['processData'][id] != value:
            self.businessObject['processData'][id] = value


    def getObject(self, key: str):
        objectsReturn = []
        #object = None
        try:
            if existsJsonPath(self.businessObject,['objects']):
                objList = self.businessObject['objects']
                if objList is not None:
                    objects = list(objList)
                    if objects is not None:
                        for obj in objects:
                            if obj['key'] == key:
                                objectsReturn.append(obj)
        except Exception as ex:
            print("Eccezione su getObject - {}".format(ex))
        return objectsReturn
    
    def uploadObject(self, object: Object):
        if 'objects' not in self.jsonComplete:
            self.jsonComplete['objects'] = []
        jsonObj = {
            "id" : object.id,
            "extension" : object.extension,
            "name" : object.name,
            "key" : object.key,
            "base64" : object.base64,
            "params" : []
        }
        self.jsonComplete['objects'].append(jsonObj)

    def complete(self, domain, taskId, priority=None, owner=None):
        json_string = self.jsonComplete #_to_json(self.jsonComplete)
        #print(json_string)
        responseComplete = requests.post(self.urlComplete.replace('{domain}', domain).replace('{taskId}', taskId), json=json_string)
        return responseComplete

def _to_json(obj):
    return json.dumps(obj, indent=4, default=lambda obj: obj.__dict__)


"""
"processData": {
    "additionalProp1": {},
    "additionalProp2": {},
    "additionalProp3": {}
  },
"""
