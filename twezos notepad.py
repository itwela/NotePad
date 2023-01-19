import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, \
    QPushButton, QLabel, QPlainTextEdit, QStatusBar, QToolBar, \
        QVBoxLayout, QAction, QFileDialog, QMessageBox, QMenu
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFontDatabase, QIcon, QKeySequence, QPixmap
from PyQt5.QtPrintSupport import QPrintDialog

class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        #I learned that if your using windows, to get that icon to show up near the title -
        # you use self.WindowIcon(QIcon('str')) however -
        # if you are using a mac, the icon will only show if you use -
        # self.setWindowTitle('str) ('str' is the filename)
        self.setWindowFilePath('notepad.ico')
        self.screen_width, self.screen_height = self.geometry().width(), self.geometry().height()
        self.resize(self.screen_width * 1.1, self.screen_height * 1.1)

        self.filterTypes = 'Text Document (*.txt)'
        
        self.path = None

        fixedFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedFont.setPointSize(12)

        mainLayout = QVBoxLayout()

        # editor
        self.editor = QPlainTextEdit()
        self.editor.setFont(fixedFont)
        mainLayout.addWidget(self.editor)

        # statusBar
        self.statusBar = self.statusBar()
        
        # app container
        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

        #----------------------------------
        # File Menus
        #----------------------------------
        file_menu = self.menuBar().addMenu('&File')

        #----------------------------------
        # File ToolBar
        #----------------------------------
        file_toolbar = QToolBar('File')
        file_toolbar.setIconSize(QSize(60, 60))
        self.addToolBar(Qt.BottomToolBarArea, file_toolbar)

        """
        open, save, saveAs
        """

        '''open_file_action = QAction(QIcon('./icons/file_open.ico'), 'Open File...', self)
        open_file_action.setStatusTip('Open File')
        open_file_action.setShortcut(QKeySequence.Open)
        open_file_action.triggered.connect(self.file_open)'''

        open_file_action = self.create_action(self, './icons/file_open.ico', 'Open File', 'Open file', self.file_open)
        open_file_action.setStatusTip('Open File')
        open_file_action.setShortcut(QKeySequence.Open)
        open_file_action.triggered.connect(self.file_open)

        save_file_action = self.create_action(self, './icons/save.ico', 'Save File', 'Save file', self.file_save)
        save_file_action.setShortcut(QKeySequence.Save)

        save_fileAs_action = self.create_action(self, './icons/save_as.ico', 'Save File As', 'Save file as', self.file_saveAs)
        save_fileAs_action.setShortcut(QKeySequence('ctrl+Shift+S'))

        file_menu.addActions([open_file_action, save_file_action, save_fileAs_action])
        file_toolbar.addActions([open_file_action, save_file_action, save_fileAs_action])

        # Print Action (Print Document)
        print_action = self.create_action(self, './icons/printer.ico', 'Print File', 'Print file', lambda: print('print document'))
        print_action.setShortcut(QKeySequence.Print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        #----------------------------------
        # Edit Menu
        #----------------------------------
        edit_menu = self.menuBar().addMenu('&Edit')
        


        #----------------------------------
        # Edit Toolbar
        #----------------------------------
        edit_toolbar = QToolBar('Edit')
        edit_toolbar.setIconSize(QSize(60,60))
        self.addToolBar(Qt.BottomToolBarArea, edit_toolbar)

        # Undo, Redo Actions
        undo_action = self.create_action(self, './icons/undo.ico', 'Undo', 'Undo', self.editor.undo)
        undo_action.setShortcut(QKeySequence.Undo)

        redo_action = self.create_action(self, './icons/redo.ico', 'Redo', 'Redo', self.editor.redo)
        redo_action.setShortcut(QKeySequence.Redo)

        edit_menu.addActions([undo_action, redo_action])
        edit_toolbar.addActions([undo_action, redo_action])

        edit_menu.addSeparator()
        edit_toolbar.addSeparator()

        

        self.update_title()

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Open file',
            '',
            self.filterTypes
        )

        text = self.editor.toPlainText()

        if not path:
            return
        else:
            try:
                with open(path, 'r') as f:
                    text = f.read()
                    f.close()
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()
    
    def file_save(self):
        if self.path is None:
            self.file_saveAs()
        else:
            try:
                text = self.editor.toPlainText()
                with open(self.path, 'w') as f:
                    f.write(text)
                    f.close()
            except Exception as e:
                self.dialog_message(str(e))

    def file_saveAs(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save file as',
            '',
            self.filterTypes
        )

        text = self.editor.toPlainText()

        if not path:
            return
        else:
            try:
                with open(path, 'w') as f:
                    f.write(text)
                    f.close()
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path = path
                self.update_title()


    #def is a method
    def update_title(self):
        self.setWindowTitle('{0} - TwezopadX'.format(os.path.basename(self.path) if self.path else 'Untitled'))

    def dialog_message(self, message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def create_action(self, parent, icon_path, action_name, set_status_tip, triggered_method)  :
        action = QAction(QIcon(icon_path), action_name, parent)
        action.setStatusTip(set_status_tip)
        action.triggered.connect(triggered_method)
        return action

app = QApplication(sys.argv)
notePade = AppDemo()
notePade.show()
sys.exit(app.exec_())
