import os.path

from pyipcore.ui_utils import *
from pyipcore.ui_main.fileitem import QFileSlot, QFixWidthLabel
from pyipcore.ui_main.tablexp_page._tools import *



class QExcelExampleShower(QWidget):
    def __init__(self, fixed_width, fixed_height, parent=None):
        super(QExcelExampleShower, self).__init__(parent)
        self.setFixedSize(fixed_width, fixed_height)
        self._font = LBL_FONT_MINI
        self.bias:tuple[int, int] = (0, 0)
        self.target:tuple[int, int] = (1, 1)
        self.delta:tuple[int, int] = (0, 0)

    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        pen0 = QPen(LT_BLACK, 1, Qt.SolidLine)
        pen1 = QPen(Qt.darkGray, 1, Qt.SolidLine)
        painter.setPen(pen0)
        painter.setBrush(QBrush(LT_JLCYELLOW))

        painter.drawRect(0, 0, self.width(), self.height())

        # # top left
        # painter.drawLine(1, 1, self.width(), 0)
        # painter.drawLine(1, 1, 0, self.height())
        #
        # # top 'A' left '1'
        # painter.setPen(pen1)
        # painter.setFont(self._font)
        # painter.drawText(20, 15, 'A')
        # painter.drawText(5, 30, '1')

class QCheckedListWidget(QWidget):
    def __init__(self, parent=None):
        super(QCheckedListWidget, self).__init__(parent)
        self.sheets = []    # 存储名称
        self._checks = []   # 存储复选框
        self._widgets = []
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.list_layout = QVBoxLayout()
        self.layout.addLayout(self.list_layout)
        self.layout.addStretch(1)

        self.setMinimumHeight(300)
        self.setMinimumWidth(200)

    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)

        painter.setPen(QPen(LT_BLACK, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.white))

        painter.drawRect(0, 0, self.width(), self.height())

        super().paintEvent(a0)

    def clear(self):
        for widget in self._widgets:
            widget.deleteLater()
        _ = self.list_layout
        self.list_layout = QVBoxLayout()
        self.layout.removeItem(_)
        self.layout.insertLayout(0, self.list_layout)

        self._widgets.clear()
        self.sheets.clear()
        self._checks.clear()

    def addItem(self, name, checked=False):
        layout = QHBoxLayout()
        lbl = QLabel(name)
        layout.addWidget(lbl)
        layout.addStretch(1)
        check = QCheckBox()
        check.setChecked(checked)
        layout.addWidget(check)
        self._checks.append(check)
        self.sheets.append(name)
        self._widgets.append(lbl)
        self._widgets.append(check)
        self.list_layout.addLayout(layout)

    @property
    def selects(self) -> list[bool]:
        return [c.isChecked() for c in self._checks]


class QSheetsListWidget(QCheckedListWidget):
    def __init__(self, excel_path=None, parent=None):
        super(QSheetsListWidget, self).__init__(parent)
        self._excel_path = excel_path
        if excel_path: self._load_sheets()

    def _load_sheets(self):
        xls = pd.ExcelFile(self._excel_path)
        for sheet in xls.sheet_names:
            self.addItem(sheet, checked=True)

    @property
    def path(self):
        return self._excel_path

    @path.setter
    def path(self, path):
        self._excel_path = path
        self.clear()
        if os.path.exists(path):
            self._load_sheets()



class QExcelFileHeaderCollector(QWidget):
    def __init__(self, parent=None):
        super(QExcelFileHeaderCollector, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)
        h0, h1 = QHBoxLayout(), QHBoxLayout()
        v0 = QVBoxLayout()
        self._fileslot = QFileSlot(formats=['xlsx'], size=80)
        self._fileslot.fileChanged.connect(self._on_file_changed)
        h0.addStretch(1)
        h0.addWidget(self._fileslot)
        h0.addStretch(1)
        v0.addLayout(h0)
        self._fxlbl = QFixWidthLabel(108)
        self._fxlbl.setText('IO Table\n(.xlsx)')
        self._fxlbl.setAlignment(Qt.AlignCenter)
        self._fxlbl.setFont(LBL_FONT)
        v0.addWidget(self._fxlbl)
        h1.addLayout(v0)
        self._shower = QExcelExampleShower(140, 160)
        h1.addWidget(self._shower)
        self._layout.addLayout(h1)

        l0, l1, l2 = QHBoxLayout(), QHBoxLayout(), QHBoxLayout()
        lbl = QLabel('Bias   : (')
        lbl.setFixedWidth(60)
        lbl.setFont(LBL_FONT)
        l0.addWidget(lbl)
        self._bias_x = QSpinBox()  # > 0
        self._bias_x.setMinimum(0)
        self._bias_x.setMaximum(100)
        self._bias_x.setValue(0)
        self._bias_x.setFont(LBL_FONT)
        self._bias_x.valueChanged.connect(self._on_value_changed)
        l0.addWidget(self._bias_x)
        lbl = QLabel(',')
        lbl.setFixedWidth(12)
        lbl.setFont(LBL_FONT)
        l0.addWidget(lbl)
        self._bias_y = QSpinBox()
        self._bias_y.setMinimum(0)
        self._bias_y.setMaximum(100)
        self._bias_y.setValue(0)
        self._bias_y.setFont(LBL_FONT)
        self._bias_y.valueChanged.connect(self._on_value_changed)
        l0.addWidget(self._bias_y)
        lbl = QLabel(')')
        lbl.setFixedWidth(12)
        lbl.setFont(LBL_FONT)
        l0.addWidget(lbl)
        self._layout.addLayout(l0)

        lbl = QLabel('Target:(')
        lbl.setFixedWidth(60)
        lbl.setFont(LBL_FONT)
        l1.addWidget(lbl)
        self._target_x = QSpinBox()
        self._target_x.setMinimum(1)
        self._target_x.setMaximum(100)
        self._target_x.setValue(1)
        self._target_x.setFont(LBL_FONT)
        self._target_x.valueChanged.connect(self._on_value_changed)
        l1.addWidget(self._target_x)
        lbl = QLabel(',')
        lbl.setFixedWidth(12)
        lbl.setFont(LBL_FONT)
        l1.addWidget(lbl)
        self._target_y = QSpinBox()
        self._target_y.setMinimum(1)
        self._target_y.setMaximum(100)
        self._target_y.setValue(1)
        self._target_y.setFont(LBL_FONT)
        self._target_y.valueChanged.connect(self._on_value_changed)
        l1.addWidget(self._target_y)
        lbl = QLabel(')')
        lbl.setFixedWidth(12)
        lbl.setFont(LBL_FONT)
        l1.addWidget(lbl)
        self._layout.addLayout(l1)

        lbl = QLabel('Delta : (')
        lbl.setFixedWidth(60)
        lbl.setFont(LBL_FONT)
        l2.addWidget(lbl)
        self._delta_x = QSpinBox()
        self._delta_x.setMinimum(0)
        self._delta_x.setMaximum(100)
        self._delta_x.setValue(0)
        self._delta_x.setFont(LBL_FONT)
        self._delta_x.valueChanged.connect(self._on_value_changed)
        l2.addWidget(self._delta_x)
        lbl = QLabel(',')
        lbl.setFixedWidth(12)
        lbl.setFont(LBL_FONT)
        l2.addWidget(lbl)
        self._delta_y = QSpinBox()
        self._delta_y.setMinimum(0)
        self._delta_y.setMaximum(100)
        self._delta_y.setValue(0)
        self._delta_y.setFont(LBL_FONT)
        self._delta_y.valueChanged.connect(self._on_value_changed)
        l2.addWidget(self._delta_y)
        lbl = QLabel(')')
        lbl.setFixedWidth(12)
        lbl.setFont(LBL_FONT)
        l2.addWidget(lbl)
        self._layout.addLayout(l2)

        self._sheets = QSheetsListWidget()
        # 设置strengthen
        self._layout.addWidget(self._sheets, 2)


    def _on_value_changed(self, *args):
        self._shower.bias = (self._bias_x.value(), self._bias_y.value())
        self._shower.target = (self._target_x.value(), self._target_y.value())
        self._shower.delta = (self._delta_x.value(), self._delta_y.value())
        self._shower.update()

    def _on_file_changed(self, path):
        print(path)
        self._sheets.path = path



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QExcelFileHeaderCollector()
    w.show()
    sys.exit(app.exec_())


