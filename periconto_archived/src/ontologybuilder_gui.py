# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ontologybuilder_gui.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!
import os, sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

from graph import Graph
from rdflib import Graph as RDFGraph
import pprint

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1291, 808)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBoxTree = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxTree.setGeometry(QtCore.QRect(20, 60, 811, 551))

        self.groupBoxTree.setObjectName("groupBoxTree")
        self.treeWidget = QtWidgets.QTreeWidget(self.groupBoxTree)
        self.treeWidget.setGeometry(QtCore.QRect(10, 31, 791, 511))
        self.treeWidget.setColumnCount(0)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.header().setCascadingSectionResizes(False)
        self.groupBoxEditor = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxEditor.setGeometry(QtCore.QRect(140, 630, 451, 91))

        self.groupBoxEditor.setObjectName("groupBoxEditor")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBoxEditor)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 401, 51))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushAddSubclass = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushAddSubclass.setObjectName("pushAddSubclass")
        self.horizontalLayout.addWidget(self.pushAddSubclass)
        self.pushAddClass = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushAddClass.setObjectName("pushAddClass")
        self.horizontalLayout.addWidget(self.pushAddClass)
        self.pushRemoveNode = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushRemoveNode.setObjectName("pushRemoveNode")
        self.horizontalLayout.addWidget(self.pushRemoveNode)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 0, 171, 31))

        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        # set the combobox with items
        self.comboBox.addItem("load")
        self.comboBox.addItem("visualize")
        self.comboBox.addItem("save")
        self.comboBox.addItem("create")
        self.comboBox.addItem("select")
        self.verticalLayout.addWidget(self.comboBox)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(870, 150, 391, 291))

        self.plainTextEdit.setObjectName("plainTextEdit")
        self.elucidationLabel = QtWidgets.QLabel(self.centralwidget)
        self.elucidationLabel.setGeometry(QtCore.QRect(990, 120, 141, 20))
        self.elucidationLabel.setObjectName("elucidationLabel")
        self.pushAddElucidation = QtWidgets.QPushButton(self.centralwidget)
        self.pushAddElucidation.setGeometry(QtCore.QRect(1010, 460, 101, 23))
        self.pushAddElucidation.setObjectName("pushAddElucidation")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1291, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # call the combobox custom methods
        # self.comboBox.activated[str].connect(self.on_select)
        # self.comboBox.activated[str].connect(self.onVisualizeSelected)
        # self.comboBox.activated[str].connect(self.onLoadSelected)
        # #self.comboBox.activated[str].connect(self.on_visualize)
        # #self.comboBox.activated[str].connect(self.on_create)
        # self.comboBox.activated[str].connect(self.onSaveSelected)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PERICONTO 0.1"))
        self.groupBoxTree.setTitle(_translate("MainWindow", "ontology tree"))
        self.groupBoxEditor.setTitle(_translate("MainWindow", "ontology editor"))
        self.pushAddSubclass.setText(_translate("MainWindow", "add subclass"))
        self.pushAddClass.setText(_translate("MainWindow", "add class"))
        self.pushRemoveNode.setText(_translate("MainWindow", "remove node"))
        self.comboBox.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.comboBox.setCurrentText(_translate("MainWindow", "<select>"))
        self.comboBox.setItemText(0, _translate("MainWindow", "<select>"))
        self.comboBox.setItemText(1, _translate("MainWindow", "load ontology"))
        self.comboBox.setItemText(2, _translate("MainWindow", "visualize ontology"))
        self.comboBox.setItemText(3, _translate("MainWindow", "create ontology"))
        self.comboBox.setItemText(4, _translate("MainWindow", "save ontology"))
        self.elucidationLabel.setText(_translate("MainWindow", "selection elucidation"))
        self.pushAddElucidation.setText(_translate("MainWindow", "add changes"))



    # testing the combobox options
    # def on_select(self, val):
    #     if val == '<select>':
    #         message = 'please select an option from the dropdown list'
        
    #     else:
    #         message = 'you have selected the option: ' + val

    #     print(message)

    # #   open ontolog
    # def onVisualizeSelected(self, val):
    #     if val == 'visualize ontology':
    #         self.process = QtCore.QProcess()
    #         self.process.start("python", ['ontovis.py'])

    
    #     #pass

    # # custom method for loading an existing ontology
    # def onLoadSelected(self, val):
    #     if val == 'load ontology' :
    #         options = QFileDialog.Options()
    #         options |= QFileDialog.DontUseNativeDialog
    #         fileName = QFileDialog.getOpenFileName(None,"Load Ontology", '../coatingOntology', "","Turtle files (*.ttl)", options=options)
    #         # with open(fileName[0], 'r') as f:
    #         #     file_text = f.read()
    #         # print('this is file name', fileName[0])
    #          # print(file_text)

    #         # g1 = RDFGraph()
    #         # g1.parse(fileName[0], format="turtle")
    #         # print('Number of tuples in the graph: ', len(g1))
    #         # # for stmt in g:
    #         # #     pprint.pprint(stmt)
    #         # for s,p,o in g1:
    #         #     print('these are ontology triples...', s,p,o)

            
    #         g2 = Graph()
    #         with open(fileName[0]) as fg:
    #             tupsList = [tuple(line.split()) for line in fg]
    #             for t in tupsList:
    #                 if t:
    #                     g2.append((t))
            
    #         # for s, p, o in g2.match(None, None, None):
    #         #     print((s,p,o))

    #         triplesList = [(o,s) for s, _, o in g2.match(None, 'subClassOf', None)]
    #         #print(triplesList)
    #         triplesDict = {}
    #         for o, s in triplesList:
    #             try:
    #                 triplesDict[o].append(s)
    #             except KeyError:
    #                 triplesDict[o] = [s]
               

    #         for key, value in triplesDict.items():
    #             root = self.horizontalLayoutWidget(self.treeWidget, [key])
    #             #print (root)
    #             subTree = []
    # #print(subTree)
    #             for val in value:
    #                 subTree.append(val)
    #                 item = self.horizontalLayout([val])
    #                 root.addChild(item)
               
            


    # def onSaveSelected(self, val):
    #     if val == 'save ontology':
    #         options = QFileDialog.Options()
    #         options |= QFileDialog.DontUseNativeDialog
    #         fileName = QFileDialog.getSaveFileName(None,"Save Ontology","","","Turtle files (*.ttl)", options=options)
    #         if fileName:
    #             print(fileName)
        

    # loaded_ontology = onLoadSelected()
    # print('ontology loaded ..', loaded_ontology) 
    # def loadAndParse(loaded_ontology):
    #     g = RDFGraph()
    #     g.parse(loaded_ontology, format="ttl")
    #     for s,p,o in g.triples(None, None, None):
    #         print(s,p,o)

    # loadAndParse

    # # custom method for visualizing a ontology (opens up ontovis tool window)
    # def on_visualize(self):
    #     self.visualizemessage = 'visualize selected'
    #     print(self.visualizemessage)

    # # custom method for creating a ontology from scratch
    # def on_create(self):
    #     self.createmessage = 'create selected'
    #     print(self.createmessage)

    # # custom method for saving the ontology (activated only when there is some change)
    # def on_save(self):
    #     self.savemessage = 'save selected'
    #     print(self.savemessage)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

