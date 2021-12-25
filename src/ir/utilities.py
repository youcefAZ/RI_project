"""Some Useful functions."""
import pickle
import json
import numpy as np


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



def output_results(type,results):
    f = open("output/results"+str(type)+".txt", "w")
    for element in results.keys():
        f.write('Threshold : '+str(element)+'    mean precision/recall : '+str(results[element])+'\n')
    
