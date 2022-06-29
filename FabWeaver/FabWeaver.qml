import QtQuick 2.2
import QtQuick.Controls 2.15
import QtQml.Models 2.15 as Models
import QtQuick.Layouts 1.1
import QtQuick.Window 2.2

import UM 1.5 as UM
import Cura 1.0 as Cura

UM.Dialog //Creates a modal window that pops up above the interface.
{
    id: dialog

    title: catalog.i18nc("@title:window", "fabWeaver")
    width: 380 * screenScaleFactor
    height: 300 * screenScaleFactor
    minimumWidth: 380 * screenScaleFactor
    maximumWidth: 380 * screenScaleFactor
    minimumHeight: 200 * screenScaleFactor
    maximumHeight: 200 * screenScaleFactor

    Item
    {
        UM.I18nCatalog{id: catalog; name: "cura"}
        id: base
        property int columnWidth: Math.round(base.width - UM.Theme.getSize("default_margin").width)
        property int textMargin: UM.Theme.getSize("narrow_margin").width
        property string activeScriptName

        anchors.fill: parent
        
        Column
        {
            id: settingsPanel
            width: base.columnWidth
            height: parent.height
            spacing:base.textMargin

            UM.Label
            {
                id: header
                text: catalog.i18nc("@label", "Settings")
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.leftMargin: base.textMargin
                font: UM.Theme.getFont("large_bold")
                elide: Text.ElideRight
            }

            UM.Label
            {
                id: guidetext
                text: catalog.i18nc("@label", "Check the box to generate a gcode file for fabWeaver.")
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.leftMargin: base.textMargin
                elide: Text.ElideRight
            }

            RowLayout
            {
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.leftMargin: base.textMargin
                UM.CheckBox
                {
                    text: catalog.i18nc("@option:check", "Activate!")
                    checked: boolCheck(UM.Preferences.getValue("FabWeaver/checkbox"))
                    onCheckedChanged: UM.Preferences.setValue("FabWeaver/checkbox", checked)
                }
            }
        }


    }

    rightButtons: Cura.TertiaryButton
    {
        text: catalog.i18nc("@action:button", "Close")
        onClicked: dialog.accept()
    }
}