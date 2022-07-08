#!/usr/local/bin/python3

"""
This version uses RDF syntax for the predicates. The subjects and objects are Literals. The latter caused problems
when saving using the serializers. It can be saved but not read afterwards.

So the approach is to use an internal representation of the predicates and translate when loading and saving.


"""

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


import json
import os

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from rdflib import Graph, ConjunctiveGraph, RDF, BNode, Literal, RDFS, Dataset
from rdflib.plugins.stores.memory import Memory


# from graphHAP import Graph
from ontologybuilderHAP_gui import Ui_MainWindow
from resources.pop_up_message_box import makeMessageBox
from resources.resources_icons import roundButton
from resources.single_list_selector_impl import SingleListSelector
from resources.ui_string_dialog_impl import UI_String

from graphviz import Digraph

ROOT_CLASS = "coating"
PREDICATES = {
        "subclass": RDFS.subClassOf,   #"is_a_subclass_of",
        "link"    : RDFS.isDefinedBy, #"link_to_class"
        }
MYPredicates = {RDFS.subClassOf: "is_a_subclass_of",
                RDFS.isDefinedBy: "link_to_class"}

LINK_COLOUR = QtGui.QColor(255, 100, 5, 255)

TTLFile = os.path.join("../coatingOntology_HAP", "%s.ttl" % "HAP")
TTLDirectory = "../coatingOntology_HAP"


def plot(graph, class_names=[]):
  """
  Create Digraph plot
  """
  dot = Digraph()
  # Add nodes 1 and 2
  for s, p, o in graph.triples((None,None,None)):
    ss = str(s)
    sp = str(p)
    so = str(o)
    if ss in class_names:
      dot.node(ss, color='red', shape="rectangle")
    else:
      dot.node(ss)

    if so in class_names:
      dot.node(so, color='red', shape="rectangle")
    else:
      dot.node(so)

    my_p = MYPredicates[p]
    dot.edge(ss, so, label=my_p)

  # Visualize the graph
  return dot

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

def makeRDFCompatible(identifier):
  """
  To be adapted to imported notation.
  For now it generates rdflib Literals
  """
  return Literal(identifier)

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

    self.buttons = {
            "load"               : self.ui.pushLoad,
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
    self.TTLfile = TTLFile

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
    self.__makeTree(origin=Literal(origin), stack=[], parent=rootItem)
    widget.show()
    widget.expandAll()
    self.current_subclass = origin
    self.__ui_state("show_tree")



  def __makeTree(self, origin=None, stack=[], parent=None):

    graph = self.CLASSES[self.current_class]
    for subject, predicate, object in graph.triples((None, None, origin)):
      if subject not in stack:
        print("add %s <-- %s" % (object, subject))
        item = QTreeWidgetItem(parent)
        if predicate == PREDICATES["link"]:
          item.setBackground(0, LINK_COLOUR)
        else:
          stack.append(subject)
        item.setText(0, subject)
        self.__makeTree(origin=Literal(subject), stack=stack, parent=item)

  def on_pushCreate_pressed(self):
    dialog = UI_String("name for your ontology file", placeholdertext="file name extension is deault")
    dialog.exec_()
    name = dialog.getText()
    if name:
      fname = name.split(".")[0] + ".ttl"
      self.TTLFile = os.path.join(TTLDirectory, fname)
    else:
      self.close()


    self.CLASSES = {ROOT_CLASS: Graph('Memory', Literal(ROOT_CLASS))}
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

    # get an identifier for the subclass
    forbidden = sorted(self.subclass_names[self.current_class]) + sorted(self.class_names)
    dialog = UI_String("name for subclass", limiting_list=forbidden)
    dialog.exec_()
    subclass_ID = dialog.getText()

    # keep track of names
    self.subclass_names[self.current_class].append(subclass_ID)

    # add to graph
    subject = makeRDFCompatible(subclass_ID)
    object = makeRDFCompatible(self.current_subclass)
    self.CLASSES[self.current_class].add((subject, PREDICATES["subclass"], object))

    # generate GUI tree
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

    self.CLASSES[class_ID] = Graph('Memory', Literal(class_ID))
    self.class_definition_sequence.append(class_ID)

    # make link
    subject = makeRDFCompatible(class_ID)
    object = makeRDFCompatible(self.current_subclass)
    self.CLASSES[self.current_class].add((subject, PREDICATES["link"], object))

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
      subject = makeRDFCompatible(class_ID)
      object = makeRDFCompatible(self.current_subclass)
      self.CLASSES[self.current_class].add((subject, PREDICATES["link"], object))

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

    # NOTE: this does work fine, but one cannot read it afterwards. Issue is the parser. It assumes that the subject and
    # NOTE: object are in the namespace.

    # conjunctiveGraph = ConjunctiveGraph('Memory')
    # for cl in self.class_definition_sequence:
    #   uri = Literal(cl)
    #   for s,p,o in self.CLASSES[cl].triples((None,None,None)):
    #     print(s,p,o)
    #     conjunctiveGraph.get_context(uri).add([s,p,o])
    #
    # print("debugging")
    #
    # f = self.TTLFile.split(".")[0] + ".nqd"
    # inf = open(f,'w')
    # inf.write(conjunctiveGraph.serialize(format="nquads"))
    # inf.close()
    #
    # print("written to file ", f)


    # Note: saving it with the RDF syntax did not work for loading. Needs more reading...?

    graphs = {}
    for cl in self.class_definition_sequence:
      graphs[cl] = []
      for  s,p,o  in self.CLASSES[cl].triples((None,None,None)):
        my_p = MYPredicates[p]
        graphs[cl].append((s,my_p,o))

    saveWithBackup(graphs, TTLFile)

    # graphs = Graph("Memory")
    # for cl in self.class_definition_sequence:
    #   # graphs[cl] = []
    #   for t in self.CLASSES[cl].triples((None, None, None)):
    #     graphs.add(t)
    #
    # self.TTLFile = self.TTLFile.split(".ttl")[0] + ".nquads"
    #
    # graphs.serialize(TTLFile, format="nquads")
    # saveWithBackup(graphs, TTLFile)
    # self.changed = False

    self.changed = False


  def saveAs(self):
    print("not implemented")

  def on_pushLoad_pressed(self):
    options = QFileDialog.Options()
    dialog = QFileDialog.getOpenFileName(None,
                                         "Load Ontology",
                                         TTLDirectory,
                                         "",
                                         # "Turtle files (*.ttl)",
                                         "Nquads files (*.ttl",
                                         # options=options
                                         )
    self.TTLFile = dialog[0]
    if dialog[0] == "":
      self.close()

    # try:
    #   data = Dataset()
    #   infile = open(self.TTLFile, 'r')
    #   data.parse(infile, format="nquads")
    #   infile.close()
    #   print("debugging")
    # except:
    #   pass

    print("debugging")
    graphs = getData(self.TTLFile)
    self.CLASSES = {}
    for g in graphs:
      self.class_definition_sequence.append(g)
      self.class_names.append(g)
      self.subclass_names[g] = []
      self.link_lists[g] = []
      self.CLASSES[g] = Graph()
      for s, p, o in graphs[g]:
        subject = makeRDFCompatible(s)
        object = makeRDFCompatible(o)
        if p == "is_a_subclass_of":
          p = PREDICATES["subclass"]
        if p == "link_to_class":
          p = PREDICATES["link"]
        self.CLASSES[g].add((subject, p, object))
        # s, p, o = t
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
      for t in self.CLASSES[cl].triples((None,None,None)):
        graph_overall.add(t)

    dot = plot(graph_overall, self.class_names)
    print("debugging -- dot")
    dot.render("graph", directory=TTLDirectory)
    dot.view()


if __name__ == "__main__":
  import sys

  app = QApplication(sys.argv)

  icon_f = "task_ontology_foundation.svg"
  icon = os.path.join(os.path.abspath("resources/icons"), icon_f)
  app.setWindowIcon(QtGui.QIcon(icon))

  MainWindow = OntobuilderUI()
  MainWindow.show()
  sys.exit(app.exec_())
