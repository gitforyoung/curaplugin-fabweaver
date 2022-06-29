
import os.path

from typing import cast

from cura.CuraApplication import CuraApplication
from UM.Application import Application
from UM.Extension import Extension
from UM.Logger import Logger
from UM.PluginRegistry import PluginRegistry

from . import Script

class FabWeaver(Extension):

    def __init__(self):
        super().__init__()

        self.setMenuName("fabWeaver Plugin")
        self.addMenuItem("Setting", self.showPopup)

        self.fab_window = None

        Application.getInstance().mainWindowChanged.connect(self._createDialogue)

        self._application = CuraApplication.getInstance()
        self._preferences = self._application.getPreferences()
        self._preferences.addPreference("FabWeaver/checkbox", False)

        Application.getInstance().getOutputDeviceManager().writeStarted.connect(self.execute)


    def showPopup(self):
        if self.fab_window is None:
            self._createDialogue()
            if self.fab_window is None:
                Logger.log("e", "Not creating window since the QML component failed to be created.")
                return
        self.fab_window.show()

    def _createDialogue(self):
        qml_file_path = os.path.join(cast(str, PluginRegistry.getInstance().getPluginPath("FabWeaver")), "FabWeaver.qml")
        self.fab_window = Application.getInstance().createQmlComponent(qml_file_path, {"manager":self})
        if self.fab_window is None:
            Logger.log("e", "Not creating window since the QML component failed to be created.")
            return
        Logger.log("d", "View created.")

    def execute(self, output_device) -> None:
        if self._preferences.getValue("FabWeaver/checkbox"):
            scene = Application.getInstance().getController().getScene()
            if not hasattr(scene, "gcode_dict"):
                return
            gcode_dict = getattr(scene, "gcode_dict")
            if not gcode_dict:
                return

            active_build_plate_id = CuraApplication.getInstance().getMultiBuildPlateModel().activeBuildPlate
            gcode_list = gcode_dict[active_build_plate_id]
            if not gcode_list:
                return

            if ";FABWEAVER" not in gcode_list[0]:
                try:
                    script = Script.Script()
                    gcode_list = script.execute(gcode_list)
                except Exception:
                    Logger.logException("e", "Exception in script.")
                gcode_list[0] += ";POSTPROCESSED\n"
                gcode_dict[active_build_plate_id] = gcode_list
                setattr(scene, "gcode_dict", gcode_dict)
            else:
                Logger.log("e", "Already processed")
