import argparse
import pytest

log_list = []
log_dict = {}
level_dict = {'HANDLER':''}
len_col = 25



# args = sys.argv[1:]
# print(args)
parser = argparse.ArgumentParser()
parser.add_argument('input',nargs="+", help="Выгрузка в файл")
parser.add_argument('--report', help="Выгрузка в файл")
args = parser.parse_args()


def open_file(args):
    for a in args.input:
        with open(a, 'r') as file:
                for line in file:
                    log_list.append(line)     
    return log_list
  
def create_dict(log_list = [],level_dict={}):
    for i in range(len(log_list)):
        log_list[i] = log_list[i].split(' ')
        if not log_list[i][2] in level_dict:
            level_dict[log_list[i][2]] = 0
        if log_list[i][3] == 'django.request:':
            if log_list[i][4] =='GET':
                log_dict[log_list[i][5]]= dict()
            else:
                log_dict[log_list[i][7]] = dict()
    return log_dict, level_dict, log_list

def count(s = '',l=[], k=''):
    c = 0
    for i in l:
        if i[3] == 'django.request:':
            if i[2] == s and i[5] == k :
                c += 1
            elif i[2] == s and i[7] == k:
                c += 1
    return c

def create_level_dict(log_list,level_dict):
    for key in log_dict:
        for l in log_list:
            log_dict[key][l[2]]=count(l[2], log_list, key)
        for c in level_dict:    
            if c == 'HANDLER':
                level_dict[c] = ''
            else:
                level_dict[c] += log_dict[key][c]
    return level_dict, log_dict

def log_print(log_dict,level_dict):
    dict_for_print = dict(sorted(log_dict.items()))
    for n in level_dict:  
        ln = len_col-len(n)
        print(f'{n}{ln* " "}', end= "")
    for l in dict_for_print:
        ln = len_col-len(l)
        for n in level_dict:                 
            if n == 'HANDLER':
                w = f'\n{l}'
            else:
                w = dict_for_print[l][n]
            ln = len_col-len(str(w))
            print(f'{w}{ln* ' '}',end= "")
    print()
    for n in level_dict:
        s = level_dict[n]
        ln = len_col-len(str(s))
        print(f'{s}{ln* ' '}',end= "")
    print()

def report_generation(level_dict,log_dict):
    dict_for_print = dict(sorted(log_dict.items()))
    if args.report:
        with open(f"{args.report}.txt", "w") as file:
            for n in level_dict:
                ln = len_col-len(n)
                file.writelines(f'{n}{ln* ' '}')
            for l in dict_for_print:
                ln = len_col-len(l)
                for n in level_dict:                 
                    if n == 'HANDLER':
                        w = f'\n{l}'
                    else:
                        w = dict_for_print[l][n]
                    ln = len_col-len(str(w))
                    file.write(f'{w}{ln* ' '}') 
            file.write( ' \n')
            for n in level_dict: 
                s = level_dict[n]
                ln = len_col-len(str(s))
                file.write(f'{s}{ln* ' '}')


def main():
    try:
        open_file(args)
        create_dict(log_list,level_dict)
        create_level_dict(log_list,level_dict)
        log_print(log_dict,level_dict)
        report_generation(level_dict,log_dict)
    except FileNotFoundError:
        print('Такого файла нет')
    
if __name__ == '__main__':
    main()
    
