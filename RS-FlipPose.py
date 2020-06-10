from maya import cmds
import copy, re


def getObjAttrs(objName):
    objData = {
        'name': objName,
        't': list(cmds.getAttr(objName+'.translate')[0]),
        'r': list(cmds.getAttr(objName+'.rotate')[0]),
        's': list(cmds.getAttr(objName+'.scale')[0]),
        'userDefined': {},
    }
    
    userDefined = cmds.listAttr(objName, ud=True)

    if userDefined is not None:
        for key in userDefined:
            objData['userDefined'][key] = cmds.getAttr(objName+'.'+key)
       
    return objData
   
    
def updateObjAttrs(newData):
    cmds.setAttr(newData['name']+'.tx', newData['t'][0])
    cmds.setAttr(newData['name']+'.ty', newData['t'][1])
    cmds.setAttr(newData['name']+'.tz', newData['t'][2])
    cmds.setAttr(newData['name']+'.rx', newData['r'][0])
    cmds.setAttr(newData['name']+'.ry', newData['r'][1])
    cmds.setAttr(newData['name']+'.rz', newData['r'][2])
    cmds.setAttr(newData['name']+'.sx', newData['s'][0])
    cmds.setAttr(newData['name']+'.sy', newData['s'][1])
    cmds.setAttr(newData['name']+'.sz', newData['s'][2])
    
    for custom in newData['userDefined']:
         cmds.setAttr(newData['name']+'.'+custom, newData['userDefined'][custom])
    
    
def swopAttr(name1, name2):
    x1 = getObjAttrs(name1)
    x2 = getObjAttrs(name2)
    temp = copy.deepcopy(x1)
    
    x1['t'] = x2['t']
    x1['r'] = x2['r']
    x1['s'] = x2['s']
    x2['t'] = temp['t']
    x2['r'] = temp['r']
    x2['s'] = temp['s']
    
    for custom in  x1['userDefined']:
        x1['userDefined'][custom] = x2['userDefined'][custom]
        x2['userDefined'][custom] = temp['userDefined'][custom]
        
    updateObjAttrs(x1)
    updateObjAttrs(x2)


def flipSideCon(name):
    data = getObjAttrs(name)
    data['t'][0] *=-1
    data['r'][1] *=-1
    data['r'][2] *=-1
    updateObjAttrs(data)
    
    


objs = cmds.ls(selection=True)

sidesCon = {}
midCon = []

# Group Side or Mid Controller
for obj in objs:
    r = re.match(r'^[RrLl]_', obj)
    if r:
        sidesCon.setdefault(obj[2:], []).append(obj)
    else:
        midCon.append(obj)
# Flip Side Controlles
for key in sidesCon:
    if len(sidesCon[key]) == 2:
        swopAttr(sidesCon[key][0], sidesCon[key][1])
        flipSideCon(sidesCon[key][0])
        flipSideCon(sidesCon[key][1])
        
# Flip Mid Controlles
for key in midCon:
    flipSideCon(key)
        
    
#swopTRS(objs[0],objs[1])
#flipSideCon(objs[0])

    
    