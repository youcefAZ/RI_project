import numpy as np
from ir import vectorial_model,evaluation
import matplotlib.pyplot as plt


def plotting(pertinent_list,weighted_list,list_doc,request_list) :
    threshold_list=list(np.arange(0.4,0.62,0.02))
    precision_res=[]
    recall_res=[]
    for threshold in threshold_list:
        mean_precision=0
        mean_recall=0
        for j in range(1,len(request_list)+1):
            print('REQUEST : ',j)
            try :
                rsv=vectorial_model(weighted_list,list_doc,request_list[j],3,threshold)
                mean_precision+=evaluation.precision(pertinent_list[j],rsv.keys())
                mean_recall+=evaluation.recall(pertinent_list[j],rsv.keys())
            except Exception:
                print('EXCEPTION IN ',j)
            
        precision_res.append(mean_precision/(len(request_list)-12))
        recall_res.append( mean_recall/(len(request_list)-12))
    
    plt.plot(threshold_list, precision_res, label = "Precision")
    plt.plot(threshold_list, recall_res, label = "Recall")

    plt.xlabel('x - thresholds')
    plt.ylabel('x - score')

    plt.title('Cos function')
    plt.legend()
    plt.show()
        
def plot_request(pertinent_list,weighted_list,list_doc,request_list) :
    request=(range(1,65,1))
    precision_list=[]
    recall_list=[]
    for i in request:
        try :
            rsv=vectorial_model(weighted_list,list_doc,request_list[i],3,0.45)
            precision_list.append(evaluation.precision(pertinent_list[i],rsv.keys())) 
            recall_list.append(evaluation.recall(pertinent_list[i],rsv.keys())) 
        except Exception:
            print('EXCEPTION IN ',i)
            precision_list.append(0)
            recall_list.append(0)
    
    plt.plot(request, precision_list, label = "Precision")
    plt.plot(request, recall_list, label = "Recall")

    plt.xlabel('x - requests')
    plt.ylabel('x - score')

    plt.title('Cos function for every request')
    plt.legend()
    plt.show()