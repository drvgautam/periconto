#!/usr/local/bin/python3


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


import os
import pprint

from PyQt5 import QtCore, QtGui
# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

from graph import Graph
from ontologybuilderHAP_gui import Ui_MainWindow
from resources.resources_icons import roundButton
from resources.ui_string_dialog_impl import UI_String

ROOT_CLASS = "coating"
PREDICATES = {"subclass": "is_a_subclass_of",
              "link" : "link_to_class"}
LINK_COLOUR = QtGui.QColor(255, 100, 5, 255)

class OntobuilderUI(QMainWindow):
  def __init__(self):
    super(OntobuilderUI, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    self.ontology_graph = None
    self.ontology_root = None

    roundButton(self.ui.pushLoad, "load", tooltip="load ontology")
    roundButton(self.ui.pushVisualise, "dot_graph", tooltip="visualise ontology")
    roundButton(self.ui.pushCreate, "plus", tooltip="create")
    roundButton(self.ui.pushSave, "save", tooltip="save ProMo base ontology")
    roundButton(self.ui.pushExit, "exit", tooltip="exit")

    self.buttons = {"load" : self.ui.pushLoad,
               "create": self.ui.pushCreate,
               "visualise": self.ui.pushVisualise,
               "save" : self.ui.pushSave,
               "exit": self.ui.pushExit,
               "add_subclass" : self.ui.pushAddSubclass,
               "link_new_class": self.ui.pushAddNewClass,
               "link_existing_class": self.ui.pushAddExistingClass,
               "remove": self.ui.pushRemoveNode
               }
    w = 150
    h = 25
    for i in ["add_subclass", "link_new_class",  "link_existing_class"]:
      self.buttons[i].setFixedSize(w,h)


    self.ui_state("start")
    self.current_class = None
    self.current_subclass = None
    self.subclass_names= {}
    self.class_names = []
    self.class_path = []
    self.link_lists = {}

    #
    # coating = Graph()
    # coating.clear()
    # coating.append(('substrate', 'is-a', 'coating'))
    # coating.append(('pre-treatement', 'is-a', 'coating'))
    # coating.append(('coating-layer', 'is-a', 'coating'))
    # coating.append(('interface', 'is-a', 'coating'))
    # coating.append(('pigment', 'is-a', 'coating-layer'))
    # coating.append(('extender', 'is-a', 'coating-layer'))
    # coating.append(('dye', 'is-a', 'coating-layer'))
    # coating.append(('additive', 'is-a', 'coating-layer'))
    # coating.append(('defoamer', 'is-a', 'additive'))
    # coating.append(('wetting', 'is-a', 'additive'))
    # self.coating = coating
    #
    # self.__createTree("coating")

  def ui_state(self, state):
    if state == "start":
      show = ["load",
              "create",
              "exit",
              ]
    elif state == "show tree":
      show = ["save",
              "create",
              "exit",
              ]
    elif state == "selected_subclass":
      show = ["save",
              "exit",
              "add_subclass",
              "link_new_class",
              "link_existing_class",
              ]
    elif state == "selected_class":
      show = ["save",
              "exit",
              "add_subclass"
              ]
    else:
      show = []

    for b in self.buttons:
      if b not in show:
        self.buttons[b].hide()
      else:
        self.buttons[b].show()

  def __createTree(self, origin):
    widget = self.ui.treeClass
    widget.clear()

    rootItem = QTreeWidgetItem(widget)
    widget.setColumnCount(1)
    rootItem.root = origin
    rootItem.setText(0, origin)
    rootItem.setSelected(True)
    widget.addTopLevelItem(rootItem)
    self.current_class = origin
    self.__makeTree(origin=origin, stack=[], parent=rootItem)
    widget.show()
    widget.expandAll()

  def __makeTree(self, origin=None, stack=[], parent=None):

    graph = self.CLASSES[self.current_class]
    for subject, predicate , object in graph.match(None, None, origin):
      if subject not in stack:
        print("add %s <-- %s"%(object,subject))
        item = QTreeWidgetItem(parent)
        columns = item.columnCount()
        if predicate == PREDICATES["link"]:
          print("debugging columns ", columns)
          item.setBackground(columns,LINK_COLOUR)
        item.setText(0, subject)
        stack.append(subject)
        self.__makeTree(origin=subject,stack=stack, parent=item)

  def on_pushCreate_pressed(self):
    self.CLASSES= {ROOT_CLASS: Graph()}
    self.__createTree(ROOT_CLASS)
    self.current_class = ROOT_CLASS
    self.subclass_names[ROOT_CLASS] = []
    self.class_names.append(ROOT_CLASS)
    self.class_path = [ROOT_CLASS]
    self.link_lists[ROOT_CLASS] = []

    self.ui.listClasses.addItems(self.class_path)


  def on_treeClass_itemPressed(self, item, column):
    text_ID = item.text(column)
    print("debugging -- ", text_ID)
    self.current_subclass = text_ID

    if text_ID in self.class_names:
      self.ui_state("selected_class")
      if self.current_class != text_ID:
        self.shiftClass(text_ID)
    else:
      self.ui_state("selected_subclass")
      self.current_subclass = text_ID



  def on_pushLoad_pressed(self):
    print("debugging")
    # options = QFileDialog.Options()
    # options |= QFileDialog.DontUseNativeDialog
    # fileName = QFileDialog.getOpenFileName(None, "Load Ontology", '../coatingOntology', "", "Turtle files (*.ttl)",
    #                                        options=options)
    #
    # self.ontology_root = 'root'
    # tree = self.ui.treeClass
    # tree.setColumnCount(1)
    #
    # # The tuples are of the form (o,s) that are filtered from (s, subClassOf, o)
    # # TODO: likewise, one can get lists of tuples with other relations (predicates) if desired.
    #
    # og = self.create_ontograph(fileName[0])
    # tupslist_isaclass = [(o, s) for s, _, o in og.match(None, 'isA', 'Class')]
    # tupslist_subclassof = [(o, s) for s, _, o in og.match(None, 'subClassOf', None)]
    # tupslist_classsubclass = tupslist_isaclass + tupslist_subclassof
    # print('Tuples list isA...', tupslist_isaclass)
    # print('Tuples list subcassof ...', tupslist_subclassof)
    # print('Tuples list class-subclass...', tupslist_classsubclass)
    # # tups_list = self.get_tupleslist(fileName[0])
    # ns_dict = self.nested_dictionary(tupslist_classsubclass)
    # pprint.pprint(ns_dict, width=1)
    #
    # # pass the dictKey = 'Class' so that the Class node is not rendered in the treeWidget
    # self.make_treewidget(ns_dict, tree, self.ontology_root, dictKey='Class')
    # self.ontology_graph = og
    # # current_tree = self.build_tree(data=ns_dict, parent=tree)
    # # self.current_tree = self.build_tree(data=ns_dict, parent=tree)



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



  def on_pushAddSubclass_pressed(self):
    print("debugging -- add subclass")
    parent_item = self.ui.treeClass.currentItem()

    forbidden = sorted(self.subclass_names[self.current_class]) + sorted(self.class_names)
    dialog = UI_String("name for subclass",limiting_list=forbidden)
    dialog.exec_()
    subclass_ID = dialog.getText()
    self.subclass_names[self.current_class].append(subclass_ID)
    self.CLASSES[self.current_class].append((subclass_ID, PREDICATES["subclass"], self.current_subclass))
    item = QTreeWidgetItem(parent_item)
    item.setText(0, subclass_ID)

  def on_pushAddNewClass_pressed(self):
    print("debugging -- add class")

    forbidden = sorted(self.class_names)
    dialog = UI_String("name for subclass",limiting_list=forbidden)
    dialog.exec_()
    class_ID = dialog.getText()

    # make link
    self.CLASSES[self.current_class].append((class_ID,PREDICATES["link"], self.current_subclass))

    self.CLASSES[class_ID] = Graph()
    self.__createTree(class_ID)
    self.current_class = class_ID
    self.subclass_names[class_ID] = []
    self.class_names.append(class_ID)
    self.addToClassPath(addclass=class_ID)
    if class_ID not in self.link_lists:
      self.link_lists[class_ID] = []
    self.link_lists[class_ID].append((class_ID, self.current_subclass))

  def addToClassPath(self, addclass):
    self.class_path.append(addclass)
    self.ui.listClasses.clear()
    self.ui.listClasses.addItems(self.class_path)


  def cutClassPath(self, cutclass):
    i = self.class_path.index(cutclass)
    self.class_path = self.class_path[:i+1]
    self.ui.listClasses.clear()
    self.ui.listClasses.addItems(self.class_path)

  def on_listClasses_itemDoubleClicked(self,item):
    class_ID = item.text()
    print("debugging -- ", class_ID)
    self.shiftClass(class_ID)

  def shiftClass(self, class_ID):
    self.current_class = class_ID
    self.__createTree(class_ID)
    if class_ID not in self.class_path:
      self.addToClassPath(class_ID)
    else:
      self.cutClassPath(class_ID)

  def on_pushExistingClass_pressed(self):
    print("debugging -- pushExistingClass")



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


  def on_pushAddClass_pressed(self):
    print("debugging -- puschAddClass")

  def on_pushSave_pressed(self):
    print("debugging -- pushSave")

    for cl in self.CLASSES:
      graph = self.CLASSES[cl]
      graph.write(cl)



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

  # def addSubclassItem(self):
  #   pass
  #
  # def removeItem(self):
  #   pass

  # def onAddSubclassClicked(self):
  #     print('add subclass is clicked')

  # @QtCore.pyqtSlot(QTreeWidgetItem, int)
  # def onItemClicked(self, it, n):
  #     print("Item clicked: ", it.text(n))
  #     clicked_node_name = it.text(n)
  #     return clicked_node_name


  def onSaveSelected(self, val):
    if val == 'save ontology':
      # tupslist_subclassof = [(o,s) for s, _, o in self.ontology_graph.match(None, 'subClassOf', None)]
      options = QFileDialog.Options()
      options |= QFileDialog.DontUseNativeDialog
      fileName = QFileDialog.getSaveFileName(None, "Save Ontology", '../coatingOntology', "", "Turtle files (*.ttl)",
                                             options=options)
      try:
        file = open(fileName[0], 'w')
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
      self.ontology_root = 'root'
      item = QTreeWidgetItem(self.ui.treeWidget)
      item.setText(0, self.ontology_root)
      self.ontology_graph = Graph()
      # self.ontology_graph = self.ontology_graph.append((self.ontology_root, 'subClassOf', None))

  def onItemClicked(self, item, n):
    self.clicked_item = item.text(n)
    print('clicked item is:', self.clicked_item)
    # self.ui.pushRemoveNode.setEnabled(True)
    ontograph = self.ontology_graph

    try:
      # triplesList = [(o,s) for s, _, o in ontograph.match(None, 'subClassOf', None)]

      tupslist_isaclass = [(o, s) for s, _, o in ontograph.match(None, 'isA', 'Class')]
      tupslist_subclassof = [(o, s) for s, _, o in ontograph.match(None, 'subClassOf', None)]
      tupslist_classsubclass = tupslist_isaclass + tupslist_subclassof

    except AttributeError:
      print('The root is subclass of None')
    # print(triplesList)

    try:
      clicked_path_list = ontograph.path(self.clicked_item, 'root')
      clicked_path = os.path.join(*clicked_path_list)
    except AttributeError:
      print('This is root node')
    print(clicked_path)

    # To handle the deafult case while creating ontology
    # Initially there are no triples in the graph
    if not tupslist_classsubclass:
      self.ui.pushAddSubclass.setEnabled(False)
      self.ui.pushAddClass.setEnabled(True)

    for item in tupslist_classsubclass:
      # The add class option is enabled only when root is is selected
      if self.clicked_item == 'root':
        # self.ui.pushAddSubclass.setEnabled(True)
        self.ui.pushAddClass.setEnabled(True)
        self.ui.pushAddSubclass.setEnabled(False)
        self.ui.pushRemoveNode.setEnabled(False)

      if self.clicked_item == item[1] and item[0] == 'Class':

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
  #
  # def on_pushAddSubclass_pressed(self):
  #   print("debugging -- add subclass")
  #
  #   subclass_name =
    # text, ok = QtWidgets.QInputDialog.getText(self, "Add sub class",
    #                                           "Enter subclass name as one word f.ex coating system as coatingSystem: ")
    # if ok:
    #   print(type(self.clicked_item), type(text))
    #   # print(len(self.ontology_graph))
    #   # og = self.ontology_graph.append((text, 'subClassOf', self.clicked_item))
    #   # tupslist_subclassof = [(o,s) for s, _, o in og.match(None, 'subClassOf', None)]
    #   # #tups_list = self.get_tupleslist(fileName[0])
    #   # ns_dict = self.nested_dictionary(tupslist_subclassof)
    #   # self.build_tree(data=ns_dict, parent=self.ui.treeWidget)
    #   # it = QTreeWidgetItem([text])
    #   # self.ui.treeWidget.addChild(it)
    #   ontograph = self.ontology_graph
    #   # triplesList = [(o,s) for s, _, o in ontograph.match(None, 'subClassOf', None)]
    #
    #   self.ontology_graph.append((text, 'subClassOf', self.clicked_item))
    #   tupslist_subclassof = [(o, s) for s, _, o in ontograph.match(None, 'subClassOf', None)]
    #   print('this is add list', tupslist_subclassof)
    #   ns_dict = self.nested_dictionary(tupslist_subclassof)
    #   print('This is nested dictionary....', ns_dict)
    #   # self.ui.treeWidget.clear()
    #   self.make_treewidget(ns_dict, self.ui.treeWidget, self.ontology_root)
  #
  # def on_pushAddClass_pressed(self):
  #   print("debugging -- puschAddClass")


    # text, ok = QtWidgets.QInputDialog.getText(self, "Add new class",
    #                                           "Enter class name as one word f.ex coating system as coatingSystem: ")
    #
    # if ok:
    #   print('item clicked:', self.clicked_item)
    #   self.ontology_graph.append((text, 'isA', 'Class'))
    #   tupslist_subclassof = [(o, s) for s, _, o in self.ontology_graph.match(None, 'isA', None)]
    #
    #   tupslist_isaclass = [(o, s) for s, _, o in self.ontology_graph.match(None, 'isA', 'Class')]
    #   tupslist_subclassof = [(o, s) for s, _, o in self.ontology_graph.match(None, 'subClassOf', None)]
    #   tupslist_classsubclass = tupslist_isaclass + tupslist_subclassof
    #   print('Tuples list isA...', tupslist_isaclass)
    #   print('Tuples list subcassof ...', tupslist_subclassof)
    #   print('Tuples list class-subclass...', tupslist_classsubclass)
    #   # tups_list = self.get_tupleslist(fileName[0])
    #   ns_dict = self.nested_dictionary(tupslist_classsubclass)
    #   pprint.pprint(ns_dict, width=1)
    #
    #   # print('this is add list', tupslist_subclassof)
    #   # ns_dict = self.nested_dictionary(tupslist_subclassof)
    #   # print(ns_dict)
    #   # self.ui.treeWidget.clear()
    #   self.make_treewidget(ns_dict, self.ui.treeWidget, self.ontology_root, dictKey='Class')

  # TODO: remove option is currently disable by setting flag to False. This needs to be fixed!
  # def on_pushRemoveNode_pressed(self):
  #   remove_item_list = [(s, p, o) for s, p, o in self.ontology_graph.match(self.clicked_item, 'subClassOf', None)]
  #   print('remove items list ......', remove_item_list)
  #   for rm in remove_item_list:
  #     self.ontology_graph.remove(rm)
  #   tupslist_subclassof = [(o, s) for s, _, o in self.ontology_graph.match(None, 'subClassOf', None)]
  #   print('this is add list', tupslist_subclassof)
  #
  #   ns_dict = self.nested_dictionary(tupslist_subclassof)
  #   print(ns_dict)
  #   # self.ui.treeWidget.clear()
  #   self.make_treewidget(ns_dict, self.ui.treeWidget, self.ontology_root)

  # def on_pushAddSubclass_pressed(self):
  #     self.ui.pushasp_signal = True
  #     return self.ui.pushasp_signal

  # og = self.create_ontograph
  # for s, _, o in g2.match(None, 'subClassOf', None):
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
