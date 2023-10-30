"""Python test module"""

import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsScene, QGraphicsView, QGraphicsItem
from PyQt5.QtCore import QRectF, Qt

class DraggableRectItem(QGraphicsRectItem):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('design.ui', self)


    #     self.scene = QGraphicsScene(self)
    #     self.graphicsView = QGraphicsView(self.scene, self.centralwidget)
    #     self.graphicsView.setGeometry(10, 10, 780, 580)

    #     # Add draggable items
    #     self.scene.addItem(DraggableRectItem(20, 20, 100, 50))
    #     self.scene.addItem(DraggableRectItem(150, 150, 100, 50))

    #     # Add lines
    #     self.lines = [
    #         QRectF(0, 0, 801, 20),
    #         QRectF(0, 20, 801, 20),
    #         QRectF(0, 40, 801, 20),
    #         QRectF(0, 60, 801, 20)
    #     ]

    # def checkItemOnLine(self):
    #     for item in self.scene.items():
    #         if isinstance(item, DraggableRectItem):
    #             for line in self.lines:
    #                 if item.sceneBoundingRect().intersects(line):
    #                     self.onItemDroppedOnLine(item, line)
    #                     break

    # def onItemDroppedOnLine(self, item, line):
    #     print(f"Item dropped on line: {line}")
    #     # Implement your hook logic here

    # def mouseReleaseEvent(self, event):
    #     super(MainWindow, self).mouseReleaseEvent(event)
    #     self.checkItemOnLine()

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())