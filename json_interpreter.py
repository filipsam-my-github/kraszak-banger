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
        
def ReadItems(language, *args):
    with open("data/language.json", 'r',encoding='utf-8') as lang_file:
        lang_data = json.load(lang_file)
        
        # for i in include:
        #     try:
        #         del lang_data[i]
        #     except:
        #         print(f"we cannot find the {i} play list. del have not saccesfulled")
        items = []
        
        for item_i in args:
            if type(item_i) != str:
                for item_j in item_i:
                    if language in lang_data.keys():#
                        if item_j == None:
                            items.append(lang_data)
                        else:
                            items.append(lang_data[language][item_j])
                    else:
                        raise KeyError(f"In data/language.json file there is no such language as {language}")
            else:
                if language in lang_data.keys():
                    if item_i == None:
                        items.append(lang_data)
                    else:
                        items.append(lang_data[language][item_i])
                else:
                    raise KeyError(f"In data/language.json file there is no such language as {language}")
        return items
        
print(ReadItems("English", "funny_thing", ("funny_thing", "funny_thing")))