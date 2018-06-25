import maya.cmds as cmds
import maya.mel as mel

mel.eval('global proc int maya2glTF_advanceExportProgressUI(string $stepName) {print($stepName+ "\\n"); return 0;}')
cmds.loadPlugin("maya2glTF")

selectedObjectNames = cmds.ls(selection=True)

selectedPaths = cmds.fileDialog2(fileMode=2)

for objName in selectedObjectNames:
	cmds.select(objName)
	pivot = cmds.getAttr(".rotatePivot")[0]
	cmds.setAttr(".translate", -pivot[0], -pivot[1], -pivot[2])
	cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)
	cmds.maya2glTF(outputFolder=selectedPaths[0], sceneName=objName, scaleFactor=0.01)
	cmds.setAttr(".translate", pivot[0], pivot[1], pivot[2])
	cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0, pn=1)