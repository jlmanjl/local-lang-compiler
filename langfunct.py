import os
import pandas as pd
import docx

def path_dict_generator(path):

    copy_filepath_dict = {}
    
    spanish_abr = ["_SPA", "_ES_", "ES "]
    german_abr = ["_GER", "_DE_", "DE "]
    french_abr = ["_FRE", "_FR_", "FR "]
    brazport_abr = ["_POR", "_PTBR_", "BR "]
    dutch_abr = ["_NL", "_NL_", "NL "]


    for file in os.listdir(path):
        print(file)
        if file.endswith(".doc") or file.endswith(".docx"):
            if file.startswith("ES_") or "_SPA" in file or "_ES_" in file:
                copy_filepath_dict["ES"] = path + "/" + file
            elif file.startswith("DE_") or "_GER" in file or "_DE_" in file:
                copy_filepath_dict["DE"] = path + "/" + file
            elif file.startswith("FR_") or "_FRE" in file or "_FR_" in file:
                copy_filepath_dict["FR"] = path + "/" + file
            elif file.startswith("BR_") or "_POR" in file or "_PTBR_" in file:
                copy_filepath_dict["BR"] = path + "/" + file
            elif file.startswith("NL_") or "_NL" in file or "_NL_" in file:
                copy_filepath_dict["NL"] = path + "/" + file
            else:
                copy_filepath_dict["EN"] = path + "/" + file
        else:
            continue

    print(copy_filepath_dict)
    #copy_filepath_dict["EN"] = copy_filepath_dict.pop("EN")
    
    print(copy_filepath_dict)
    return copy_filepath_dict

def generate_copy_list(filepath):
    data = []
    document = docx.Document(filepath)
    table = document.tables[1] #grab content table from .docx

    for row in table.rows:
        row_data = []
        for cell in row.cells:
            row_data.append(cell.text)
        data.append(row_data)

    df = pd.DataFrame(data, columns=["Message Type", "Message"])
    df2 = df[4:] #All content after "Modal Message" row
    df2.reset_index() #resets index for iterations

    #Create a list of all the copy
    copy_list = []
    for index, row in df2.iterrows():
        text = row['Message'].splitlines()
        copy_list.append(text)
    
    return copy_list
     
def copy_lang_dict_generator(copy_filepath_dict):
    copy_language_dict = {}
    for key, filepath in copy_filepath_dict.items():
        i = generate_copy_list(filepath)
        copy_language_dict[key] = i

    return copy_language_dict


#filters out any blank values caused by line breaks from the copy list 
def update_copy_dictionary(copy_list):
    copy_dict_list = []
    for item in copy_list: # iterates over all the copy in the doc i.e. each slide/section
        # print(item)
        item = list(filter(lambda a: a != '', item))
        #item = list(filter(lambda a: a != '[Button]', item))  
        item = list(filter(lambda a: a != 'Modal message', item))  
        #item = [ s for s in item if not re.search(r'\[[^\]]*\]',s) ] #filters out anything in between two square brackets
        # item = list(filter(lambda a: re.search(r'\[[^\]]*\]', item), item))
        # print(item)
        list_of_copy = []
        for line in item: #iterates over a single cell of copy i.e. headings, copy, buttons
            list_of_copy.append(line)
        copy_dict_list.append(list_of_copy)
                
                
    return copy_dict_list

def updating_language_dict(copy_language_dict):
    updated_language_dict = {}
    for key, copy_list in copy_language_dict.items():
        new_value = update_copy_dictionary(copy_list)
        updated_language_dict[key] = new_value
        print("success for " + key)
    return updated_language_dict

def print__output(updated_language_dict):
    message_list = []
    first_key = list(updated_language_dict.keys())[0]
    try:
        for c in range(len(updated_language_dict[first_key])):
            for i in range(len(updated_language_dict[first_key][c])):
                message_fragments = []
                ## Edit here for additional langs
                if "ES" in updated_language_dict.keys():
                    ES = """{% when "es-ES","es","ES" %}<br>""" + updated_language_dict["ES"][c][i] + '\n'
                    message_fragments.append(ES)
                else:
                    pass
                if "FR" in updated_language_dict.keys():
                    FR = """{% when "fr-FR","fr","FR" %}<br>""" + updated_language_dict["FR"][c][i] + '\n'
                    message_fragments.append(FR)
                else:
                    pass
                if "DE" in updated_language_dict.keys():
                    DE = """{% when "de-DE","de","DE" %}<br>""" + updated_language_dict["DE"][c][i] + '\n'
                    message_fragments.append(DE)            
                else:           
                    pass           
                if "NL" in updated_language_dict.keys():           
                    NL = """{% when "nl-NL","nl","NL" %}<br>""" + updated_language_dict["NL"][c][i] + '\n'
                    message_fragments.append(NL)            
                else:           
                    pass           
                if "BR" in updated_language_dict.keys():           
                    BR = """{% when "pt-BR","br","BR" %}<br>""" + updated_language_dict["BR"][c][i] + '\n'
                    message_fragments.append(BR)           
                else:
                    pass 
                if "EN" in updated_language_dict.keys():
                    EN = """{% else %}<br>""" + updated_language_dict["EN"][c][i]
                    message_fragments.append(EN) 
                else:
                    pass

                message = '<br>'.join(message_fragments)

                message_list.append(message)
    except IndexError:
        for c in range(len(updated_language_dict["EN"])):
            for i in range(len(updated_language_dict["EN"][c])):
                message_fragments = []
                ## Edit here for additional langs
                if "ES" in updated_language_dict.keys():
                    ES = """{% when "es-ES","es","ES" %}<br>""" + updated_language_dict["ES"][c][i] + '\n'
                    message_fragments.append(ES)
                else:
                    pass
                if "FR" in updated_language_dict.keys():
                    FR = """{% when "fr-FR","fr","FR" %}<br>""" + updated_language_dict["FR"][c][i] + '\n'
                    message_fragments.append(FR)
                else:
                    pass
                if "DE" in updated_language_dict.keys():
                    DE = """{% when "de-DE","de","DE" %}<br>""" + updated_language_dict["DE"][c][i] + '\n'
                    message_fragments.append(DE)            
                else:           
                    pass           
                if "NL" in updated_language_dict.keys():           
                    NL = """{% when "nl-NL","nl","NL" %}<br>""" + updated_language_dict["NL"][c][i] + '\n'
                    message_fragments.append(NL)            
                else:           
                    pass           
                if "BR" in updated_language_dict.keys():           
                    BR = """{% when "pt-BR","br","BR" %}<br>""" + updated_language_dict["BR"][c][i] + '\n'
                    message_fragments.append(BR)           
                else:
                    pass 
                if "EN" in updated_language_dict.keys():
                    EN = """{% else %}<br>""" + updated_language_dict["EN"][c][i]
                    message_fragments.append(EN) 
                else:
                    pass

                message = '<br>'.join(message_fragments)

                message_list.append(message)
    except:
        print("me no work")

    return message_list

