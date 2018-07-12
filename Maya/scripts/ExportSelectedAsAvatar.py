import maya.cmds

mel.eval('global proc int maya2glTF_advanceExportProgressUI(string $stepName) {print($stepName+ "\\n"); return 0;}')
cmds.loadPlugin("maya2glTF")
cmds.loadPlugin("gameFbxExporter")

selectedObjectNames = cmds.ls(selection=True)

nodes = cmds.ls(type="gameFbxExporter")

params = 'maya2glTF -outputFolder "{0}" -sceneName "{1}" -animationClipFrameRate {2}\n'.format("../Export", selectedObjectNames[0], 24)

for nodeName in nodes:
    print(nodeName)
    numAnimClips = cmds.getAttr(nodeName + ".animClips", size=True)
    for animClipIdx in range(numAnimClips):
        name = cmds.getAttr("{0}.animClips[{1}].animClipName".format(nodeName, animClipIdx))
        start = cmds.getAttr("{0}.animClips[{1}].animClipStart".format(nodeName, animClipIdx))
        end = cmds.getAttr("{0}.animClips[{1}].animClipEnd".format(nodeName, animClipIdx))
        params += '-animationClipName "{0}" -animationClipStartTime {1} -animationClipEndTime {2}\n'.format(name, start, end)

print(params)
        