import sys


from PyQt5.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox

)


from PyQt5.uic import loadUi

from ir  import utilities,app,boolean_model,vectorial_model,tp,evaluation

from ui.main_window_ui import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setupUi(self)

        self.connectSignalsSlots()
        self.main_needed()


    def main_needed(self):
        """all the objects needed from the main.py in ir ect.
        
        Note: 
            TODO: we can optimize this i think """

        app.get_them_all()
        self.list_doc = utilities.openPkl("list_doc.pkl","pickle/")
        self.idf_list = utilities.openPkl("idf_list.pkl","pickle/")
        self.weighted_idf = utilities.openPkl("weighted_idf.pkl","pickle/")


    def connectSignalsSlots(self):
        """ Connecter every signal (bouton ect, to a fonction:).

        Note:
            * The equivalent of triggered of QAtion's triggered in QPushButton is: clicked
        """
        self.search_btn.clicked.connect(self.search) 
        self.search_by_query_btn.clicked.connect(self.search_by_query)
        self.action_About.triggered.connect(self.about)


    def is_empty(self,word):
        """Check if a word is empy.and throw an error if it's the case!.
        """
        if (word==""):
            QMessageBox.about(self, "Search query is empty", 
            "please write your query before clicking the search button")
        else:
            return False


    def radio_is_selected(self):
        """check if one of the QRadioButton  buttions are selected!
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

    def search_by_query(self):
        """
        """
        #check if it's vectorial
        result = ""
        model_selected = self.radio_is_selected()
        if (model_selected == 2): #vect
            query = self.get_query_num()
            pertinent_list_doc = self.get_pertinent_list()

            if query ==None:
                QMessageBox.about(self, "Operation impossible!", 
                    "Please select a query between 1 and 64"
                )
            else:
                result = self.vectorial_query(query)

                # precision and recall!
                if pertinent_list_doc != None and query :
                    prec = evaluation.precision(pertinent_list_doc, result.keys())
                    recall = evaluation.recall(pertinent_list_doc, result.keys())
                    self.recall_field.setText("%.4f" % recall)
                    self.precision_field.setText("%.4f" % prec)
                else: 
                    QMessageBox.about(self, "calculation of recall and precison impossible!", 
                        "WARNING: the pertinent list of the query query number you selected \
                        doesn't exist.\n \
                        Therefore we can't compute percision and recall for them"
                    )
        else:
            QMessageBox.about(self, "Operation not allowed!", 
                    "please select a the vectorial model before searching by queries")

        self.document_result_field.setText(utilities.print_dico(result))

    def get_pertinent_list(self):
        query_selected = self.query_select_box.text()
        try:
            if int(query_selected) >0 and int(query_selected) <65: 
                pertinent_list = utilities.openPkl("pertinent_list.pkl","pickle/")
                pertinent_docs = pertinent_list[int(query_selected)]
            else:
                return 
            
        except Exception as e:
            # TODO:handle this exception better
            print("ERROR: \"",e,"\" In get_pertinent_list")
            return
        return pertinent_docs


    def search(self):
        """What we will do when doing seach
        * check if the `seach_field` QlineEdit object is not empty
        * check if it's the boolean 
            1.try to disable or something, the precision and recall and choose function widgets?
        * perform the search using some function from the `boolean_model.py`
    
        """
        print(self.threshold_field.text())
        print(self.query_select_box.text())
        
        result = ""
        query = self.search_field.text()
        model_selected = self.radio_is_selected()
        
        if (not self.is_empty(query)):
            #TODO check if a QRadioButton is selectioned

            if(model_selected ==1):#bool
                result = self.boolean_query(query)


            elif (model_selected ==2):#vect

                # tokenize and do the things to the query
                query = tp.Stopword_elimination(query)
                query =tp.dict_freq(query)

                self.vectorial_query(query)
            else:
                #TODO: handle bettter!
                print("ERROR") 
                return


            # TODO: print them by the priority?? (best score)
            self.document_result_field.setText(utilities.print_dico(result))

        # self.recall_field.setText("gekko") --TO SET A TEXT in a QTextBrowser!

    def vectorial_query(self,query,use_weighted_idf=True):
        """Perform vectorial query!!.
        query   --    a request in this form :ex {'articles': 1, 'exist': 1, 'deal': 1,...}
        """
        threashold = float(self.threshold_field.text())

        rsv_func = self.get_rsv_function()
        if use_weighted_idf :
            result = vectorial_model.vectorial_model(self.weighted_idf, self.list_doc, query, rsv_func, threshold=threashold)
        else: 
            result = vectorial_model.vectorial_model(self.idf_list,self.list_doc,query,rsv_func,threshold=threashold)

        return result


    def boolean_query(self,query):
        """perfrm boolean query
        """
        result = boolean_model.boolean_model(query, self.list_doc)
        return result


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
        


    def get_query_num(self):
        """if the input is a number between 1 and 64
        then we will take the file from qrels
        """
        query_selected = self.query_select_box.text()

        try:
            if int(query_selected) >0 and int(query_selected) <65: 
                request_list = utilities.openPkl("request_list.pkl","pickle/")
                query = request_list[int(query_selected)]
                print("query is:",query)
                #pertinent_list = utilities.openPkl("pertinent_list.pkl","pickle/")
            else: 
                QMessageBox.about(self, "Query doesn't exist!", 
                    "please select a query number between 1 and 64")
                return 
        except:
            #TODO: handle better
            print("ERROR, in get_query_num")
            exit()

        return query 


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