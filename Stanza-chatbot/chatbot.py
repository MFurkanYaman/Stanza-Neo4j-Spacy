# chatbot.py
from stanza import Pipeline
from db_operations import run_query

nlp = Pipeline('tr')


def process_sentence(sentence):
    """
    Bu fonksiyon gelen soruyu lemmalara böler ve lemma_list'e atar.
    Aynı zamanda veritabanından node isimlerini alır ve onları da
    lemmalara bölerek node_list'e atar.
    """
    lemma_list = []
    node_list = []
    kelime = ""
    
    # Girilen cümlenin lemmalarını al
    doc = nlp(sentence)
    
    for sent in doc.sentences:
        for word in sent.words:
            lemma_list.append(word.lemma)
    
    print("Sorunun lemmaları:", lemma_list)

    # Veritabanındaki düğümlerin lemmalarını al
    query = "MATCH (n) RETURN DISTINCT n.name as db_record;"
    result = run_query(query)

    for record in result:
        kelime += record["db_record"] + " "

    doc2 = nlp(kelime)
    for sent in doc2.sentences:
        for word in sent.words:
            node_list.append(word.lemma)

    print("Database lemmaları: ", node_list)
    return lemma_list, node_list, doc

def get_answer(sentence, lemma_list, node_list):
    node_id = []
    subject = None
    control = False
  
    for i in lemma_list:
        if i.lower() == "ankara":
            continue
        for j in node_list:
            if i == j:
                subject = j
                control = True
                break  # İlk eşleşen konuyu bulduğumuzda döngüden çık
        if control:
            break
    
    print("Liste karşılaştırması sonucu ortak lemma:", subject)

    query_getId = "MATCH (n) RETURN ID(n) AS node_id;"
    result = run_query(query_getId)
   
    for record in result:
        node_id.append(record["node_id"])

    get_id = node_id[node_list.index(subject)]  # İlk eşleşen node'u bulur
    query_getSubject = f"MATCH (n) WHERE ID(n) = {get_id} RETURN n.name as subject;"
    result = run_query(query_getSubject)
    
    for record in result:
        subject = record["subject"]

    query_getAnswer = f"""
    MATCH (n)-[:CONTAINS]->(info)
    WHERE n.name = '{subject}'
    RETURN info.name as result
    """

    result = run_query(query_getAnswer)
    answers = [record['result'] for record in result]
    
    print("get_answer:", answers)
    return answers

def get_correct_suffix(kelime):
    """
    Türkçedeki ses uyumuna göre -dır, -dir, -tır, -tir ekini belirler.
    """
    kalin_unluler = ['a', 'ı', 'o', 'u']
    ince_unluler = ['e', 'i', 'ö', 'ü']
    sert_unsuzler = ['p', 'ç', 't', 'k', 'f', 'h', 's', 'ş']
    
    # Kelimenin son ünlüsünü bul
    son_unlu = ''

    for harf in kelime[::-1]:
        if harf in kalin_unluler + ince_unluler:
            son_unlu = harf
            break
    
    son_unsuz = kelime[-1]  # Kelimenin son harfi

    if son_unlu in kalin_unluler:
        if son_unsuz not in sert_unsuzler:
            ek = 'dır'
        else:
            ek = 'tır'
    elif son_unlu in ince_unluler:
        if son_unsuz not in sert_unsuzler:
            ek = 'dir'
        else:
            ek = 'tir'
    
    return kelime + ek

def answer(db_result, question, doc):
    splited_question=[]
    for sent in doc.sentences:
        for index in sent.words:
            if index.upos == "PRON" or index.upos == "VERB":
                split_id = index.id
    split_id=2
    splited_question=question.split()
    splited_question = splited_question[:split_id-1]
    splited_question.append(":")
    
    answer = splited_question + db_result[::-1]

    # Veritabanı sonucundan son kelimeyi al ve ek getir
    last_word = db_result[-1]
    modified_word = get_correct_suffix(last_word)
    answer.append(modified_word)
    answer = " ".join(answer)
    
    print("Cevap:", answer)
