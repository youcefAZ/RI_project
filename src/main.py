import tp

datapath='data/cacm.all'


def read_data() :
    docs={}
    with open(datapath, 'r+', encoding='utf-8') as file:
        res=''
        for lines in file :
            if (lines[0]=='.') & (lines[1]=='I') :
                id=lines.strip('.I ')

            elif (lines[0]=='.') & (lines[1]=='T'):
                title=next(file).strip()
            
            elif (lines[0]=='.') & (lines[1]=='W'):
                nex=next(file).strip()
                while nex[0]!='.' :
                    res=res+nex
                    nex=next(file).strip()
                
            elif (lines[0]=='.') & (lines[1]=='X'):
                docs[id]={title,res}
                res=''
                print(id,docs[id])


    file.close()

read_data()