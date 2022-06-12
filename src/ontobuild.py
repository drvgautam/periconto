#!/usr/local/bin/python3


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ontologybuilder_gui import Ui_MainWindow

import os, sys

from graph import Graph
from rdflib import Graph as RDFGraph
import pprint

class OntobuilderUI(QMainWindow):
    def __init__(self):
        super(OntobuilderUI, self). __init__()
        # uic.loadUi("ontologybuilder_gui.ui", self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ontology_graph = None

        #set ontology_root as None. Currently, ontology root node is named cfo (Coating Formulation Ontology)
        # cfo is is currently set as a prefix in ontology file
        # while creating ontology from scratch,self.ontology_root is assigned 'cfo' as root node 
        # subsequent classes and subclasses are added to create ontology  

        #TODO a user given name is set as root node of ontology tree
       
        self.ontology_root = None

        #self.show()

        self.UiComboBox()

    def UiComboBox(self):
        # self.comboBox = QComboBox(self)
        # comboBox_action_list = ["load", "visualize", "save", "create", "select"]
        # self.comboBox.addItems(comboBox_action_list)

        self.ui.comboBox.activated[str].connect(self.onSelectSelected)
        self.ui.comboBox.activated[str].connect(self.onVisualizeSelected)
        self.ui.comboBox.activated[str].connect(self.onLoadSelected)
        #self.comboBox.activated[str][str].connect(self.on_visualize)
        self.ui.comboBox.activated[str][str].connect(self.onCreateSelected)
        self.ui.comboBox.activated[str].connect(self.onSaveSelected)

        

        self.ui.treeWidget.itemClicked.connect(self.onItemClicked)
        # self.ui.pushAddClass.clicked.connect(self.onAddSubclassClicked)
        
        
        self.ui.pushAddClass.setEnabled(False)
        self.ui.pushAddSubclass.setEnabled(False)
        self.ui.pushRemoveNode.setEnabled(False)


    

    #   open ontolog
    

    
        #pass

  
    # def print_test(self):
    #     return 'This is working fine!'

    # method to load a ontology from a file and create ontology graph base on graph utility provided by Thomas
    def create_ontograph(self, onto_filename):
        ontoGraph = Graph()
        with open(onto_filename) as fg:
            tupsList = [tuple(line.split()) for line in fg]
            for t in tupsList:
                if t:
                    ontoGraph.append((t))
            
            # for s, p, o in g2.match(None, None, None):
            #     print((s,p,o))

        return ontoGraph






    # method to creare a nested dictionary from the list of tuples
    # 
    '''
    myTuplesList = [('a', 'b'), ('a','c'), ('a', 'd'), 
                    ('c', 'e'), ('c', 'f'), ('c','g'), 
                    ('c', 'h'), ('c', 'i'),
                    ('c', 'j'), ('k','l'), ('k', 'm'), 
                    ('k', 'n')]
    nestedDict = {
               'a':{
                   'b': {},
                   'c': {'e', 'f'},
                   'd': {}
                'k': {
                    'l': {}, 
                    'm': {},  
                    'n': {}
                     }
                     }
              }
    '''

    def nested_dictionary(self, data):
        nested_dict, master_dict = {}, {}
        for a, b in data:
            if a not in master_dict:
                nested_dict[a] = master_dict[a] = {}
            master_dict[a][b] = master_dict[b] = {}
        return nested_dict

    # method to create coating ontology tree usingg QTreeWidget
    '''
    in args
            : nested dictionary
            :QTreeWidget (in our case, treeWidget object name from the Ui_MainWindow())
    out: a visual view of the tree in a PyQt Widget
    '''
    def build_tree(self, data=None, parent=None):
        # initialize root of the tree
        for key, value in data.items():
            item = QTreeWidgetItem(parent)
            item.setText(0, key)
            if isinstance(value, dict):
                self.build_tree(data=value, parent=item)

    def make_treewidget(self, data, widget):
        widget.clear()
        self.build_tree(data, widget.invisibleRootItem())
        widget.expandAll()


    #....................................................####
    # a more generic method to make tree 
    # the method mirorrs a dictionary (having dict, lists, class objects and others) as it.
    #TODO: Nmay need some debugging to get it work
    
    # def build_tree(self, value, item):
    #     item.setExpanded(True)
    #     if type(value) is dict:
    #         for key, val in sorted(value.iteritems()):
    #             child = QTreeWidgetItem()
    #             child.setText(0, unicode(key))
    #             item.addChild(child)
    #             self.build_tree(child, val)

    #     elif type(value) is list:
    #         for val in value:
    #             child = QTreeWidgetItem()
    #             item.addChild(child)
    #         if type(val) is dict:      
    #             child.setText(0, '[dict]')
    #             self.build_tree(child, val)
    #         elif type(val) is list:
    #             child.setText(0, '[list]')
    #             self.build_tree(child, val)
    #         else:
    #             child.setText(0, unicode(val))              
    #         child.setExpanded(True)
    #     else:
    #         child = QTreeWidgetItem()
    #         child.setText(0, unicode(value))
    #         item.addChild(child)

    # def make_treewidget(self, value, widget):
    #     self.widget.clear()
    #     build_tree(value, widget.invisibleRootItem())

    #........................................####








# def makeTreeView(treeWidget, ontology_tree):
#   root = "root"  # RULE: root of tree is called "root"

#   treeWidget.clear()
#   tree_items = {}
#   networks = list(ontology_tree.keys())
#   # root = self.root
#   tree_items[root] = __addItemToTreeWidget(treeWidget, None, root)
#   tree_items[root].name = ontology_tree[root]["name"]
#   for nw in networks:
#     if nw != root:
#       parent = root
#       child = ontology_tree[nw]["name"]
#       nodes = []
#       [nodes.append(n) for n in ontology_tree[nw]["parents"][::-1]]
#       nodes.append(child)
#       for child in nodes:
#         if child in tree_items:
#           parent = child
#         else:
#           parent_item = tree_items[parent]
#           tree_items[child] = __addItemToTreeWidget(treeWidget, parent_item, child)
#           tree_items[child].name = ontology_tree[child]["name"]
#           parent = child

#   treeWidget.expandAll()
#   return tree_items













    
    # custom method for loading an existing ontology  
    
            # with open(fileName[0], 'r') as f:
            #     file_text = f.read()
            # print('this is file name', fileName[0])
             # print(file_text)

            # g1 = RDFGraph()
            # g1.parse(fileName[0], format="turtle")
            # print('Number of tuples in the graph: ', len(g1))
            # # for stmt in g:
            # #     pprint.pprint(stmt)
            # for s,p,o in g1:
            #     print('these are ontology triples...', s,p,o)
            
            
            # x=self.print_test()
            # print(x)

            # g2 = Graph()
            # with open(fileName[0]) as fg:
            #     tupsList = [tuple(line.split()) for line in fg]
            #     for t in tupsList:
            #         if t:
            #             g2.append((t))
            
            # # for s, p, o in g2.match(None, None, None):
            # #     print((s,p,o))

            # triplesList = [(o,s) for s, _, o in g2.match(None, 'subClassOf', None)]
            # print(triplesList)
            # triplesListDict = {}
            # for o, s in triplesList:
            #     try:
            #         triplesListDict[o].append(s)
            #     except KeyError:
            #         triplesListDict[o] = [s]
            # print(triplesListDict)

            # nested_dict, master_dict = {}, {}
            # for a, b in triplesList:
            #     if a not in master_dict:
            #         nested_dict[a] = master_dict[a] = {}
            #     master_dict[a][b] = master_dict[b] = {}

            # print(nested_dict)
               
           
            # tree.setHeaderLabels(['l1', 'l2', 'l3'])

            # data = {'coatedSystem': {'substrate': {}, 'preTreatedSurface': {}, 'coatingLayer': {'binder': {}, 
            #         'pigment': {}, 'extender': {}, 'dye': {}, 'additive': {}}, 'interface': {}}, 'material': {'organic': {}, 
            #         'inorganic': {}, 'solid': {}, 'fluid': {'liquid': {'electrolyte': {}}, 'gas': {}}}, 'process': {'anodizing': {}, 
            #         'washing': {}, 'pickling': {}, 'solGelCoating': {}, 'etching': {}}}

            # def build_tree(data=None, parent=None):
            #     for key, value in data.items():
            #         item = QTreeWidgetItem(parent)
            #         item.setText(0, key)
            #         if isinstance(value, dict):
            #             build_tree(data=value, parent=item)

            
            
           

    #         subTree = []
    #         for key, value in triplesDict.items():
    #             root = QTreeWidgetItem(tree, [key])
    #             #print (root)
                
    # #print(subTree)
    #             for val in value:
    #                 # subTree.append(val)
    #                 item = QTreeWidgetItem([val])
    #                 root.addChild(item)
                # print(subTree)
            


  
    # def closeevent(self, event):
        
    #     quit_msg = "Are you sure you want to exit the program?"
    #     reply = QMessageBox.question(self, 'Message', 
    #                     quit_msg, QMessageBox.Yes | QMessageBox.No)

    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()
    def closeEvent(self, event):
        close = QMessageBox()
        close.setText("You sure?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel | QMessageBox.Save)
        close = close.exec()

        if close == QMessageBox.Yes:
            event.accept()
        elif close == QMessageBox.Save:
            self.onSaveSelected('save ontology')
            event.accept()
        else:
            event.ignore()


    
    # def check_subpath(self, item):
    #     globalpath_list = self.ontology_graph.path(self.item, self.ontology_root)
    #     localpath_list = self.ontology_graph.path(self.item, self.ontology_root)
    #     clicked_path = os.path.join(*clicked_item_path_list)




    #     self.clicked_item = item.text(n)
    #     print('clicked item is:', self.clicked_item)
    #     # self.ui.pushRemoveNode.setEnabled(True)
    #     ontograph = self.ontology_graph

    #     try:
    #         triplesList = [(o,s) for s, _, o in ontograph.match(None, 'subClassOf', None)]
    #     except AttributeError:
    #         print('The root is subclass of None')
    #     #print(triplesList)

    #     try:
    #         clicked_path_list = ontograph.path(self.clicked_item, 'cfo')
    #         clicked_path = os.path.join(*clicked_path_list)
    #     except AttributeError:
    #         print('This is root node')
    #     print(clicked_path)

    def addSubclassItem(self):
        pass

    def removeItem(self):
        pass

    # def onAddSubclassClicked(self):
    #     print('add subclass is clicked')




    # @QtCore.pyqtSlot(QTreeWidgetItem, int)
    # def onItemClicked(self, it, n):
    #     print("Item clicked: ", it.text(n))
    #     clicked_node_name = it.text(n)
    #     return clicked_node_name

    @QtCore.pyqtSlot(str)
    def onSelectSelected(self, val):
        if val == '<select>':
            message = 'please select an option from the dropdown list'
        
        else:
            message = 'you have selected the option: ' + val

        print(message)

    def onLoadSelected(self, val):
        if val == 'load ontology' :
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName = QFileDialog.getOpenFileName(None,"Load Ontology", '../coatingOntology', "","Turtle files (*.ttl)", options=options)


            tree = self.ui.treeWidget
            tree.setColumnCount(1)

            # The tuples are of the form (o,s) that are filtered from (s, subClassOf, o)
            # TODO: likewise, one can get lists of tuples with other relations (predicates) if desired.  
    
            og = self.create_ontograph(fileName[0])
            tupslist_subclassof = [(o,s) for s, _, o in og.match(None, 'subClassOf', None)]
            #tups_list = self.get_tupleslist(fileName[0])
            ns_dict = self.nested_dictionary(tupslist_subclassof) 
            self.make_treewidget(ns_dict, tree)
            self.ontology_graph = og
            # current_tree = self.build_tree(data=ns_dict, parent=tree)
            # self.current_tree = self.build_tree(data=ns_dict, parent=tree)

    def onSaveSelected(self, val):
        if val == 'save ontology':
            #tupslist_subclassof = [(o,s) for s, _, o in self.ontology_graph.match(None, 'subClassOf', None)]
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName = QFileDialog.getSaveFileName(None,"Save Ontology",'../coatingOntology',"","Turtle files (*.ttl)", options=options)
            try:
                file = open(fileName[0],'w')
                for l in [(s, p, o) for s, p, o in self.ontology_graph.match(None, None, None)]:
                    file.write(' '.join(str(s) for s in l) + '\n')
                    
            except FileNotFoundError:
                print('You have not selected a file to save or file was not found')
            file.close()


    def onVisualizeSelected(self, val):
        if val == 'visualize ontology':
            self.process = QtCore.QProcess()
            self.process.start("python", ['ontovis.py'])


    def onCreateSelected(self, val):
        if val == 'create ontology':
            self.ui.treeWidget.clear()
            self.ui.treeWidget.setColumnCount(1)
            print('create ontology selected')
            self.ontology_root = 'cfo'
            item = QTreeWidgetItem(self.ui.treeWidget)
            item.setText(0, self.ontology_root)
            self.ontology_graph = Graph()
            #self.ontology_graph = self.ontology_graph.append((self.ontology_root, 'subClassOf', None))

    

    def onItemClicked(self, item, n):
        self.clicked_item = item.text(n)
        print('clicked item is:', self.clicked_item)
        # self.ui.pushRemoveNode.setEnabled(True)
        ontograph = self.ontology_graph

        try:
            triplesList = [(o,s) for s, _, o in ontograph.match(None, 'subClassOf', None)]
        except AttributeError:
            print('The root is subclass of None')
        #print(triplesList)

        try:
            clicked_path_list = ontograph.path(self.clicked_item, 'cfo')
            clicked_path = os.path.join(*clicked_path_list)
        except AttributeError:
            print('This is root node')
        print(clicked_path)

        # To handle the deafult case while creating ontology
        # Initially there are no triples in the graph
        if not triplesList:
            self.ui.pushAddSubclass.setEnabled(True)

        for item in triplesList:
            # The add class option is enabled only when root is is selected
            if self.clicked_item == 'cfo':
                # self.ui.pushAddSubclass.setEnabled(True)
                self.ui.pushAddClass.setEnabled(False)
                self.ui.pushAddSubclass.setEnabled(True)
                self.ui.pushRemoveNode.setEnabled(False)
            
            if self.clicked_item == item[1] and item[0] == 'cfo':

                self.ui.pushAddClass.setEnabled(False)
                self.ui.pushAddSubclass.setEnabled(True)
                self.ui.pushRemoveNode.setEnabled(False)

            

            if self.clicked_item == item[0]:
                self.ui.pushAddClass.setEnabled(False)
                self.ui.pushAddSubclass.setEnabled(True)
                self.ui.pushRemoveNode.setEnabled(False)

                    # self.ui.pushAddSubclass.setEnabled(True)
                    # # self.ui.pushAddClass.setEnabled(False)
                    # self.ui.pushRemoveNode.setEnabled(True)

        
            
                

                # self.ui.pushAddClass.setEnabled(False)
            
            else:
                pass
                # self.ui.pushRemoveNode.setEnabled(True)

        


    def on_pushAddSubclass_pressed(self):
        text, ok = QtWidgets.QInputDialog.getText(self, "Add sub class", 
            "Enter subclass name as one word f.ex coating system as coatingSystem: ")
        if ok:
            print(type(self.clicked_item), type(text))
            # print(len(self.ontology_graph))
            # og = self.ontology_graph.append((text, 'subClassOf', self.clicked_item))
            # tupslist_subclassof = [(o,s) for s, _, o in og.match(None, 'subClassOf', None)]
            # #tups_list = self.get_tupleslist(fileName[0])
            # ns_dict = self.nested_dictionary(tupslist_subclassof) 
            # self.build_tree(data=ns_dict, parent=self.ui.treeWidget)
            # it = QTreeWidgetItem([text])
            # self.ui.treeWidget.addChild(it)
            ontograph = self.ontology_graph
            # triplesList = [(o,s) for s, _, o in ontograph.match(None, 'subClassOf', None)]
            
            self.ontology_graph.append((text, 'subClassOf', self.clicked_item))
            tupslist_subclassof = [(o,s) for s, _, o in ontograph.match(None, 'subClassOf', None)]
            print('this is add list', tupslist_subclassof)
            ns_dict = self.nested_dictionary(tupslist_subclassof) 
            print('This is nested dictionary....', ns_dict)
            # self.ui.treeWidget.clear()
            self.make_treewidget(ns_dict, self.ui.treeWidget)
            

    def on_pushAddClass_pressed(self):   
        text, ok = QtWidgets.QInputDialog.getText(self, "Add new class", 
            "Enter class name as one word f.ex coating system as coatingSystem: ")

        if ok:
            print('item clicked:', self.clicked_item)
            self.ontology_graph.append((text, 'subClassOf', 'cfo'))
            tupslist_subclassof = [(o,s) for s, _, o in self.ontology_graph.match(None, 'subClassOf', None)]
            print('this is add list', tupslist_subclassof)
            ns_dict = self.nested_dictionary(tupslist_subclassof) 
            print(ns_dict)
            # self.ui.treeWidget.clear()
            self.make_treewidget(ns_dict, self.ui.treeWidget)
            
    #TODO: remove option is currently disable by setting flag to False. This needs to be fixed!
    def on_pushRemoveNode_pressed(self):
        remove_item_list = [(s,p,o) for s, p, o in self.ontology_graph.match(self.clicked_item, 'subClassOf', None)]
        print('remove items list ......', remove_item_list)
        for rm in remove_item_list:
            self.ontology_graph.remove(rm)
        tupslist_subclassof = [(o,s) for s, _, o in self.ontology_graph.match(None, 'subClassOf', None)]
        print('this is add list', tupslist_subclassof)

        ns_dict = self.nested_dictionary(tupslist_subclassof) 
        print(ns_dict)
        # self.ui.treeWidget.clear()
        self.make_treewidget(ns_dict, self.ui.treeWidget)
            
    

    # def on_pushAddSubclass_pressed(self):
    #     self.ui.pushasp_signal = True
    #     return self.ui.pushasp_signal



        # og = self.create_ontograph
        #for s, _, o in g2.match(None, 'subClassOf', None):
        # def addClassItem(node):
        #     current_root = node
        # text, ok = self.ui.
        
        # QtWidget.QInputDialog.getText(self, 'add a new class')
        # if ok:
        #     it = self.ui.treeWidget.QTreeWidgetItem([text])
        #     self.ui.treeWidget.clicked_node.addChild(it)

        # self.addSubclassItem()
    


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = OntobuilderUI()
    MainWindow.show()
    sys.exit(app.exec_())