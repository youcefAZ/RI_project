"""Some Useful functions."""
import pickle
import json
import numpy as np
import os

def print_dico(dico):
    """Print any dictionary in a json way(more beautiful manner)."""
    return json.dumps(dico, indent=4, sort_keys=True)


def openPkl(filename,pathopen):
    with  open(pathopen+filename,"rb") as file:
        return pickle.load(file)

def savePkl(objname,filename,pathsave):
    """
    objname : nom de l'objet qu'on veut sauvegarder
    filename : sous quel nom on veut le sauvegarder (ajouter .pkl au nom )
    """
    with  open(pathsave+filename,"wb") as file:
        pickle.dump(objname,file,pickle.HIGHEST_PROTOCOL)



def check_pickle(pickle_name,path_pick= "pickle/"):
    """create the pickle file if it doesn't exist
    
    Returns: 
        False if the files doens't exist (it created the directory)
        True if the file exists!
    """

    #path ="/".join(img_path.split("/")[:-1])
    if not os.path.exists(path_pick):
        print("path:\"",path_pick,"\"  doesnt exist so we created it")
        os.makedirs(path_pick)

    if os.path.exists(path_pick+pickle_name):
        return True

    return False


def output_results(type,results):
    f = open("output_weighted/results"+str(type)+".txt", "w")
    for element in results.keys():
        f.write('Threshold : '+str(element)+'    mean precision/recall : '+str(results[element])+'\n')
    
