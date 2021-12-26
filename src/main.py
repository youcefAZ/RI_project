import sys


from PyQt5.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox

)


from PyQt5.uic import loadUi

from ir  import utilities,app,boolean_model,vectorial_model,tp

from ui.main_window_ui import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setupUi(self)

        self.connectSignalsSlots()
        self.main_needed()

    def main_needed(self):
        """all the objects needed from the main.py in ir ect.
        TODO:check if the files exists in pickle/ folder and create them
        if not"""
        self.list_doc = utilities.openPkl("list_doc.pkl","pickle/")
        self.idf_list = utilities.openPkl("idf_list.pkl","pickle/")
        self.weighted_idf = utilities.openPkl("weighted_idf.pkl","pickle/")


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

        Returns:
            1 : boolean selected
            2 : vectorielle selected
            0 : No one selected
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
            # TODO: prompt an Error instead of a QMessageBox
            QMessageBox.about(self, "Model not selected", 
            "please select one of the moodels boolean or vectorial")
            return False


    def search(self):
        """TODO:
        What we will do when doing seach
        * check if the `seach_field` QlineEdit object is not empty
        * check if it's the boolean 
            1.try to disable or something, the precision and recall and choose function widgets?
        * perform the search using some function from the `boolean_model.py`
        * put the result in `document_result_field` QTableView object.
        TODO: use weightd idf!
        """
        query = self.search_field.text()
        result = ""
        model_selected = self.radio_is_selected()
        if (not self.is_empty(query)):
            #TODO check if a QRadioButton is selectioned
            if(model_selected ==1):#bool
                #get the query
                result = boolean_model.boolean_model(query, self.list_doc)

            elif (model_selected ==2):#vect
                # tokenize and do the things to the query
                query = self.get_query(query)
                rsv_func = self.get_rsv_function()
                result = vectorial_model.vectorial_model(self.idf_list,self.list_doc,query,rsv_func,0)
                #TODO choisir fonction
            else:
                #TODO: handle bettter!
                print("ERROR") 

            self.document_result_field.setText(utilities.print_dico(result))

        # self.recall_field.setText("gekko") --TO SET A TEXT in a QTextBrowser!

    def get_rsv_function(self):
        """get the rsv choosen, the default is 1"""
        if (self.function_chs_cbx.currentText() =="Inner product"):
            return 1
        elif (self.function_chs_cbx.currentText() =="Dice coef"):
            return 2
        elif (self.function_chs_cbx.currentText() =="Cosinus"): 
            return 3
        elif (self.function_chs_cbx.currentText() =="Jaccard"):
            return 4
        else:
            exit("ERROR IN COMBOBOX")
        


    def get_query(self,query):
        """if the input is a number between 1 and 64
        then we will take the file from qrels
        otherwise we will do the tokenization thing and return it.
        """
        try:
            if int(query) >0 and int(query) <65: #TODO:make sure it's the right number
                request_list = utilities.openPkl("request_list.pkl","pickle/")
                query = request_list[int(query)]
                #pertinent_list = utilities.openPkl("pertinent_list.pkl","pickle/")
            else:
                query = tp.Stopword_elimination(query)
                query =tp.dict_freq(query)


        except:
                query = tp.Stopword_elimination(query)
                query =tp.dict_freq(query)
        return query 

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


if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())