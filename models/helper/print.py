DICT_ENCODINGS = ["Dictionary", "Unencoded", "LZ4", "RunLength", "FoR-SIMD"]
DICT_COLUMNS = ["driver_id", "latitude", "longitude", "timestamp", "status"]

def to_MegaByte(value):
    return value/1_000_000

def print_header(longest_str, column_dict, storage):
    print('Storage:', storage)
    for column_name in ['CHUNK'] + column_dict:
        print(column_name.ljust(longest_str), end='')
    print('') 

def print_conf(model, sort_bool, column_dict, encoding_dict):
    longest_str = max([len(encoding) for encoding in encoding_dict]) + 10
    line_break_count = 0
    config = []
     
    for item in model.X:
        if round(model.X[item].value) == 1.0:
            config += [item]
            
    for b in model.B:
        print_header(longest_str, column_dict, b)
        for item in config:
            if line_break_count == 0:
                print(str(item[0]).ljust(longest_str), end='')
            if line_break_count <= len(column_dict):
                if item[5] == b: 
                    if sort_bool:
                        print(display_conf_values_bool(item, encoding_dict).ljust(longest_str), end='')
                    else:
                        print(display_conf_values(item, encoding_dict, line_break_count).ljust(longest_str), end='')
                else:
                    print(' '.ljust(longest_str), end='')
                line_break_count += 1
            if line_break_count == len(column_dict):
                print('')
                line_break_count = 0
        print('')

def display_conf_values_bool(item, encoding_dict):
    s  = '- ' if item[3] == 0 else 'S '
    s += '- ' if item[4] == 0 else 'I '
    s += encoding_dict[item[2]]
    return s

def display_conf_values(item, encoding_dict, line_break_count):
    s  = '- ' if item[3] != line_break_count else 'S '
    s += '- ' if item[4] == 0 else 'I '
    s += encoding_dict[item[2]]
    return s

def print_result(result, model, sort_bool, column_dict=DICT_COLUMNS, encoding_dict=DICT_ENCODINGS):
    print(f'Solving for budget;')
    for i in range(len(model.B)):
        print(f'  Storage: {i}     Storage Size: {model.SB[i].value} ') 
    print('')
    condition = result.json_repn()['Solver'][0]['Termination condition']
    print(f'Result: {condition}', end='')
    if condition == 'optimal':
        print(f" (walltime: {float(result.json_repn()['Solver'][0]['Wall time']):.4f}s)")
        print(f'Objective: {model.Obj.expr()}')
        print('Memory consumption:')
        for b in model.B:
            print(f'  {b}: {to_MegaByte(model.MemoryBudgetConstraint[b].body())} MB')
        print('')
        print_conf(model, sort_bool, DICT_COLUMNS, DICT_ENCODINGS)
    print('')