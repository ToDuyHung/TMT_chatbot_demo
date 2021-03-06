import re
import numpy as np 
import pandas as pd 

from sklearn.feature_extraction.text import TfidfVectorizer  
from sklearn.model_selection import train_test_split  
from sklearn import svm,metrics
import pickle
import joblib

import re  
import nltk 
nltk.download('stopwords')  
from nltk.corpus import stopwords 
import unidecode

# %matplotlib inline
# from constant import clf, INTENT_THRESHOLD, TYPE_NAME_SEARCH_TTHC, list_chiphi_notification, list_giayto_notification, \
#     list_ketqua_notification, list_thoigian_notification, list_thuchien_notification, list_diadiem_notification
# from query import search
# from functools import reduce


# def searchTTHC(type_database, query):
#     query = preprocess_message(query)
#     [result, info] = search(type_database, query)
#     if len(result) > 0:
#         TTHC = list(map(lambda x: list(map(lambda y: {y[0]: y[1]}, x.items())), result))
#         return [flatten(TTHC), info]
#     return [[],{'type': 'unknown', 'count': 0}]


def catch_intent(message):
    message = preprocess_message(message)
    print(message)

    # intent = extract_and_get_intent(message)
    # if intent != 'none':
    #     return intent
    return predict_message(message)

def corpus_from_file(corpus_path):
    full = pd.read_csv(corpus_path, sep='\n', header=None)
    full = full.dropna()
    X_corp = full.values
    corpus = preprocess(X_corp, rm_short=True)
    return corpus

def make_tfidf_model(corpus=None, save_path = None, pretrained_path = None):
    if pretrained_path is None:
        tfidfconverter = TfidfVectorizer(max_features=10000)  
        tfidfconverter = tfidfconverter.fit(corpus)
        if save_path is not None:
            pickle.dump(tfidfconverter, open(save_path, 'wb'))
            print("Model is saved to ", save_path)
    else:
        tfidfconverter = pickle.load(open(pretrained_path, 'rb'))
        print("Model is loaded from ", pretrained_path)

    return tfidfconverter  

def preprocess(doc, rm_short=False):
    results = []
    for i in range(len(doc)):  
        result = str(doc[i]).lower()

        result = re.sub('^kh??ch.*:', '', result)
        result = re.sub('\W', ' ', str(result))
        result = re.sub('\s+', ' ', result, flags=re.I)
        result = re.sub('^\s|\s$', '', result)
        result = re.sub('.*: ', '', result)

        if len(result) > 2 or rm_short is False:
            results.append(result)
    return results  

def predict_message(message):

    X_corp = np.array([message])

    #Check color
    check_color = False
    tfidfconverter = pickle.load(open('tfidf_color.pickle', 'rb'))
    clf = pickle.load(open('color_pickle', 'rb'))
    X_corp_tfidf = tfidfconverter.transform(X_corp).toarray()
    y_corp_pred = clf.predict(X_corp_tfidf)
    if int(y_corp_pred[0]) == 1:
        check_color = True


    
    
    intent_list = ['hello', 'done', 'inform', 'request', 'feedback', 'connect', 'order', 'changing', 'return']

    #Check hello
    # corpus = corpus_from_file(corpus_path = 'Output2.txt')
    # tfidfconverter = make_tfidf_model(corpus, pretrained_path='tfidf.pickle')
    tfidfconverter = pickle.load(open('tfidf.pickle', 'rb'))
    clf = pickle.load(open('hungne', 'rb'))
    X_corp_tfidf = tfidfconverter.transform(X_corp).toarray()
    y_corp_pred = clf.predict(X_corp_tfidf)
    intent = int(y_corp_pred[0])
    if intent >= 0 and intent <= 8:
        if intent == 6:
            if check_color == True:
                return 'rep_' + intent_list[intent] 
            else:
                return 'rep_' + intent_list[intent] + '_color'
        else:
            return 'rep_' + intent_list[intent] 
    else:
        return 'nothing'
    
    
    


    #Check size
    # tfidfconverter = pickle.load(open('tfidf_size.pickle', 'rb'))
    # clf = pickle.load(open('size_pickle', 'rb'))
    # X_corp_tfidf = tfidfconverter.transform(X_corp).toarray()
    # y_corp_pred = clf.predict(X_corp_tfidf)
    # if int(y_corp_pred[0]) ==1:
    #     check2=True
    # else:
    #     check2=False
    # # if check2==True:
    # #     return "size"
    # print("check2")
    # print (check2)

    # if check1==True and check2==True:
    #     return "color_size"
    # if check3==True:
    #     return "rep_hello"
    # if check1==True and check2==False:
    #     return "color"   
    # if check1==False and check2==True:
    #     return "size"
    # if check1==False and check2==False:
    #     return "nothing"



    # #tfidf_converter
    # tfidfconverter = pickle.load(open('tfidf.pickle', 'rb'))
    # tfidfconverter = pickle.load(open('tfidf.pickle', 'rb'))
    # clf = pickle.load(open('module_pickle', 'rb'))
    # X_corp_tfidf = tfidfconverter.transform(X_corp).toarray()
    # y_corp_pred = clf.predict(X_corp_tfidf)
    # if int(y_corp_pred[0]) ==1:
    #     return True
    # else:
    #     return False
    # predict_result = clf.predict(message)

    # proba = max(predict_result[2].numpy()) * 100

    # if (proba < INTENT_THRESHOLD):
    #     return 'none'

    # return get_name_intent(int(predict_result[0]))


# def extract_and_get_intent(message):
#     for notification in list_chiphi_notification:
#         if message.lower().find(notification) != -1:
#             return 'chiphi'

#     for notification in list_diadiem_notification:
#         if message.lower().find(notification) != -1:
#             return 'diadiem'

#     for notification in list_thoigian_notification:
#         if message.lower().find(notification) != -1:
#             return 'thoigian'

#     for notification in list_ketqua_notification:
#         if message.lower().find(notification) != -1:
#             return 'ketqua'

#     for notification in list_thuchien_notification:
#         if message.lower().find(notification) != -1:
#             return 'thuchien'

#     for notification in list_giayto_notification:
#         if message.lower().find(notification) != -1:
#             return 'giayto'

#     return 'none'


# def get_name_tthc(message):
#     if 'l??nh v???c' in message.lower():
#         filter_message = re.sub(r"^.*?(l??nh v???c)", '', message.lower())
#         type_name = TYPE_NAME_SEARCH_TTHC.LINH_VUC
#         return [filter_message, type_name]

#     if 'c???a' in message.lower():
#         filter_message = re.sub(r"^.*?(c???a)", '', message.lower())
#         type_name = TYPE_NAME_SEARCH_TTHC.CO_QUAN
#         return [filter_message, type_name]

#     filter_message = re.sub(
#         r"^.*?((th??? t???c)|(c??ch l??m)|(c??ch))", '', message.lower())
#     type_name = TYPE_NAME_SEARCH_TTHC.THU_TUC
#     return [filter_message, type_name]


def preprocess_message(message):
    message = re.sub(
        '[\:\_=\+\#\@\$\%\$\\(\)\~\@\;\'\|\<\>\]\[\"\????????????*]', ' ', message)

    message = message.lower()
    message = message.replace(',', ' , ')
    message = message.replace('.', ' . ')
    message = message.replace('!', ' ! ')
    message = message.replace('&', ' & ')
    message = message.replace('?', ' ? ')
    message = message.replace('(', ' ( ')
    message = message.replace(')', ' ) ')
    message = compound2unicode(message)
    list_token = message.split(' ')
    while '' in list_token:
        list_token.remove('')
    message = ' '.join(list_token)
    return message


def compound2unicode(text):
    # https://gist.github.com/redphx/9320735`
    text = text.replace("\u0065\u0309", "\u1EBB")  # ???
    text = text.replace("\u0065\u0301", "\u00E9")  # ??
    text = text.replace("\u0065\u0300", "\u00E8")  # ??
    text = text.replace("\u0065\u0323", "\u1EB9")  # ???
    text = text.replace("\u0065\u0303", "\u1EBD")  # ???
    text = text.replace("\u00EA\u0309", "\u1EC3")  # ???
    text = text.replace("\u00EA\u0301", "\u1EBF")  # ???
    text = text.replace("\u00EA\u0300", "\u1EC1")  # ???
    text = text.replace("\u00EA\u0323", "\u1EC7")  # ???
    text = text.replace("\u00EA\u0303", "\u1EC5")  # ???
    text = text.replace("\u0079\u0309", "\u1EF7")  # ???
    text = text.replace("\u0079\u0301", "\u00FD")  # ??
    text = text.replace("\u0079\u0300", "\u1EF3")  # ???
    text = text.replace("\u0079\u0323", "\u1EF5")  # ???
    text = text.replace("\u0079\u0303", "\u1EF9")  # ???
    text = text.replace("\u0075\u0309", "\u1EE7")  # ???
    text = text.replace("\u0075\u0301", "\u00FA")  # ??
    text = text.replace("\u0075\u0300", "\u00F9")  # ??
    text = text.replace("\u0075\u0323", "\u1EE5")  # ???
    text = text.replace("\u0075\u0303", "\u0169")  # ??
    text = text.replace("\u01B0\u0309", "\u1EED")  # ???
    text = text.replace("\u01B0\u0301", "\u1EE9")  # ???
    text = text.replace("\u01B0\u0300", "\u1EEB")  # ???
    text = text.replace("\u01B0\u0323", "\u1EF1")  # ???
    text = text.replace("\u01B0\u0303", "\u1EEF")  # ???
    text = text.replace("\u0069\u0309", "\u1EC9")  # ???
    text = text.replace("\u0069\u0301", "\u00ED")  # ??
    text = text.replace("\u0069\u0300", "\u00EC")  # ??
    text = text.replace("\u0069\u0323", "\u1ECB")  # ???
    text = text.replace("\u0069\u0303", "\u0129")  # ??
    text = text.replace("\u006F\u0309", "\u1ECF")  # ???
    text = text.replace("\u006F\u0301", "\u00F3")  # ??
    text = text.replace("\u006F\u0300", "\u00F2")  # ??
    text = text.replace("\u006F\u0323", "\u1ECD")  # ???
    text = text.replace("\u006F\u0303", "\u00F5")  # ??
    text = text.replace("\u01A1\u0309", "\u1EDF")  # ???
    text = text.replace("\u01A1\u0301", "\u1EDB")  # ???
    text = text.replace("\u01A1\u0300", "\u1EDD")  # ???
    text = text.replace("\u01A1\u0323", "\u1EE3")  # ???
    text = text.replace("\u01A1\u0303", "\u1EE1")  # ???
    text = text.replace("\u00F4\u0309", "\u1ED5")  # ???
    text = text.replace("\u00F4\u0301", "\u1ED1")  # ???
    text = text.replace("\u00F4\u0300", "\u1ED3")  # ???
    text = text.replace("\u00F4\u0323", "\u1ED9")  # ???
    text = text.replace("\u00F4\u0303", "\u1ED7")  # ???
    text = text.replace("\u0061\u0309", "\u1EA3")  # ???
    text = text.replace("\u0061\u0301", "\u00E1")  # ??
    text = text.replace("\u0061\u0300", "\u00E0")  # ??
    text = text.replace("\u0061\u0323", "\u1EA1")  # ???
    text = text.replace("\u0061\u0303", "\u00E3")  # ??
    text = text.replace("\u0103\u0309", "\u1EB3")  # ???
    text = text.replace("\u0103\u0301", "\u1EAF")  # ???
    text = text.replace("\u0103\u0300", "\u1EB1")  # ???
    text = text.replace("\u0103\u0323", "\u1EB7")  # ???
    text = text.replace("\u0103\u0303", "\u1EB5")  # ???
    text = text.replace("\u00E2\u0309", "\u1EA9")  # ???
    text = text.replace("\u00E2\u0301", "\u1EA5")  # ???
    text = text.replace("\u00E2\u0300", "\u1EA7")  # ???
    text = text.replace("\u00E2\u0323", "\u1EAD")  # ???
    text = text.replace("\u00E2\u0303", "\u1EAB")  # ???
    text = text.replace("\u0045\u0309", "\u1EBA")  # ???
    text = text.replace("\u0045\u0301", "\u00C9")  # ??
    text = text.replace("\u0045\u0300", "\u00C8")  # ??
    text = text.replace("\u0045\u0323", "\u1EB8")  # ???
    text = text.replace("\u0045\u0303", "\u1EBC")  # ???
    text = text.replace("\u00CA\u0309", "\u1EC2")  # ???
    text = text.replace("\u00CA\u0301", "\u1EBE")  # ???
    text = text.replace("\u00CA\u0300", "\u1EC0")  # ???
    text = text.replace("\u00CA\u0323", "\u1EC6")  # ???
    text = text.replace("\u00CA\u0303", "\u1EC4")  # ???
    text = text.replace("\u0059\u0309", "\u1EF6")  # ???
    text = text.replace("\u0059\u0301", "\u00DD")  # ??
    text = text.replace("\u0059\u0300", "\u1EF2")  # ???
    text = text.replace("\u0059\u0323", "\u1EF4")  # ???
    text = text.replace("\u0059\u0303", "\u1EF8")  # ???
    text = text.replace("\u0055\u0309", "\u1EE6")  # ???
    text = text.replace("\u0055\u0301", "\u00DA")  # ??
    text = text.replace("\u0055\u0300", "\u00D9")  # ??
    text = text.replace("\u0055\u0323", "\u1EE4")  # ???
    text = text.replace("\u0055\u0303", "\u0168")  # ??
    text = text.replace("\u01AF\u0309", "\u1EEC")  # ???
    text = text.replace("\u01AF\u0301", "\u1EE8")  # ???
    text = text.replace("\u01AF\u0300", "\u1EEA")  # ???
    text = text.replace("\u01AF\u0323", "\u1EF0")  # ???
    text = text.replace("\u01AF\u0303", "\u1EEE")  # ???
    text = text.replace("\u0049\u0309", "\u1EC8")  # ???
    text = text.replace("\u0049\u0301", "\u00CD")  # ??
    text = text.replace("\u0049\u0300", "\u00CC")  # ??
    text = text.replace("\u0049\u0323", "\u1ECA")  # ???
    text = text.replace("\u0049\u0303", "\u0128")  # ??
    text = text.replace("\u004F\u0309", "\u1ECE")  # ???
    text = text.replace("\u004F\u0301", "\u00D3")  # ??
    text = text.replace("\u004F\u0300", "\u00D2")  # ??
    text = text.replace("\u004F\u0323", "\u1ECC")  # ???
    text = text.replace("\u004F\u0303", "\u00D5")  # ??
    text = text.replace("\u01A0\u0309", "\u1EDE")  # ???
    text = text.replace("\u01A0\u0301", "\u1EDA")  # ???
    text = text.replace("\u01A0\u0300", "\u1EDC")  # ???
    text = text.replace("\u01A0\u0323", "\u1EE2")  # ???
    text = text.replace("\u01A0\u0303", "\u1EE0")  # ???
    text = text.replace("\u00D4\u0309", "\u1ED4")  # ???
    text = text.replace("\u00D4\u0301", "\u1ED0")  # ???
    text = text.replace("\u00D4\u0300", "\u1ED2")  # ???
    text = text.replace("\u00D4\u0323", "\u1ED8")  # ???
    text = text.replace("\u00D4\u0303", "\u1ED6")  # ???
    text = text.replace("\u0041\u0309", "\u1EA2")  # ???
    text = text.replace("\u0041\u0301", "\u00C1")  # ??
    text = text.replace("\u0041\u0300", "\u00C0")  # ??
    text = text.replace("\u0041\u0323", "\u1EA0")  # ???
    text = text.replace("\u0041\u0303", "\u00C3")  # ??
    text = text.replace("\u0102\u0309", "\u1EB2")  # ???
    text = text.replace("\u0102\u0301", "\u1EAE")  # ???
    text = text.replace("\u0102\u0300", "\u1EB0")  # ???
    text = text.replace("\u0102\u0323", "\u1EB6")  # ???
    text = text.replace("\u0102\u0303", "\u1EB4")  # ???
    text = text.replace("\u00C2\u0309", "\u1EA8")  # ???
    text = text.replace("\u00C2\u0301", "\u1EA4")  # ???
    text = text.replace("\u00C2\u0300", "\u1EA6")  # ???
    text = text.replace("\u00C2\u0323", "\u1EAC")  # ???
    text = text.replace("\u00C2\u0303", "\u1EAA")  # ???
    return text


# def get_name_intent(id):
#     if id == 0:
#         return 'chiphi'
#     if id == 1:
#         return 'diadiem'
#     if id == 2:
#         return 'giayto'
#     if id == 3:
#         return 'ketqua'
#     if id == 4:
#         return 'thoigian'
#     if id == 5:
#         return 'thuchien'
#     return 'none'


def update(a, b):
    a.update(b)
    return a


def flatten(result):
    return list(map(lambda x: reduce(update, x), result))