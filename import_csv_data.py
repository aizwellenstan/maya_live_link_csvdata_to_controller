import csv
import maya.cmds
import sys
def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)
# add_path('D:\workspace\td\mocap_facial\modules')
python_version = '%d.%d' % sys.version_info[:2]
print(python_version)

# yaml
add_path(r'I:\script\bin\td\3rd\lib\python\%s' % python_version)
import yaml
path = "D:\\workspace\\td\\MyState_15_ARKit_iPhone.csv"
file = open(path)
reader = csv.reader(file)

header = next(reader)
data = [row for row in reader]

import maya.cmds as cmds

import random

def cleanData():
    global data
    newData = []
    lastTimeCode = 0
    lastData = []
    for d in data:
        timeCode = int(d[0][-3:])
        if d[1] == "0": continue
        if lastTimeCode > 0:
            if timeCode - lastTimeCode > 1:
                for i in range(0, timeCode - lastTimeCode):
                    newData.append(lastData)
        newData.append(d)
        lastData = d
        lastTimeCode = timeCode
    data = newData

def selectNurbsCurve(nurbsCurveName):
    curve_transforms = [cmds.listRelatives(i, p=1, type='transform')[0] for i
    in cmds.ls(type='nurbsCurve', o=1, r=1, ni=1)]

    for curve in curve_transforms:
        name = curve.split(":")
        if nurbsCurveName == name[1]:
            cmds.select(curve)

# selectNurbsCurve("UpEyeLid_R")

def read_yaml(path):
    u"""Read data from path as yaml format.
    """
    with open(path) as f:
        return yaml.load(f)

def setKeyframes(key, reverse=False):
    obj = cmds.ls(selection=True)[0]

    frame = 0
    cmds.setKeyframe(obj + '.translateY', value=0, time=0)
    frame += 1
    multiplier = 2
    for d in data:
        if len(d) < 3: continue
        dataDict = {}
        translateDict = {}
        translateDict['EyeBlinkLeft'] = '.translateY'
        if reverse:
            dataDict['EyeBlinkLeft'] = float(d[2])*multiplier * -1
        else:
            dataDict['EyeBlinkLeft'] = float(d[2])*multiplier

        translateDict['EyeLookDownLeft'] = '.translateY'
        dataDict['EyeLookDownLeft'] = float(d[3])*multiplier * -1

        translateDict['EyeLookInLeft'] = '.translateX'
        dataDict['EyeLookInLeft'] = float(d[4])*multiplier * -1

        translateDict['EyeLookOutLeft'] = '.translateX'
        dataDict['EyeLookOutLeft'] = float(d[4])*multiplier

        translateDict['EyeLookUpLeft'] = '.translateY'
        dataDict['EyeLookUpLeft'] = float(d[3])*multiplier

        translateDict['EyeSquintLeft'] = '.translateY'
        dataDict['EyeSquintLeft'] = float(d[3])*multiplier

        translateDict['EyeWideLeft'] = '.translateY'
        dataDict['EyeWideLeft'] = float(d[3])*multiplier


        translateDict['EyeBlinkRight'] = '.translateY'
        if reverse:
            dataDict['EyeBlinkRight'] = float(d[2])*multiplier * -1
        else:
            dataDict['EyeBlinkRight'] = float(d[2])*multiplier

        translateDict['EyeLookDownRight'] = '.translateY'
        dataDict['EyeLookDownRight'] = float(d[3])*multiplier * -1

        translateDict['EyeLookInRight'] = '.translateX'
        dataDict['EyeLookInRight'] = float(d[4])*multiplier

        translateDict['EyeLookOutRight'] = '.translateX'
        dataDict['EyeLookOutRight'] = float(d[4])*multiplier * -1

        translateDict['EyeLookUpRight'] = '.translateY'
        dataDict['EyeLookUpRight'] = float(d[3])*multiplier

        translateDict['EyeSquintRight'] = '.translateY'
        dataDict['EyeSquintRight'] = float(d[3])*multiplier

        translateDict['EyeWideRight'] = '.translateY'
        dataDict['EyeWideRight'] = float(d[3])*multiplier


        translateDict['JawForward'] = '.translateX'
        dataDict['JawForward'] = float(d[3])*multiplier

        translateDict['JawLeft'] = '.rotateY'
        dataDict['JawLeft'] = float(d[3])*multiplier * -1

        translateDict['JawRight'] = '.rotateY'
        dataDict['JawRight'] = float(d[3])*multiplier

        translateDict['JawOpen'] = '.translateY'
        dataDict['JawOpen'] = float(d[3])*multiplier

        translateDict['BrowDownLeft'] = '.translateY'
        dataDict['BrowDownLeft'] = float(d[3])*multiplier * -1

        translateDict['BrowDownRight'] = '.translateY'
        dataDict['BrowDownRight'] = float(d[3])*multiplier * -1

        translateDict['BrowInnerUp'] = '.translateY'
        dataDict['BrowInnerUp'] = float(d[3])*multiplier

        translateDict['BrowOuterUpLeft'] = '.translateY'
        dataDict['BrowOuterUpLeft'] = float(d[3])*multiplier

        translateDict['BrowOuterUpRight'] = '.translateY'
        dataDict['BrowOuterUpRight'] = float(d[3])*multiplier

        translateDict['NoseSneerLeft'] = '.translateY'
        dataDict['NoseSneerLeft'] = float(d[3])*multiplier

        translateDict['NoseSneerRight'] = '.translateY'
        dataDict['NoseSneerRight'] = float(d[3])*multiplier
        print(d[0], key)


        
        if "Squint" in key:
            if key == 'EyeSquintLeft':
                if dataDict['EyeSquintLeft'] < dataDict['EyeBlinkLeft']:
                    cmds.setKeyframe(obj + translateDict[key], value=dataDict[key], time=frame)
            elif key == 'EyeSquintRight':
                if dataDict['EyeSquintRight'] < dataDict['EyeBlinkRight']:
                    cmds.setKeyframe(obj + translateDict[key], value=dataDict[key], time=frame)
        else:
            cmds.setKeyframe(obj + translateDict[key], value=dataDict[key], time=frame)
        
        frame += 1

def insertKey():
    mapping_path = "D:\\workspace\\td\\mocap_facial\\yaml\\blendshape_mapping.yaml"
    mapping_rules = read_yaml(mapping_path)
    print(mapping_rules)

    print(len(data))
    cleanData()
    print(len(data))
    for key, value in  mapping_rules.iteritems():
        controllers = mapping_rules.get(key, None)
        for mapping_kwargs in controllers:
            controller = mapping_kwargs.pop('controller')
            selectNurbsCurve(controller)
            reverse = controller.startswith('Dn')
            setKeyframes(key, reverse)
    
insertKey()
