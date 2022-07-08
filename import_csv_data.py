import csv
import maya.cmds as cmds
import sys
import os
from os import listdir
from os.path import isfile, join

def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)
# add_path('D:\workspace\td\mocap_facial\modules')
python_version = '%d.%d' % sys.version_info[:2]
print(python_version)

# yaml
add_path(r'I:\script\bin\td\3rd\lib\python\%s' % python_version)
import yaml

def cleanData(data):
    newData = []
    lastTimeCode = 0
    lastData = []
    for d in data:
        if len(d) < 1: continue
        timeCode = int(d[0][-3:])
        if d[1] == "0": continue
        # if lastTimeCode > 0:
        if lastTimeCode > 1000:
            if timeCode - lastTimeCode > 1:
                for i in range(0, timeCode - lastTimeCode):
                    newData.append(lastData)
        newData.append(d)
        lastData = d
        lastTimeCode = timeCode
    return newData
    
def createAnimationArr(data):
    multiplier = 2
    animationArr = []
    for d in data:
        if len(d) < 3: continue
        dataDict = {}
        translateDict = {}
        translateDict['EyeBlinkLeft'] = '.translateY'
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

        animationDict = {}
        animationDict['data'] = dataDict
        animationDict['translate'] = translateDict
        animationArr.append(animationDict)
    return animationArr

def selectNurbsCurve(nurbsCurveName):
    curve_transforms = [cmds.listRelatives(i, p=1, type='transform')[0] for i
    in cmds.ls(type='nurbsCurve', o=1, r=1, ni=1)]

    for curve in curve_transforms:
        if nurbsCurveName == curve:
            return curve
    return ""

# selectNurbsCurve("UpEyeLid_R")

def read_yaml(path):
    u"""Read data from path as yaml format.
    """
    with open(path) as f:
        return yaml.load(f)

def setKeyframes(obj, data, key, reverse=False):
    val = 1
    if reverse: val = -1

    frame = 0
    cmds.setKeyframe(obj + '.translateY', value=0, time=0)
    frame += 1

    animationArr = []
    for d in data:
        translateDict = d['translate']
        dataDict = d['data']
        
        if "Squint" in key:
            if key == 'EyeSquintLeft':
                if dataDict['EyeSquintLeft'] < dataDict['EyeBlinkLeft']:
                    cmds.setKeyframe(obj + translateDict[key], value=dataDict[key], time=frame)
            elif key == 'EyeSquintRight':
                if dataDict['EyeSquintRight'] < dataDict['EyeBlinkRight']:
                    cmds.setKeyframe(obj + translateDict[key], value=dataDict[key], time=frame)
        else:
            cmds.setKeyframe(obj + translateDict[key], value=dataDict[key]*val, time=frame)
        
        frame += 1

def getData(path):
    data = []
    with open(path) as f:
        reader = csv.reader(f)
        header = next(reader)
        data = [row for row in reader]
       
    return data

def insertKey():
    mapping_path = "D:/workspace/td/mocap_facial/yaml/blendshape_mapping.yaml"
    facialPath = "J:/test_project/work/progress/mcp/satou_test/facial/facialData"
    # rigFile = 'J:/test_project/work/document/from_client/BIJJ/tianYuanMoAvA/rig/hx_pub_char_tianYuanMoAvA_rig_v006.ma'
    rigFile = 'J:/test_project/work/progress/mcp/satou_test/rig/hx_pub_char_tianYuanMoAvA_rig_v006.ma'
    outPutPath = 'J:/test_project/work/progress/mcp/satou_test/facial/maya'

    mapping_rules = read_yaml(mapping_path)
    onlyfiles = [f for f in listdir(facialPath) if isfile(join(facialPath, f))]

    for f in onlyfiles:
        filePath = facialPath+'/'+f
        data = getData(filePath)
        data = cleanData(data)
        animationArr = createAnimationArr(data)
        fileName = os.path.splitext(f)[0]
        print(fileName)
        cmds.file(rigFile, open=True, force=True)
        for key, value in  mapping_rules.iteritems():
            controllers = mapping_rules.get(key, None)
            for mapping_kwargs in controllers:
                controller = mapping_kwargs['controller']
                curve = selectNurbsCurve(controller)
                print(curve)
                reverse = controller.startswith('Dn')
                setKeyframes(curve, animationArr, key, reverse)
        cmds.file(rename=outPutPath+'/'+fileName+".ma")
        cmds.file(save=True, type="mayaAscii")
