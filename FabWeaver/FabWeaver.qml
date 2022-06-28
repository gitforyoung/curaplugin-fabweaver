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
    width: 500 * screenScaleFactor
    height: 500 * screenScaleFactor
    minimumWidth: 400 * screenScaleFactor
    minimumHeight: 250 * screenScaleFactor

    Item
    {
        UM.I18nCatalog{id: catalog; name: "cura"}
        id: base
        property int columnWidth: Math.round((base.width / 2) - UM.Theme.getSize("default_margin").width)
        property int textMargin: UM.Theme.getSize("narrow_margin").width
        property string activeScriptName

        anchors.fill: parent

    }

    rightButtons: Cura.TertiaryButton
    {
        text: catalog.i18nc("@action:button", "Close")
        onClicked: dialog.accept()
    }
}