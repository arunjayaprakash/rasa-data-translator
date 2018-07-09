from googletrans import Translator
import json
import copy
import sys

source = sys.argv[1]
lang = sys.argv[2]

translator = Translator()
new_json = {
    "rasa_nlu_data":{
        "common_examples":[],
        "regex_features": []
    }
}

with open(source, "r", encoding='utf-8-sig') as read_file:
    original_json = json.load(read_file)
    common_examples_arr = original_json["rasa_nlu_data"]["common_examples"]
    
    for x in common_examples_arr:
        data = dict()
        
        #intent,text translated
        data["text"] = translator.translate(x["text"],dest=lang).text
        data["intent"]=x["intent"]
        data["entities"]=[]

        # translate entity
        for y in x["entities"]:
            data_entity = dict()
            data_entity["value"]=y["value"]
            data_entity["entity"]=y["entity"]
            start_index = data["text"].find(data_entity["value"])
            end_index = start_index + len(data_entity["value"])
            data_entity["start"] = start_index
            data_entity["end"] = end_index
            data["entities"].append(data_entity)
        new_json["rasa_nlu_data"]["common_examples"].append(data)
     
    try:
        regex_features_arr = original_json["rasa_nlu_data"]["regex_features"]
        for y in regex_features_arr:
            data = dict()
            data["name"] = y["name"]
            data["pattern"] = y["pattern"]
            new_json["rasa_nlu_data"]["regex_features"].append(data)
    except KeyError:
        pass

if '/' in source:
    file_name='/'.join(source.split('/')[:-1])+'/'+"test_"+lang+".json"
else:
    file_name="test_"+lang+".json"
with open(file_name, 'w') as f:
    json.dump(new_json, f, indent=4)