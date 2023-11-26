"""
Quantum Circuit & Entanglement simulator by PYQT 

This code generate GUI using PYQT module for quantum circuit. It can calculate result of quantum circuit and decide which part is entangled. 
This code include module [qubit.qubit, qubit.gates, quantum_circuit] 

Author: Chanwoo Moon
Email: ixora990919@gmail.com
Website: https://github.com/tlemsl/Entanglement_visualizerg


"""

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPainter, QPen, QColor, QFont
from PyQt5.QtCore import Qt, QPoint
import circuit.quantum_circuit as circuit
import qubit.qubit as qb
import qubit.gates as qg

QUBIT_NUM = 2
CIRCUIT_LEN = 10


class TwoInputDialog(QDialog):
    """Class inherits QDialog in QWidget

    This class is custum QDialog class for generation of control gate 

    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Control gate")
        self.layout = QVBoxLayout()

        self.label1 = QLabel("Gate type:")
        self.input1 = QComboBox()
        self.input1.addItem('X')
        self.input1.addItem('Y')
        self.input1.addItem('Z')
        self.input1.addItem('H')

        self.label2 = QLabel("Target:")
        self.input2 = QLineEdit()

        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.input1)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.input2)

        self.button = QPushButton("Confirm")
        self.button.clicked.connect(self.get_input_values)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

        self.return_value1 = None
        self.return_value2 = None

    def get_input_values(self):
        self.return_value1 = self.input1.currentText()
        self.return_value2 = self.input2.text()
        self.accept()

class CellViewer(QDialog):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Qubit state")
        layout = QVBoxLayout()
        self.label = QLabel(text)
        layout.addWidget(self.label)
        self.setLayout(layout)

class QuantumGate(QComboBox):
    """Class inherits QComboBox in QWidget

    This class is custum QComboBox class for management quantum gate in the circuit.     

    """

    def __init__(self, parent=None):
        super(QuantumGate, self).__init__(parent)
        self.currentIndexChanged.connect(self.handle_selection)
        self.is_control = False
        font = self.font()
        font.setPointSize(20)  # Change the font size here
        self.setFont(font)
        self.is_active = False

    def handle_selection(self, index):
        ''''handle function when gate is selected on the box'''
        if self.objectName():
            selected_item = self.currentText()
            if self.is_control:
                idx = 0
                for _, x, y, to in self.parent().control_draw_list:
                    if (x == int(self.objectName()[4])
                            and y == int(self.objectName()[6])):
                        self.parent().gate_widget_list[to][y + 2].show()
                        self.parent().gate_widget_list[to][y + 2].is_active = False
                        self.is_active = False
                        del self.parent().control_draw_list[idx]

                        self.parent().QC.del_gate(to, y)
                        print("deleted")
                        break
                    idx += 1

            # IF control gated is choosen
            if selected_item == "⊙":
                self.handle_control()
            # IF X,Y,Z,H gate is choosen
            elif selected_item in ["X", "Y", "Z", "H"]:
                self.is_active = True
                if selected_item == "X":
                    self.parent().QC.add_gate(
                        int(self.objectName()[4]), int(self.objectName()[6]),
                        qg.X(QUBIT_NUM, int(self.objectName()[4])))
                elif selected_item == "Y":
                    self.parent().QC.add_gate(
                        int(self.objectName()[4]), int(self.objectName()[6]),
                        qg.Y(QUBIT_NUM, int(self.objectName()[4])))
                elif selected_item == "Z":
                    self.parent().QC.add_gate(
                        int(self.objectName()[4]), int(self.objectName()[6]),
                        qg.Z(QUBIT_NUM, int(self.objectName()[4])))
                elif selected_item == "H":
                    self.parent().QC.add_gate(
                        int(self.objectName()[4]), int(self.objectName()[6]),
                        qg.H(QUBIT_NUM, int(self.objectName()[4])))
            else:
                self.parent().QC.del_gate(int(self.objectName()[4]),
                                          int(self.objectName()[6]))
                self.is_active = False

            self.parent().update()


    def handle_control(self):
        '''handle function for control gate'''
        dialog = TwoInputDialog()
        dialog.exec_()
        if not dialog.return_value2.isnumeric() or (int(dialog.return_value2) >= QUBIT_NUM) or int(dialog.return_value2)==int(self.objectName()[4]):
            QMessageBox.warning(self, 'Warning', 'Please check your input', QMessageBox.Ok)
            self.setCurrentIndex(0)
            return None


        self.parent().control_draw_list.append([
            dialog.return_value1,
            int(self.objectName()[4]),
            int(self.objectName()[6]),
            int(dialog.return_value2)
        ])
        self.is_control = True
        self.is_active = True
        self.parent().gate_widget_list[int(dialog.return_value2)][int(self.objectName()[6])+2].is_active = True
        if dialog.return_value1 == "X":
            self.parent().QC.add_gate(
                int(dialog.return_value2), int(self.objectName()[6]),
                qg.X(QUBIT_NUM, int(dialog.return_value2),
                     int(self.objectName()[4])))
        elif dialog.return_value1 == "Y":
            self.parent().QC.add_gate(
                int(dialog.return_value2), int(self.objectName()[6]),
                qg.Y(QUBIT_NUM, int(dialog.return_value2),
                     int(self.objectName()[4])))
        elif dialog.return_value1 == "Z":
            self.parent().QC.add_gate(
                int(dialog.return_value2), int(self.objectName()[6]),
                qg.Z(QUBIT_NUM, int(dialog.return_value2),
                     int(self.objectName()[4])))
        elif dialog.return_value1 == "H":
            self.parent().QC.add_gate(
                int(dialog.return_value2), int(self.objectName()[6]),
                qg.H(QUBIT_NUM, int(dialog.return_value2),
                     int(self.objectName()[4])))

        print(self.parent().control_draw_list)


class QubitInput(QComboBox):
    """Class inherits QComboBox in QWidget

    This class is custum QComboBox class for Qubit initial input.     

    """

    def __init__(self, input):
        super(QubitInput, self).__init__(input)
        self.currentIndexChanged.connect(self.handle_selection)

    def handle_selection(self, index):
        '''handle function when initial value is selected on qubit input box'''
        self.parent().qubit_update()


# connect UI to pyqt
form_class = uic.loadUiType("/home/qtuser/Entanglement_visualizer/src/gui/design.ui")[0]


# Class for initial window
class WindowClass(QMainWindow, form_class):

    qubit = qb.Qubit(QUBIT_NUM, 0)
    QC = circuit.QuantumCircuit(qubit, CIRCUIT_LEN)
    is_init = False

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowTitle('Quantum Circuit Simulator')

        self.button_cal.clicked.connect(self.handle_button_cal)
        self.button_add.clicked.connect(self.handle_button_add)
        self.button_del.clicked.connect(self.handle_button_del)

        self.tableWidget.setRowCount(CIRCUIT_LEN+1)  # 행 수 설정
        self.tableWidget.setColumnCount(2)  # 열 수 설정
        self.tableWidget.setItem(0, 0, QTableWidgetItem("State"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("Qubit"))
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 250)
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.cellClicked.connect(self.showCellContent)

        # control gate list
        self.control_draw_list = []
        # entangled qubit list
        self.entangled_draw_list = []
        # result of qubit
        self.qubit_cal_list = []


        y = 80
        label_no = 0
        self.gate_widget_list = []
        for i in range(QUBIT_NUM):
            tmp_list = []
            x = 200
            tmp_label = QLabel(self)
            tmp_label.setText(str(label_no))
            tmp_label.move(10, y + 20)
            tmp_list.append(tmp_label)
            label_no += 1

            tmp_input = QubitInput(self)
            tmp_input.addItems(["0", "1"])
            tmp_input.move(70, y + 20)
            tmp_input.setObjectName("input_" + str(i))
            tmp_list.append(tmp_input)

            for j in range(CIRCUIT_LEN):
                tmp = QuantumGate(self)
                tmp.resize(60, 60)
                tmp.move(x, y)
                tmp.addItems(["", "X", "Y", "Z", "H", "⊙"])
                tmp.setObjectName("gate" + str(i) + "_" + str(j))
                x += 110
                tmp_list.append(tmp)
            y += 100
            self.gate_widget_list.append(tmp_list)

            is_init = True

    def paintEvent(self, event):
        '''Paint function

        1. Generate line for control gate
        2. Visualize Entanglement with line
        
        '''
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))  # 펜 설정: 검은색, 두께 2, 실선

        # 시작점과 끝점 설정
        start_point = (0, 0)
        end_point = (0, 0)

        for gate, x, y, to in self.control_draw_list:
            position1 = self.gate_widget_list[x][y + 2].pos()
            position2 = self.gate_widget_list[to][y + 2].pos()
            start_point = (position1.x() + 30, position1.y() + 30)
            end_point = (position2.x() + 30, position2.y() + 30)
            painter.drawLine(start_point[0], start_point[1], end_point[0],
                             end_point[1])
            painter.setFont(QFont('Arial', 20))
            painter.drawText(end_point[0] - 10, end_point[1] + 10, gate)
            self.gate_widget_list[to][y + 2].hide()
        
        # entanlement visualize
        colors = [
            QColor(255, 0, 0),  # Red
            QColor(0, 255, 0),  # Green
            QColor(0, 0, 255),  # Blue
            QColor(255, 255, 0),  # Yellow
            QColor(255, 0, 255),  # Magenta
            QColor(0, 255, 255)  # Cyan
        ]
        qubit_colors = [-1 for i in range(QUBIT_NUM)]

        color_index = 0
        for state_idx, ent_set_list in enumerate(self.entangled_draw_list):
            for qubit_list in ent_set_list:
                if state_idx>0:
                    if qubit_list in self.entangled_draw_list[state_idx-1]:
                        for qbt in qubit_list:
                            painter.setPen(QPen(colors[qubit_colors[qbt]], 10, Qt.SolidLine))
                            position = self.gate_widget_list[qbt][state_idx+2].pos()
                            painter.drawLine(position.x()+30, position.y()+27,position.x()+130,position.y()+27)
                    else:
                        color_index += 1
                        for qbt in qubit_list:
                            painter.setPen(QPen(colors[color_index], 10, Qt.SolidLine))
                            position = self.gate_widget_list[qbt][state_idx+2].pos()
                            painter.drawLine(position.x()+30, position.y()+27,position.x()+130,position.y()+27)
                            qubit_colors[qbt] = color_index
                else:
                    color_index += 1
                    for qbt in qubit_list:
                        painter.setPen(QPen(colors[color_index], 10, Qt.SolidLine))  
                        position = self.gate_widget_list[qbt][state_idx+2].pos()
                        painter.drawLine(position.x()+30, position.y()+27,position.x()+130,position.y()+27)
                        qubit_colors[qbt] = color_index



        

    def handle_button_cal(self):
        '''Handle function when click calculate button'''
        self.qubit_cal_list = self.QC.calculate_qubit_state()
        self.entangled_draw_list = []

        for idx, qubit_cal in enumerate(self.qubit_cal_list):
            # will be changed when Qubit code fixed
            self.entangled_draw_list.append(qubit_cal.entangled())
            # update qubit result at result table
            self.tableWidget.setItem(idx+1, 0, QTableWidgetItem(str(idx)))
            self.tableWidget.setItem(idx+1, 1, QTableWidgetItem(str(qubit_cal)))

        
        print("entangle",self.qubit_cal_list[-1].entangled())

        self.result_0.setText(str(self.qubit_cal_list[-1]))
        print("check",self.entangled_draw_list)
        self.update()



    def handle_button_add(self):
        '''Handle function when click add qubit button'''
        global QUBIT_NUM
        if QUBIT_NUM >= 7:
            QMessageBox.warning(self, 'Error', 'Qubit number exceed max', QMessageBox.Ok)
            return None
        QUBIT_NUM += 1
        y = self.gate_widget_list[-1][0].pos().y() + 80
        label_no = len(self.gate_widget_list)
        tmp_list = []
        x = 200
        tmp_label = QLabel(self)
        tmp_label.setText(str(label_no))
        tmp_label.move(10, y + 20)
        tmp_label.show()
        tmp_list.append(tmp_label)

        tmp_input = QubitInput(self)
        tmp_input.addItems(["0", "1"])
        tmp_input.move(70, y + 20)
        tmp_input.setObjectName("input_" + str(label_no))
        tmp_input.show()
        tmp_list.append(tmp_input)

        for j in range(CIRCUIT_LEN):
            tmp = QuantumGate(self)
            tmp.resize(60, 60)
            tmp.move(x, y)
            tmp.show()

            tmp.addItems(["", "X", "Y", "Z", "H", "⊙"])
            tmp.setObjectName("gate" + str(label_no) + "_" + str(j))
            x += 110
            tmp_list.append(tmp)
        self.gate_widget_list.append(tmp_list)
        self.QC.add_circuit_row()


    def handle_button_del(self):
        '''Handle function when click del qubit button''' 
        global QUBIT_NUM
        if QUBIT_NUM <= 1:
            QMessageBox.warning(self, 'Error', 'There is no Qubit to delete', QMessageBox.Ok)
            return None
        for tmp_gate in self.gate_widget_list[-1][2:]:
            if tmp_gate.is_active:
                QMessageBox.warning(self, 'Error', 'Please delete gate first', QMessageBox.Ok)
                return None
       

        QUBIT_NUM -= 1


        for i in self.gate_widget_list[-1]:
            i.deleteLater()
        self.gate_widget_list = self.gate_widget_list[0:-1]
        self.QC.del_circuit_row()

    def qubit_update(self):
        '''Function to update qubit value when input qubit value is changed'''
        qubit_value = 0
        for idx, row in enumerate(self.gate_widget_list):
            if int(row[1].currentText()):
                qubit_value += 2**idx

        self.QC.change_qubit_value(qubit_value)

    def showCellContent(self,row, col):
        '''fucntion for table view'''
        item = self.tableWidget.item(row, col)
        if item is not None:
            text = item.text()
            dialog = CellViewer(text, self)
            dialog.exec_()



# Genreate quantum circuit class instance

# Hyper parameter of circuit ( it will be changed to dynamic varibale at next commit)

# Initialize Qubit

if __name__ == "__main__":
    #QApplication : 프로그램을 실행시켜주는 클래스

    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
