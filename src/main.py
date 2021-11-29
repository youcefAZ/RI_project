import tp

stopwordsfile='stopwords/stopwords_eng.txt'
datapath='data/cacm.all'
stopword_list=open(stopwordsfile, "r", encoding="utf-8").read().splitlines()

#from file, makes dictionarry with doc_id as its key, and
#title+ resume as its content
def read_data() :
    docs={}
    with open(datapath, 'r+', encoding='utf-8') as file:
        res=''
        title=''
        for lines in file :
            if (lines[0]=='.') & (lines[1]=='I') :
                id=lines.strip('.I ')
                id=id.strip()

            if (lines[0]=='.') & (lines[1]=='T'):
                nex=next(file).strip()
                while nex[0]!='.' :
                    title=title+' '+nex
                    nex=next(file).strip()
            
                if (nex[0]=='.') & (nex[1]=='W'):
                    nex=next(file).strip()
                    while nex[0]!='.' :
                        res=res+' '+nex
                        nex=next(file).strip()
                
            if (lines[0]=='.') & (lines[1]=='X'):
                docs[id]={'title':title,'resume':res}
                res=''
                title=''

    file.close()
    return docs


def tokenization(docs) :
    detailed_doc={}
    for key in docs:
        title=doc[key]['title']
        resume=doc[key]['resume']
        
        title = tp.Stopword_elimination(title)
        resume = tp.Stopword_elimination(resume)

        detailed_doc[key]={'title':title,'resume':resume}
        
    return detailed_doc
        


doc=read_data()
det=tokenization(doc)
print(det)