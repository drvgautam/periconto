import sys
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt5.QtWidgets import QApplication, QMenuBar, QGridLayout, QAction, qApp, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt


class Ontovis(QWidget):

    def __init__(self):
        super().__init__()

        # layout = QGridLayout()
        # self.setLayout(layout)

        # # create menu
        # menubar = QMenuBar()
        # layout.addWidget(menubar, 0, 0)
        # actionFile = menubar.addMenu("File")
        # actionFile.addAction("New")
        # actionFile.addAction("Open")
        # actionFile.addAction("Save")
        # actionFile.addSeparator()
        # actionFile.addAction("Quit")
        # menubar.addMenu("Edit")
        # menubar.addMenu("View")
        # menubar.addMenu("Help")

        self.initUI()

    def initUI(self):

        # vbox = QVBoxLayout(self)
        layout = QGridLayout()
        self.setLayout(layout)
        menubar = QMenuBar()
        layout.addWidget(menubar, 0, 0)
        #menubar = layout.addWidget(QMenuBar(self))

        actionFile = menubar.addMenu("File")
        actionFile.addAction("New")
        actionFile.addAction("Open")
        actionFile.addAction("Save")
        actionFile.addSeparator()
        actionFile.addAction("Quit")
        menubar.addMenu("Help")



        self.webEngineView = QWebEngineView()
        self.loadPage()

        # button_open_action = QAction("Open",self)
        # button_open_action.triggered.connect(self.loadPage)
        #button_action2.setCheckable(True)

        # quit_action = QAction('Quit', self)
        # quit_action.triggered.connect(self.quitActionClicked)


        layout.addWidget(self.webEngineView)

        self.setLayout(layout)
        
        #self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle('OntoVis')
        self.showMaximized()

    def loadPage(self):
  
        with open('../nx.html', 'r') as f:

            html = f.read()
            self.webEngineView.setHtml(html)

    
    # def quitActionClicked(self):
    #     qApp.quit()

# def main():

#     app = QApplication(sys.argv)
#     ex = Ontovis()
#     sys.exit(app.exec_())


if __name__ == '__main__':
    # main()
    app = QApplication(sys.argv)
    ex = Ontovis()
    sys.exit(app.exec_())