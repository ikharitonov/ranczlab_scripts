import json
import numpy as np
import xml.etree.ElementTree as ET

def load_config_json(path):
    with open(path, 'r') as f:
        file = json.load(f)

    APGain_values = []
    LFPGain_values = []
    APFilter_values = []
    Reference_values = []

    for i in range(len(file['Channels'])):
        APGain_values.append(file['Channels'][i]["APGain"])
        LFPGain_values.append(file['Channels'][i]["LFPGain"])
        APFilter_values.append(file['Channels'][i]["APFilter"])
        Reference_values.append(file['Channels'][i]["Reference"])
        

    print("Loaded file summary:")

    for APGain_unique_val in np.unique(APGain_values):
        channels_selected = np.where(APGain_values==APGain_unique_val)
        print(f"APGain value of {APGain_unique_val} is set for {channels_selected[0].shape[0]} channels from {channels_selected[0][0]} to {channels_selected[0][-1]}.")
    
    for LFPGain_unique_val in np.unique(LFPGain_values):
        channels_selected = np.where(LFPGain_values==LFPGain_unique_val)
        print(f"LFPGain value of {LFPGain_unique_val} is set for {channels_selected[0].shape[0]} channels from {channels_selected[0][0]} to {channels_selected[0][-1]}.")
    
    for APFilter_unique_val in np.unique(APFilter_values):
        channels_selected = np.where(APFilter_values==APFilter_unique_val)
        print(f"APFilter value of {APFilter_unique_val} is set for {channels_selected[0].shape[0]} channels from {channels_selected[0][0]} to {channels_selected[0][-1]}.")
    
    for Reference_unique_val in np.unique(Reference_values):
        channels_selected = np.where(Reference_values==Reference_unique_val)
        print(f"Reference value of {Reference_unique_val} is set for {channels_selected[0].shape[0]} channels from {channels_selected[0][0]} to {channels_selected[0][-1]}.")
    
    return file

def load_config_xml(path):
    tree = ET.parse(path)
    file = tree.getroot()
    
    APGain_values = []
    LFPGain_values = []
    APFilter_values = []
    Reference_values = []

    for i in range(len(file[-2])):
        APGain_values.append(file[-2][i][2].text) # APGain
        LFPGain_values.append(file[-2][i][3].text) # LFPGain
        APFilter_values.append(file[-2][i][5].text) # APFilter
        Reference_values.append(file[-2][i][6].text) # Reference

    APGain_values = np.array(APGain_values)
    LFPGain_values = np.array(LFPGain_values)
    APFilter_values = np.array(APFilter_values)
    Reference_values = np.array(Reference_values)
    
    print("Loaded file summary:")

    for APGain_unique_val in np.unique(APGain_values):
        channels_selected = np.where(APGain_values==APGain_unique_val)
        print(f"APGain value of {APGain_unique_val} is set for {channels_selected[0].shape[0]} channels from {channels_selected[0][0]} to {channels_selected[0][-1]}.")
    
    for LFPGain_unique_val in np.unique(LFPGain_values):
        channels_selected = np.where(LFPGain_values==LFPGain_unique_val)
        print(f"LFPGain value of {LFPGain_unique_val} is set for {channels_selected[0].shape[0]} channels from {channels_selected[0][0]} to {channels_selected[0][-1]}.")
    
    for APFilter_unique_val in np.unique(APFilter_values):
        channels_selected = np.where(APFilter_values==APFilter_unique_val)
        print(f"APFilter value of {APFilter_unique_val} is set for {channels_selected[0].shape[0]} channels from {channels_selected[0][0]} to {channels_selected[0][-1]}.")
    
    for Reference_unique_val in np.unique(Reference_values):
        channels_selected = np.where(Reference_values==Reference_unique_val)
        print(f"Reference value of {Reference_unique_val} is set for {channels_selected[0].shape[0]} channels from {channels_selected[0][0]} to {channels_selected[0][-1]}.")
    
    return file

def modify_config_json(json_file, modify_channel_groups):
    for channel_group in modify_channel_groups:
        channel_id_list_to_modify = [x for x in range(channel_group["start_channel_id"], channel_group["end_channel_id"]+1)]

        for channel_id in channel_id_list_to_modify:
            json_file['Channels'][channel_id]["APGain"] = channel_group["APGain"]
            json_file['Channels'][channel_id]["LFPGain"] = channel_group["LFPGain"]
            json_file['Channels'][channel_id]["APFilter"] = channel_group["APFilter"]
            json_file['Channels'][channel_id]["Reference"] = channel_group["Reference"]

            # # Modifying the gain correction value based on gain value
            # try:
            #     file['Channels'][channel_id]["APGainCorrection"] = file['Channels'][channel_id]["GainCorrectrions"]
            # except:
            #     print("Selected gain value is not allowed. Please choose a different value and run the script again.")
        
        print(f"New values set for {len(channel_id_list_to_modify)} channel group:")
        print(channel_group)

    return json_file

def modify_config_xml(xml_file, modify_channel_groups):
    for channel_group in modify_channel_groups:
        channel_id_list_to_modify = [x for x in range(channel_group["start_channel_id"], channel_group["end_channel_id"]+1)]

        for channel_id in channel_id_list_to_modify:
            xml_file[-2][channel_id][2].text = channel_group["APGain"]
            xml_file[-2][channel_id][3].text = channel_group["LFPGain"]
            xml_file[-2][channel_id][5].text = channel_group["APFilter"]
            xml_file[-2][channel_id][6].text = channel_group["Reference"]
        
        print(f"New values set for {len(channel_id_list_to_modify)} channel group:")
        print(channel_group)

    return xml_file

def save_config_json(path, json_file):
    with open(path, 'w') as f:
        json.dump(json_file, f, indent=4)
    print("File saved.")

def save_config_xml(path, xml_file):
    new_tree = ET.ElementTree(xml_file)
    new_tree.write(path)
    print("File saved.")