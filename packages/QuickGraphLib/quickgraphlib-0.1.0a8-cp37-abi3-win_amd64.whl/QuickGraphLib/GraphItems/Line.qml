// SPDX-FileCopyrightText: Copyright (c) 2024 Refeyn Ltd and other QuickGraphLib contributors
// SPDX-License-Identifier: MIT

import QtQuick
import QtQuick.Shapes as QQS
import QuickGraphLib as QuickGraphLib

/*!
    \qmltype Line
    \inqmlmodule QuickGraphLib.GraphItems
    \inherits QtQuick::Shapes::ShapePath
    \brief Displays a line graph.

    Graph a line using a list of X,Y points. The style of the line can be adjusted using the \l {ShapePath::strokeColor} {strokeColor} and \l {ShapePath::strokeWidth} {strokeWidth} properties.

    \qml
        GraphArea {
            id: grapharea
            viewRect: Qt.rect(-20, -1.1, 760, 2.2)

            Line {
                dataTransform: grapharea.dataTransform
                path: Helpers.linspace(0, 720, 100).map(x => Qt.point(x, Math.sin(x / 180 * Math.PI)))
                strokeColor: "red"
                strokeWidth: 2
            }
        }
    \endqml
*/

QQS.ShapePath {
    id: root

    /*!
        Must be assigned the data transform of the graph area this axis is paired to.

        \sa GraphArea::dataTransform
    */

    required property matrix4x4 dataTransform

    /*!
        Points to graph. Each point is a \l point (containing x and y coordinates) in the data space.
    */
    required property var path

    capStyle: QQS.ShapePath.RoundCap
    fillColor: "transparent"
    joinStyle: QQS.ShapePath.RoundJoin

    PathPolyline {
        path: QuickGraphLib.Helpers.mapPoints(root.path, root.dataTransform)
    }
}
