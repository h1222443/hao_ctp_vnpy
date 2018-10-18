import sys
import vtText
from vtFunction import jsonPathDict
from PyQt5 import QtWidgets


class SettingEditor(QtWidgets.QWidget):
    """配置编辑器"""

    # ----------------------------------------------------------------------
    def __init__(self, mainEngine, parent=None):
        """Constructor"""
        super(SettingEditor, self).__init__(parent)

        self.mainEngine = mainEngine
        self.currentFileName = ''

        self.initUi()

    # ----------------------------------------------------------------------
    def initUi(self):
        """初始化界面"""
        self.setWindowTitle(vtText.EDIT_SETTING)

        self.comboFileName = QtWidgets.QComboBox()
        self.comboFileName.addItems(jsonPathDict.keys())

        buttonLoad = QtWidgets.QPushButton(vtText.LOAD)
        buttonSave = QtWidgets.QPushButton(vtText.SAVE)
        buttonLoad.clicked.connect(self.loadSetting)
        buttonSave.clicked.connect(self.saveSetting)

        self.editSetting = QtWidgets.QTextEdit()
        self.labelPath = QtWidgets.QLabel()

        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.comboFileName)
        hbox.addWidget(buttonLoad)
        hbox.addWidget(buttonSave)
        hbox.addStretch()

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.editSetting)
        vbox.addWidget(self.labelPath)

        self.setLayout(vbox)

    # ----------------------------------------------------------------------
    def loadSetting(self):
        """加载配置"""
        self.currentFileName = str(self.comboFileName.currentText())
        filePath = jsonPathDict[self.currentFileName]
        self.labelPath.setText(filePath)

        with open(filePath) as f:
            self.editSetting.clear()

            for line in f:
                line = line.replace('\n', '')  # 移除换行符号
                line = line.decode('UTF-8')
                self.editSetting.append(line)

    # ----------------------------------------------------------------------
    def saveSetting(self):
        """保存配置"""
        if not self.currentFileName:
            return

        filePath = jsonPathDict[self.currentFileName]

        with open(filePath, 'w') as f:
            content = self.editSetting.toPlainText()
            content = content.encode('UTF-8')
            f.write(content)

    # ----------------------------------------------------------------------
    def show(self):
        """显示"""
        # 更新配置文件下拉框
        self.comboFileName.clear()
        self.comboFileName.addItems(jsonPathDict.keys())

        # 显示界面
        super(SettingEditor, self).show()



a = SettingEditor(mainEngine='hao')
a.show()
