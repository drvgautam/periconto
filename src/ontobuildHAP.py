#!/usr/local/bin/python3


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


import json
import os

from PyQt5 import QtCore
from PyQt5 import QtGui
# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

from graph import Graph
from ontologybuilderHAP_gui import Ui_MainWindow
from resources.pop_up_message_box import makeMessageBox
from resources.resources_icons import roundButton
from resources.single_list_selector_impl import SingleListSelector
from resources.ui_string_dialog_impl import UI_String

ROOT_CLASS = "coating"
PREDICATES = {"subclass": "is_a_subclass_of",
              "link"    : "link_to_class"}
LINK_COLOUR = QtGui.QColor(255, 100, 5, 255)

QTROUPLEFILE = os.path.join("../coatingOntology_HAP", "%s.ttl" % "HAP")


def putData(data, file_spec, indent="  "):
  print("writing to file: ", file_spec)
  dump = json.dumps(data, indent=indent)
  with open(file_spec, "w+") as f:
    f.write(dump)


def getFilesAndVersions(abs_name, ext):
  base_name = os.path.basename(abs_name)
  ver = 0  # initial last version
  _s = []
  directory = os.path.dirname(abs_name)  # listdir(os.getcwd())
  files = os.listdir(directory)

  for f in files:
    n, e = os.path.splitext(f)
    #        print 'name', n
    if e == ext:  # this is another type
      if n[0:len(base_name) + 1] == base_name + "(":  # only those that start with name
        #  extract version
        l = n.index("(")
        r = n.index(")")
        assert l * r >= 0  # both must be there
        v = int(n[l + 1:r])
        ver = max([ver, v])
        _s.append(n)
  return _s, ver


def saveBackupFile(path):
  ver_temp = "(%s)"
  (abs_name, ext) = os.path.splitext(path)  # path : directory/<name>.<ext>
  #  TODO: the access check fails -- not clear why, when removed writing works OK
  if os.path.exists(path):
    _f, ver = getFilesAndVersions(abs_name, ext)
    old_path = path
    new_path = abs_name + ver_temp % str(ver + 1) + ext
    next_path = abs_name + ver_temp % str(ver + 2) + ext
    os.rename(old_path, new_path)
    return old_path, new_path, next_path
  else:
    print("Error -- no such file : %s" % path, file=sys.stderr)
    return


def saveWithBackup(data, path):
  print("saving")
  old_path, new_path, next_path = saveBackupFile(path)
  putData(data, path)


def getData(file_spec):
  # print("get data from ", file_spec)
  if os.path.exists(file_spec):
    f = open(file_spec, "r")
    data = json.loads(f.read())
    return data
  else:
    return None


class OntobuilderUI(QMainWindow):
  def __init__(self):
    super(OntobuilderUI, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    roundButton(self.ui.pushLoad, "load", tooltip="load ontology")
    roundButton(self.ui.pushVisualise, "dot_graph", tooltip="visualise ontology")
    roundButton(self.ui.pushCreate, "plus", tooltip="create")
    roundButton(self.ui.pushSave, "save", tooltip="save ProMo base ontology")
    roundButton(self.ui.pushExit, "exit", tooltip="exit")

    self.buttons = {"load"               : self.ui.pushLoad,
                    "create"             : self.ui.pushCreate,
                    "visualise"          : self.ui.pushVisualise,
                    "save"               : self.ui.pushSave,
                    "exit"               : self.ui.pushExit,
                    "add_subclass"       : self.ui.pushAddSubclass,
                    "link_new_class"     : self.ui.pushAddNewClass,
                    "link_existing_class": self.ui.pushAddExistingClass,
                    "remove"             : self.ui.pushRemoveNode
                    }
    w = 150
    h = 25
    for i in ["add_subclass", "link_new_class", "link_existing_class"]:
      self.buttons[i].setFixedSize(w, h)

    self.ontology_graph = None
    self.ontology_root = None
    self.changed = False

    self.__ui_state("start")
    self.current_class = None
    self.current_subclass = None
    self.subclass_names = {}
    self.class_names = []
    self.class_path = []
    self.link_lists = {}
    self.class_definition_sequence = []

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

  def __ui_state(self, state):
    if state == "start":
      show = ["load",
              "create",
              "exit",
              ]
    elif state == "show_tree":
      show = ["save",
              "exit",
              "visualise",
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
              "add_subclass",
              ]
    elif state == "no_existing_classes":
      show = ["save",
              "exit",
              "add_subclass",
              "link_new_class",
              ]
    elif state == "occupied":
      show = ["save",
              "exit",
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
    self.current_subclass = origin
    self.__ui_state("show_tree")

  def __makeTree(self, origin=None, stack=[], parent=None):

    graph = self.CLASSES[self.current_class]
    for subject, predicate, object in graph.match(None, None, origin):
      if subject not in stack:
        print("add %s <-- %s" % (object, subject))
        item = QTreeWidgetItem(parent)
        if predicate == PREDICATES["link"]:
          item.setBackground(0, LINK_COLOUR)
        else:
          stack.append(subject)
        item.setText(0, subject)
        self.__makeTree(origin=subject, stack=stack, parent=item)

  def on_pushCreate_pressed(self):
    self.CLASSES = {ROOT_CLASS: Graph()}
    self.__createTree(ROOT_CLASS)
    self.current_class = ROOT_CLASS
    self.subclass_names[ROOT_CLASS] = []
    self.class_names.append(ROOT_CLASS)
    self.class_path = [ROOT_CLASS]
    self.link_lists[ROOT_CLASS] = []
    self.ui.listClasses.addItems(self.class_path)
    self.class_definition_sequence.append(ROOT_CLASS)
    self.changed = True

  def on_treeClass_itemPressed(self, item, column):
    text_ID = item.text(column)
    print("debugging -- ", text_ID)
    self.current_subclass = text_ID

    if text_ID in self.class_names:
      self.__ui_state("selected_class")
      if self.current_class != text_ID:
        self.__shiftClass(text_ID)
    elif self.__islinked(text_ID):
      self.__ui_state("occupied")
      pass
    else:

      if not self.__permittedClasses():
        self.__ui_state("no_existing_classes")
      else:
        self.__ui_state("selected_subclass")
      self.current_subclass = text_ID

  def __islinked(self, ID):
    for cl in self.link_lists:
      for linked_class, linked_to_class, linked_to_subclass in self.link_lists[cl]:
        if linked_to_class == self.current_class:
          if linked_to_subclass == ID:
            return True

    return False

  def on_pushAddSubclass_pressed(self):
    print("debugging -- add subclass")

    forbidden = sorted(self.subclass_names[self.current_class]) + sorted(self.class_names)
    dialog = UI_String("name for subclass", limiting_list=forbidden)
    dialog.exec_()

    subclass_ID = dialog.getText()
    self.subclass_names[self.current_class].append(subclass_ID)
    self.CLASSES[self.current_class].append((subclass_ID, PREDICATES["subclass"], self.current_subclass))
    parent_item = self.ui.treeClass.currentItem()
    item = QTreeWidgetItem(parent_item)
    item.setText(0, subclass_ID)
    self.ui.treeClass.expandAll()
    self.changed = True


  def on_pushAddNewClass_pressed(self):
    print("debugging -- add class")

    forbidden = sorted(self.class_names)
    dialog = UI_String("name for subclass", limiting_list=forbidden)
    dialog.exec_()
    class_ID = dialog.getText()
    if not class_ID:
      return

    self.CLASSES[class_ID] = Graph()
    self.class_definition_sequence.append(class_ID)
    # make link
    self.CLASSES[self.current_class].append((class_ID, PREDICATES["link"], self.current_subclass))

    if class_ID not in self.link_lists:
      self.link_lists[class_ID] = []
    self.link_lists[class_ID].append((class_ID, self.current_class, self.current_subclass))

    self.__createTree(class_ID)
    self.subclass_names[class_ID] = []
    self.class_names.append(class_ID)
    self.__addToClassPath(addclass=class_ID)
    self.current_class = class_ID
    self.changed = True

  def on_pushAddExistingClass_pressed(self):
    print("debugging -- pushExistingClass")
    permitted_classes = self.__permittedClasses()

    print("debugging -- ", permitted_classes)
    if permitted_classes:
      dialog = SingleListSelector(permitted_classes)
      dialog.exec_()
      selection = dialog.getSelection()
      print("debugging")
      if not selection:
        return

      class_ID = selection
      self.CLASSES[self.current_class].append((class_ID, PREDICATES["link"], self.current_subclass))

      if class_ID not in self.link_lists:
        self.link_lists[class_ID] = []
      self.link_lists[class_ID].append((class_ID, self.current_class, self.current_subclass))

      parent_item = self.ui.treeClass.currentItem()
      item = QTreeWidgetItem(parent_item)
      item.setText(0, class_ID)
      columns = item.columnCount()
      item.setBackground(0, LINK_COLOUR)
      self.ui.treeClass.expandAll()
      self.changed = True

  def __permittedClasses(self):
    permitted_classes = []
    for cl in self.CLASSES:
      if cl != self.current_class:
        if cl not in self.link_lists[cl]:
          if cl not in self.class_path:
            permitted_classes.append(cl)
    return permitted_classes

  def __addToClassPath(self, addclass):
    self.class_path.append(addclass)
    self.ui.listClasses.clear()
    self.ui.listClasses.addItems(self.class_path)

  def __cutClassPath(self, cutclass):
    i = self.class_path.index(cutclass)
    self.class_path = self.class_path[:i + 1]
    self.ui.listClasses.clear()
    self.ui.listClasses.addItems(self.class_path)

  def on_listClasses_itemClicked(self, item):
    class_ID = item.text()
    print("debugging -- ", class_ID)
    self.__shiftClass(class_ID)

  def __shiftClass(self, class_ID):
    self.current_class = class_ID
    self.__createTree(class_ID)
    if class_ID not in self.class_path:
      self.__addToClassPath(class_ID)
    else:
      self.__cutClassPath(class_ID)

  def on_pushExit_pressed(self):
    self.closeMe()

  def closeEvent(self, event):
    self.closeMe()

  def closeMe(self):
    if self.changed:
      dialog = makeMessageBox(message="save changes", buttons=["YES", "NO"])
      if dialog == "YES":
        print("save")
        self.on_pushSave_pressed()

      elif dialog == "NO":
        print("exit")

    else:
      print("no changes")
    self.close()

  def on_pushSave_pressed(self):
    print("debugging -- pushSave")
    graphs = {}
    for cl in self.class_definition_sequence:
      graphs[cl] = []
      for t in self.CLASSES[cl].triples:
        graphs[cl].append(t)

    saveWithBackup(graphs, QTROUPLEFILE)
    self.changed = False

  def on_pushLoad_pressed(self):
    graphs = getData(QTROUPLEFILE)
    self.CLASSES = {}
    for g in graphs:
      self.class_definition_sequence.append(g)
      self.class_names.append(g)
      self.subclass_names[g] = []
      self.link_lists[g] = []
      self.CLASSES[g] = Graph()
      for t in graphs[g]:
        self.CLASSES[g].append(t)
        s, p, o = t
        if p == PREDICATES["subclass"]:
          self.subclass_names[g].append(s)
        elif p == PREDICATES["link"]:
          if g not in self.link_lists:
            self.link_lists[g] = []
          self.link_lists[g].append((s, g, o))

    self.current_class = ROOT_CLASS
    self.class_path = [ROOT_CLASS]
    self.__createTree(ROOT_CLASS)
    self.ui.listClasses.addItems(self.class_path)
    self.__ui_state("show_tree")


  def on_pushVisualise_pressed(self):

    graph_overall = Graph()
    for cl in self.CLASSES:
      for t in self.CLASSES[cl].triples:
        graph_overall.append(t)

    dot = graph_overall.plot()
    print("debugging -- dot")
    dot.render("graph")

    #
    # self.process = QtCore.QProcess()
    # self.process.start("python", ['ontovis.py'])

  # method to load a ontology from a file and create ontology graph base on graph utility provided by Thomas
  def create_ontograph(self, onto_filename):
    ontoGraph = Graph()
    with open(onto_filename) as fg:
      tupsList = [tuple(line.split()) for line in fg]
      for t in tupsList:
        if t:
          ontoGraph.append((t))
    return ontoGraph


if __name__ == "__main__":
  import sys

  app = QApplication(sys.argv)

  icon_f = "task_ontology_foundation.svg"
  icon = os.path.join(os.path.abspath("resources/icons"), icon_f)
  app.setWindowIcon(QtGui.QIcon(icon))

  MainWindow = OntobuilderUI()
  MainWindow.show()
  sys.exit(app.exec_())
