from glob import glob


if __name__ == '__main__':

    json_files_list = glob('Bioengineering/*.json')
    print (json_files_list[1])
    for json_file in json_files_list:
        with open(json_file, 'r') as file:
            raw_json = file.readlines()

        with open(json_file, 'w', encoding='utf-8') as file:
            for line in raw_json:
                line.replace(']}\n', ']},\n')
                line.replace('l}\n', 'l},\n')
                if line.find(']}\n') != -1 or line.find('l}\n') != -1:
                    line = line[:-1] + ',\n'
                
                right_ap = 0
                left_ap = 0
                index = 0
                if line.find('abstract') != -1 and line.find('"None"') == -1:
                    while index < (len(line) - index-1):
                        rindex = len(line)-1-index
                        
                        if line[index] == '"':
                            if left_ap == 3:
                                

                                line = line[:index] + "'" + line[index+1:]
                                print(line)
                            else:
                                left_ap += 1
                        if line[rindex] == '"':    
                            if right_ap == 1:
                                line = line[:rindex] + "'" + line[rindex+1:]
                                print(line)
                            else:
                                right_ap += 1

                        index += 1
                    # print(line)
                file.write(line)



