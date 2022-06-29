# Description:  This plugin generates and inserts code including a image of the
#               slices part.

from UM.Mesh.MeshWriter import MeshWriter
from UM.MimeTypeDatabase import MimeTypeDatabase, MimeType
from cura.Snapshot import Snapshot
from cura.Utils.Threading import call_on_qt_thread
from UM.Logger import Logger
from UM.Scene.SceneNode import SceneNode #For typing.
from UM.PluginRegistry import PluginRegistry
from UM.i18n import i18nCatalog
from cura.Settings.ExtruderManager import ExtruderManager
catalog = i18nCatalog("cura")

import re
from io import StringIO, BufferedIOBase #To write the g-code to a temporary buffer, and for typing.
from typing import cast, List


def getValue(line, key, default=None):
    if key not in line:
        return default
    else:
        subPart = line[line.find(key) + len(key):]
        m = re.search('^-?[0-9]+\\.?[0-9]*', subPart)
        #if m is None:
        #    pass
        #return default
    try:
        return float(m.group(0))
    except:
        return default



class FabWriter(MeshWriter):
    def __init__(self):
        Logger.log("i", "[FabWriter] - initiated.")
        super().__init__(add_to_recent_files = False)
        self._snapshot = None
        MimeTypeDatabase.addMimeType(
            MimeType(
                name = "text/fabweaver-g-code",
                comment = "gcode for fabWeaver",
                suffixes = ["gcode"]
            )
        )

    @call_on_qt_thread    
    def write(self, stream: BufferedIOBase, nodes: List[SceneNode], mode = MeshWriter.OutputMode.BinaryMode) -> bool:
        Logger.log("i", "[FabWriter] - Start to write.")
        if mode != MeshWriter.OutputMode.TextMode:
            Logger.log("e", "FabWriter does not support non-text mode.")
            self.setInformation(catalog.i18nc("@error:not supported", "FabWriter does not support non-text mode."))
            return False
        gcode_textio = StringIO() #We have to convert the g-code into bytes.
        gcode_writer = cast(MeshWriter, PluginRegistry.getInstance().getPluginObject("GCodeWriter"))
        success = gcode_writer.write(gcode_textio, None)
        
        if not success: 
            self.setInformation(gcode_writer.getInformation())
            return False
        result = self.modify(gcode_textio.getvalue())
        stream.write(result)
        Logger.log("i", "[FabWriter] - Writing finished.")
        return True

    def modify(self, in_data):
        Logger.log("i", "[FabWriter] - Run modify.")
        temp_in_data = in_data
        time_data = self.makeFabweaverCode(temp_in_data)
        return time_data
    
    def makeFabweaverCode(self, gcode_data):
        Logger.log("i", "[FabWriter] - Start to make fab code.")
        lines = gcode_data.split("\n")
        for line in lines:
            if line.startswith(";TIME:"): # ;TIME:7088
                line_index = lines.index(line)
                split_string = (re.split(":", line))[1] # 7088
                m, s = divmod(int(split_string), 60) # 7088/60 몫, 나머지
                h, m = divmod(m, 60) # 7088/60/60 몫, 나머지
                lines[line_index] = ";ESTIMATION_TIME: [{:d}:{:02d}:{:02d}]".format(h, m, s) # ;TIME:7088 => ;ESTIMATION_TIME: [1:58:08]
                continue
            elif line.startswith(";MINX:"):
                line_index = lines.index(line)
                x_min = lines[line_index][6:]
                y_min = lines[line_index+1][6:]
                z_min = lines[line_index+2][6:]
                x_max = lines[line_index+3][6:]
                y_max = lines[line_index+4][6:]
                z_max = lines[line_index+5][6:]
                x_dim = round(float(x_max) - float(x_min),1)
                y_dim = round(float(y_max) - float(y_min),1)
                z_dim = round(float(z_max) - float(z_min),1)
                total_dim = ";DIMENSION: [" + str(x_dim) + ":" + str(y_dim) + ":" + str(z_dim) + "]" # ;DIMENSION: [49.2:190.7:51.1]
                lines[line_index+5] = lines[line_index+5] + "\n" + total_dim
                break
        
        for line in lines:
            line_index = lines.index(line)
            if line.startswith(";Filament used:"): # ;Filament used: 3.09775m, 1.89364m
                split_string = re.split("[:,] ", line) # ";Filament used", "3.09775m", "1.89364m"
                try:
                    t0_filament_number = float((re.split("m", split_string[1]))[0]) # 3.09775
                except:
                    t0_filament_number = 0
                try:
                    t1_filament_number = float((re.split("m", split_string[2]))[0]) # 1.89364
                except:
                    t1_filament_number = 0
                t0_flag = "T" if t0_filament_number!=0 else "F"
                t1_flag = "T" if t1_filament_number!=0 else "F"
                if t0_flag == "T":
                    material_0 = ExtruderManager.getInstance().getActiveExtruderStacks()[0].getMetaDataEntry("GUID")
                    material_used_string = ";MATERIAL_CARTRIDGE_0: [" + str(material_0) + "]\n" # ;MATERIAL_CARTRIDGE_0: [ABS]
                if t1_flag == "T":
                    material_1 = ExtruderManager.getInstance().getActiveExtruderStacks()[1].getMetaDataEntry("GUID")
                    material_used_string = material_used_string + ";MATERIAL_CARTRIDGE_1: [" + str(material_1) + "]" # ;MATERIAL_CARTRIDGE_1: [RSA]
                nozzle_used_string = "\n;CARTRIDGE_USED_STATE: [" + t0_flag + ":" + t1_flag + "]" # ;CARTRIDGE_USED_STATE: [3.09775:1.89364]
                lines[line_index] = line + nozzle_used_string + "\n" + material_used_string
                if str(material_0) != "[PLA]":
                    lines[0] = ";CHAMBER_ON 70 0\n" + lines[0]
                break

        return_data = "\n".join(lines)
        
        return return_data