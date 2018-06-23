import maya.cmds as cmds
import maya.mel as mel

mel.eval('global proc int maya2glTF_advanceExportProgressUI(string $stepName) {print($stepName+ "\\n"); return 0;}')
cmds.loadPlugin("maya2glTF")

selectedObjectNames = cmds.ls(selection=True)

selectedPaths = cmds.fileDialog2(fileMode=2)

for objName in selectedObjectNames:
	cmds.select(objName)
	cmds.maya2glTF(outputFolder=selectedPaths[0], sceneName=objName)
