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

        self.label2 = QLabel("Control to :")
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


class QuantumGate(QComboBox):

    def __init__(self, parent=None):
        super(QuantumGate, self).__init__(parent)
        self.currentIndexChanged.connect(self.handle_selection)
        self.is_control = False

    def handle_selection(self, index):
        if self.objectName():
            selected_item = self.currentText()
            if self.is_control:
                idx = 0
                for _, x, y, to in self.parent().control_draw_list:
                    if (x == int(self.objectName()[4])
                            and y == int(self.objectName()[6])):
                        self.parent().gate_widget_list[to][y + 2].show()
                        del self.parent().control_draw_list[idx]

                        self.parent().QC.del_gate(to, y)
                        print("deleted")
                        break
                    idx += 1

            # IF control gated is choosen
            if selected_item == "Control":
                self.handle_control()
            # IF X,Y,Z,H gate is choosen
            elif selected_item in ["X", "Y", "Z", "H"]:
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

            self.parent().update()

    def handle_control(self):
        dialog = TwoInputDialog()
        dialog.exec_()
        self.parent().control_draw_list.append([
            dialog.return_value1,
            int(self.objectName()[4]),
            int(self.objectName()[6]),
            int(dialog.return_value2)
        ])
        self.is_control = True
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

    def __init__(self, input):
        super(QubitInput, self).__init__(input)
        self.currentIndexChanged.connect(self.handle_selection)

    def handle_selection(self, index):
        selected_item = self.currentText()
        if self.objectName():
            if selected_item not in ['0', '1']:
                print("none")
                return None
            self.parent().qubit_update(int(selected_item),
                                       int(self.objectName()[6]))


#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.

form_class = uic.loadUiType("test.ui")[0]


#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):

    qubit = qb.Qubit(QUBIT_NUM, 0)
    QC = circuit.QuantumCircuit(qubit, CIRCUIT_LEN)
    qubit_value = 0
    is_init = False

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.button_cal.clicked.connect(self.handle_button_cal)
        self.button_add.clicked.connect(self.handle_button_add)
        self.button_del.clicked.connect(self.handle_button_del)

        self.control_draw_list = []

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
                tmp.addItems(["", "X", "Y", "Z", "H", "Control"])
                tmp.setObjectName("gate" + str(i) + "_" + str(j))
                x += 110
                tmp_list.append(tmp)
            y += 100
            self.gate_widget_list.append(tmp_list)

            is_init = True

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))  # 펜 설정: 검은색, 두께 2, 실선

        # 시작점과 끝점 설정
        start_point = (50, 50)
        end_point = (200, 100)

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

    def handle_button_cal(self):
        self.result_0.setText(str(self.QC.calculate_qubit_state()[-1]))

    def handle_button_add(self):
        y = self.gate_widget_list[-1][0].pos().y() + 110
        label_no = len(self.gate_widget_list)
        tmp_list = []
        x = 200
        tmp_label = QLabel(self)
        tmp_label.setText(str(label_no))
        tmp_label.move(10, y + 20)
        tmp_list.append(tmp_label)

        tmp_input = QubitInput(self)
        tmp_input.addItems(["0", "1"])
        tmp_input.move(70, y + 20)
        tmp_input.setObjectName("input_" + str(label_no))
        tmp_list.append(tmp_input)

        for j in range(CIRCUIT_LEN):
            tmp = QuantumGate(self)
            tmp.resize(60, 60)
            tmp.move(x, y)
            tmp.addItems(["", "X", "Y", "Z", "Control"])
            tmp.setObjectName("gate" + str(label_no) + "_" + str(j))
            x += 110
            tmp_list.append(tmp)
        y += 100
        self.gate_widget_list.append(tmp_list)
        self.QC.add_circuit_row()

    def handle_button_del(self):
        if len(self.gate_widget_list) == 1:
            raise Exception("There is no Qubit to delete")
        for i in self.gate_widget_list[-1]:
            i.deleteLater()
        self.gate_widget_list = self.gate_widget_list[0:-1]
        self.QC.del_circuit_row()

    def qubit_update(self, value, idx):
        decimal_val = 2**idx
        if value == 0:
            self.qubit_value -= decimal_val
        else:
            self.qubit_value += decimal_val
        self.QC.change_qubit_value(self.qubit_value)


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