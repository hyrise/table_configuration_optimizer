import csv
import os

# settings for csv export of configurations
FOLDER = '../data/config/' 
MODEL_NAME = 'ISE'
SEPARATOR = '|' 
CONVERSION_FACTOR = 1_000_000 # Bytes to Megabytes 

UNSORTED_ID = 5

def serialize(val, seperator):
    config_str = ''
    for key in val:
        config_str += str(val[key].value//CONVERSION_FACTOR) + seperator
    return config_str[:-1]

def serialize_constraint(constraint, storage):
    config_str = ''
    for key in range(len(storage)):
        config_str += str(value(model.MemoryBudgetConstraint[key].body)/CONVERSION_FACTOR) + SEPARATOR
    return config_str[:-1]

def set_sorted_column_for_segment(lines, sort_columns):
    new_lines = []
    for l in lines:
        line = list(l)
        if line[0] in sort_columns:
            line[3] = sort_columns[line[0]]
        else:
            line[3] = UNSORTED_ID
        new_lines += [line]
    return new_lines

def get_file_name(model, folder):
    return folder + MODEL_NAME + '_' + serialize(model.SB, '-') + '.csv'

def write_file(file_path, header, lines, d = ','):          
    with open(file_path, mode='w') as out_file:
        csv_writer = csv.writer(out_file, delimiter=d)
        if header:
            csv_writer.writerow(header)
           
        for line in lines:
            csv_writer.writerow(line)
                
    out_file.close()
    
def export_config(model):
    lines = []
    sort_columns = {} 
    
    config = model.X
    for item in config:
        if round(config[item].value) == 1.0:
            lines += [item]
            if item[3] == 1:
                sort_columns[item[0]] = item[1]
    
    lines = set_sorted_column_for_segment(lines, sort_columns)        
    write_file(get_file_name(model, FOLDER), ['CHUNK', 'COLUMN', 'ENCODING', 'SORT', 'INDEX', 'STORAGE'], lines)