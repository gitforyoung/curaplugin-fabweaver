# import configparser  # The script lists are stored in metadata as serialised config files.
# import importlib.util
# import io  # To allow configparser to write to a string.
import os.path
# import pkgutil
# import sys
from typing import Dict, Type, TYPE_CHECKING, List, Optional, cast

# from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot

from UM.Application import Application
from UM.Extension import Extension
from UM.Logger import Logger
from UM.PluginRegistry import PluginRegistry
# from UM.Resources import Resources
# from UM.Trust import Trust, TrustBasics
# from UM.i18n import i18nCatalog
# from cura import ApplicationMetadata
# from cura.CuraApplication import CuraApplication

class FabWeaver(Extension):
    ##  Creates an instance of this extension. This is basically the starting
    #   point of your code.
    #
    #   This is called by the register() function in __init__.py, which gets
    #   called during plug-in loading. That all happens before the splash screen
    #   even appears, so this code needs to be efficient. Also, be aware, that
    #   many things have not been loaded yet at this point.
    def __init__(self):
        super().__init__()
        #A typical use of this constructor is to register some function to be
        #called upon some event in Uranium, or to add a menu item. In this case,
        #we will do both.


        ## Creating a menu item. ##
        #An extension can add several menu items. They all get placed under one header. This sets the title of that header.
        self.setMenuName("Example Extension")

        #We'll add one item that says hello to the user.
        self.addMenuItem("Say hello", self.sayHello) #When the user clicks the menu item, the sayHello function is called.

        #Lazy-load the window. Create it when we first want to say hello.
        self.hello_window = None

        ## Reacting to an event. ##
        Application.getInstance().mainWindowChanged.connect(self._createDialogue) #When the main window is created, log a message.

    ##  Creates a small dialogue window that says hello to the user.
    def sayHello(self):
        if not self.hello_window: #Don't create more than one.
            self.hello_window = self._createDialogue()
        self.hello_window.show()


    ##  Adds a message to the log, as an example of how to listen to events.
    def logMessage(self):
        Logger.log("i", "This is an example log message.")

    ##  Creates a modal dialogue.
    def _createDialogue(self):
        #Create a QML component from the Hello.qml file.
        qml_file_path = os.path.join(cast(str, PluginRegistry.getInstance().getPluginPath("FabWeaver")), "FabWeaver.qml")
        # path = os.path.join(cast(str, PluginRegistry.getInstance().getPluginPath("PostProcessingPlugin")), "PostProcessingPlugin.qml")
        component = Application.getInstance().createQmlComponent(qml_file_path, {"manager":self})
       
        return component
