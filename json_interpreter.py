import json



def ReadDialog(language="English", dialog=None):
    
    with open("data/language.json", 'r',encoding='utf-8') as lang_file:
        lang_data = json.load(lang_file)
        
        # for i in include:
        #     try:
        #         del lang_data[i]
        #     except:
        #         print(f"we cannot find the {i} play list. del have not saccesfulled")
        
        if language in lang_data.keys():
            if dialog == None:
                return lang_data
            else:
                return lang_data[language][dialog]
        else:
            raise KeyError(f"In data/language.json file there is no such language as {language}")
        
        
        # with open("data/language.json","w",encoding='utf-8') as file2:
        #     json.dump(lang_data, file2, indent=4)
        
        # return json.dumps(lang_data, ensure_ascii=False) if logs else lang_data