import maya.cmds as cmds
import maya.mel as mel
import pymel.util.path as path

windowID = "Maya2glTF Export"

def killJobs():
    # Kill any existing selection changed jobs
    jobs = cmds.scriptJob(listJobs=True)
    
    for job in jobs:
        if job.find("maya2glTFExportWindow.update()") != -1:
            jobID = int(job.split(":")[0])
            cmds.scriptJob( kill=jobID)              

def getDefaultOutputFolder():
    return path(path(cmds.file(q=True, loc=True)).dirname() + "/../Export").abspath().replace("\\", "/")
    
def getSelectionLabel(selectedObjectNames, selectedObjectCount):
    if selectedObjectCount == 0:
        return "No object selected"
    elif selectedObjectCount == 1:
        return "{0} selected".format(selectedObjectNames[0])
    else: 
        return "{0} objects selected".format(selectedObjectCount)

class Maya2glTFExportWindow:
    def __init__(self):
        self.selectedObjectNames = []
        self.selectedObjectCount = 0
        self.render()
        self.update()
        self.selectionChangedJob = cmds.scriptJob(e=["SelectionChanged", "maya2glTFExportWindow.update()"])    
        
    def render(self):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)
        
        cmds.window(windowID, closeCommand="maya2glTFExportWindow.dispose()")
    
        cmds.columnLayout()
        
        self.selectedObjectsText = cmds.text(label="No object selected")
        
        self.scaleFactorGroup = cmds.floatFieldGrp(label="Scale Factor", value1=0.01, precision=2)
        
        self.exportAnimationGroup = cmds.checkBoxGrp(label="Export Animation")

        self.frameRateGroup = cmds.intFieldGrp(label="Frame Rate", value1=24)
        
        self.gameExporterPresetGroup = cmds.optionMenuGrp(label="Game Exporter Preset:", adjustableColumn=2)
        
        self.outputFolderGroup = cmds.textFieldButtonGrp(label="Output Folder", text=getDefaultOutputFolder(), buttonLabel="Browse", buttonCommand="maya2glTFExportWindow.onBrowseOutputFolder()")
        
        cmds.button(label="Export", command="maya2glTFExportWindow.export()")
        
        cmds.showWindow()
            
            
    def update(self):
        self.selectedObjectNames = cmds.ls(selection=True)
        self.selectedObjectCount = len(self.selectedObjectNames)
        selectionLabel = getSelectionLabel(self.selectedObjectNames, self.selectedObjectCount)
        cmds.text(self.selectedObjectsText, edit=True, label=selectionLabel)
        
        self.presetNodes = cmds.ls(type="gameFbxExporter")
        cmds.optionMenuGrp(self.gameExporterPresetGroup, q=True)
        for presetNode in self.presetNodes:
            presetName = cmds.getAttr(presetNode+".presetName")
            cmds.menuItem(label=presetName)
            
    def onBrowseOutputFolder(self):
        outputFolder = cmds.textFieldButtonGrp(self.outputFolderGroup, query=True, text=True)
        selectedPaths = cmds.fileDialog2(fileMode=2, startingDirectory=outputFolder)

        if selectedPaths != None:
            cmds.textFieldButtonGrp(self.outputFolderGroup, edit=True, text=selectedPaths[0])
            
    def export(self):
        outputFolder = cmds.textFieldButtonGrp(self.outputFolderGroup, query=True, text=True)
        params = '-outputFolder "{0}"\n'.format(outputFolder)

        exportAnimation = cmds.checkBoxGrp(self.exportAnimationGroup, q=True, value1=True)

        if exportAnimation:
            frameRate = cmds.intFieldGrp(self.frameRateGroup, q=True, value1=True)
            params += "-animationClipFrameRate {0}\n".format(frameRate)

            presetIndex = cmds.optionMenuGrp(self.gameExporterPresetGroup, q=True, select=True) - 1
            print(presetIndex)
            presetName = self.presetNodes[presetIndex]
            numAnimClips = cmds.getAttr(presetName + ".animClips", size=True)
            for animClipIdx in range(numAnimClips):
                name = cmds.getAttr("{0}.animClips[{1}].animClipName".format(presetName, animClipIdx))
                start = cmds.getAttr("{0}.animClips[{1}].animClipStart".format(presetName, animClipIdx))
                end = cmds.getAttr("{0}.animClips[{1}].animClipEnd".format(presetName, animClipIdx))
                params += '-animationClipName "{0}" -animationClipStartTime {1} -animationClipEndTime {2}\n'.format(name, start, end)
        
        if self.selectedObjectCount == 0:
            mel.eval('maya2glTF -sceneName "{0}"\n'.format(self.selectedObjectNames[0]) + params)
        else:
            for objName in self.selectedObjectNames:
                cmds.select(objName)
                pivot = cmds.getAttr(".rotatePivot")[0]
                cmds.setAttr(".translate", -pivot[0], -pivot[1], -pivot[2])
                cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)
                mel.eval('maya2glTF -sceneName "{0}"\n'.format(objName) + params)
                cmds.setAttr(".translate", pivot[0], pivot[1], pivot[2])
                cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)
                cmds.select(objName)    
    
    def dispose(self):
        killJobs()
               

cmds.loadPlugin("maya2glTF", quiet=True)
cmds.loadPlugin("gameFbxExporter", quiet=True)

maya2glTFExportWindow = Maya2glTFExportWindow()


