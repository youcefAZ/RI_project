import sys


from PyQt5.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox

)


from PyQt5.uic import loadUi

from ir  import utilities,main,boolean_model,vectorial_model,tp

from ui.main_window_ui import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setupUi(self)

        self.connectSignalsSlots()
        self.main_needed()

    def main_needed(self):

        """all the objects needed from the main.py in ir ect"""
        self.doc = main.read_data()
        print("hay")


    def connectSignalsSlots(self):
        # TODO: Connecter chaque signal (bouton ect, a une fonction:)
        # The equivalent of triggered of QAtion's triggered in QPushButton is: clicked
        self.search_btn.clicked.connect(self.search) 

        '''self.action_Find_Replace.triggered.connect(self.findAndReplace)

        '''
        self.action_About.triggered.connect(self.about)

    def is_empty(self,word):
        """
            check if a word is empy.
            and throw an error if it's the case!
        """
        if (word==""):
            QMessageBox.about(self, "Search query is empty", 
            "please write your query before clicking the search button")
        else:
            return False
    def radio_is_selected(self):
        """
            check if one of the QRadioButton  buttions are selected!

            `boolean_radio` or
            `vectorielle_radio`
        """
        if (self.boolean_radio.isChecked() and self.vectorielle_radio.isChecked()):
            # this is normaly not possible TODO:throw an error
            exit("EROORRR")
        elif(self.boolean_radio.isChecked()):
            return 1
        elif(self.vectorielle_radio.isChecked()):
            return 2
        else:
            # No button is selected
            # TODO: prompt  a UI to tell the user to do something!
            QMessageBox.about(self, "Model not selected", 
            "please select one of the moodels boolean or vectorial")
        self.boolean_radio.isChecked()
        self.vectorielle_radio.isChecked()

        pass
    
    def search(self):
        """TODO:
        What we will do when doing seach
        * check if the `seach_field` QlineEdit object is not empty
        * check if it's the boolean 
            1.try to disable or something, the precision and recall and choose function widgets?
        * perform the search using some function from the `boolean_model.py`
        * put the result in `document_result_field` QTableView object.

        """
        query = self.search_field.text()
        print(self.doc)
        print(self.boolean_radio)
        model_selected = self.radio_is_selected()
        if (not self.is_empty(query)):
            #TODO check if a QRadioButton is selectioned
            if(model_selected ==1):
                #get the query
                pass


        # self.recall_field.setText("gekko") --TO SET A TEXT in a QTextBrowser!

        self.document_result_field.setText("helloo")


    def findAndReplace(self):

        dialog = FindReplaceDialog(self)

        dialog.exec()


    def about(self):

        QMessageBox.about(
            self,
            "About this Application",
            "<p>Built with &#9829; Time and lack of sleep by</p>"
            "<p>- Abdelhak Aissat</p>"
            "<p>- Youcef Azouaoui</p>"
            "<p>- The help of the guys at RealPython.com</p>",
        )

"""
class TableModel(QAbstractTableModel):
    # TODO:get it , it's raouf's shit

    def __init__(self, data, header):
        super(TableModel, self).__init__()
        self._data = data
        self._header = header

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            
            return self._data[index.row()][index.column()]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._header[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


"""

class FindReplaceDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        loadUi("ui/find_replace.ui", self)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())