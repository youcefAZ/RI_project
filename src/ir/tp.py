import math

# ouverture du fichier stopwords_fr
stopwordsfile = "stopwords/stopwords_eng.txt"
path='files'
# Récupération de la liste des mots vides
stopwords_list = open(stopwordsfile, "r", encoding="utf-8").read().splitlines()

ponctuation_list = ['?', '.', '!',';', '<', '>', '}', '{', ':', '(', ')', '[', ']', '\"', ',', '-', "»", "«", '\'', '’',
                    '#', '+', '_', '-', '*', '/', '=']


#eliminer ponctuation
def eliminate_punc(text):
    for character in ponctuation_list:
        text = text.replace(character, ' ')
    return text


# Eliminer les mots vides et la ponctuation
def Stopword_elimination(text):
    word_list = []
    # Eliminer la punctuation
    text=eliminate_punc(text)

    # str -> list
    words = text.split()
    for word in words:
        if word.lower() not in stopwords_list:
            word_list.append(word.lower())
    return word_list


# Dictionnaire des fréquences
def dict_freq(word_list):
    """Takes a word_list and outups a dictionary 

    
    Returns 
        {word:frequency,word:frequencey}
    """
    frequence_dict = {} 
    for word in word_list:
        if word not in frequence_dict:
            frequence_dict[word] = word_list.count(word)
    return frequence_dict


#freq of all files
def all_freq(n):  # n est le nombre des documents txt
    i = 1
    frequences = {}
    while (i <= n):
        with open(path+'/D' + str(i) + '.txt', 'r', encoding='utf-8') as file:
            lines = file.read()
            data = Stopword_elimination(lines)
            frequences[i] = dict_freq(data)
        file.close()
        i = i + 1
    
    return frequences #structure is dictionaire dans un dictionaire..


#freq of 1 file
def doc_freq(i) :
    frequences = {}
    with open(path+'/D' + str(i) + '.txt', 'r', encoding='utf-8') as file:
        lines = file.read()
        data = Stopword_elimination(lines)
        frequences = dict_freq(data)
        file.close()
        print(i, ":", frequences)




#verify the number of files that contains term
def freq_term(term,n):
    frequence=0
    for i in range(1,n+1,1):
        with open(path+'/D' + str(i) + '.txt', 'r', encoding='utf-8') as file:
            lines = file.read()
            data = Stopword_elimination(lines)
            if term in data:
                frequence+=1
        file.close()
    return frequence
        

def max_freq(di):
    max=0
    with open(path+'/D' + str(di) + '.txt', 'r', encoding='utf-8') as file:
        lines = file.read()
        data = Stopword_elimination(lines)
        for word in data:
            if data.count(word)>max :
                max=data.count(word)
    return max


#exo3
def weighted_terms(n):
    weighted_freq={}
    for i in range(1,n+1,1):
        with open(path+'/D' + str(i) + '.txt', 'r', encoding='utf-8') as file:
            lines = file.read()
            data = Stopword_elimination(lines)
            max=max_freq(i)
            for word in data:
                freq=data.count(word)
                ni=freq_term(word,n)
                weighted_freq[word,i]=(freq/max)*math.log(n/ni+1,10)
    
    return weighted_freq


def get_weighted_term_list(weighted_list, doc):
    term_list={} 
    for (key,d) in weighted_list:
        if d==doc:
            term_list[key]=weighted_list[key,d]
    
    return term_list


def get_weighted_doc_list(weighted_list, term):
    doc_list={}
    for (key,d) in weighted_list:
        if key==term:
            doc_list[d]=weighted_list[key,d]
    
    return doc_list



if __name__ == "__main__":
    #poids(ti, dj) = (freq(ti,dj)/Max(freq(t, dj))*Log((N/ni) +1)
    freq=all_freq(3)
    freq_term("simple",3)

    wt=weighted_terms(3)

    print(get_weighted_term_list(wt,2))
    print(get_weighted_doc_list(wt,'préparation'))
    

