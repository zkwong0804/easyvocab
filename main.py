import requests
import datetime
import os
import json
import xlwt
from bs4 import BeautifulSoup
PREFIX = "https://dictionary.cambridge.org/dictionary/english"
TARGET_CLASS = "def ddef_d db"


def print_menu():
    title = "Welcome to easy vocab program"
    star = ""
    for e in title:
        star += "*"
    print("{}\n{}\n{}".format(star, title, star))
    print("1. Create vocab list")
    print("2. Add vocab to list")
    print("3. Export vocab list")
    print("4. Exit")

    return input("\n\nYour action: ")

def clear():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")

def get_files_name():
    name_list = []
    for name in os.listdir("./list"):
        name_list.append(name)
    return name_list;

def get_full_dir(filename):
    return "./list/{}".format(filename)

def get_meaning(word):
    meanings = []
    r = requests.get("{}/{}".format(PREFIX, word))
    soup = BeautifulSoup(r.text, "html.parser")
    for e in soup.find_all("div", class_=TARGET_CLASS):
        meanings.append(e.text)
    
    return meanings

def chose_file():
    is_file_chosen = False
    chosen_file = ""
    name_list = get_files_name()
    while not is_file_chosen:
        for i in range(len(name_list)):
            print("{}. {}".format(i, name_list[i]))
        
        opt = 0
        raw_opt = "";
        try:
            raw_opt = input("Select vocab list: ")
            opt = int(raw_opt)
            chosen_file = name_list[opt]
            is_file_chosen = True
        except ValueError:
            print("Invalid opt! {}".format(raw_opt))
        except IndexError:
            print("Invalid opt! {}".format(raw_opt))
    
    return chosen_file

def create_list():
    list_name = input("List name(Press enter to use default): ")
    if not list_name:
        list_name = datetime.datetime.now().strftime("%d%m%y");
    list_name = "{}.json".format(list_name)
    clear()
    if list_name in get_files_name():
        print("Duplicated name found!\n")
    else:
        print("File name is good to go!\n")
        f = open(get_full_dir(list_name), "w");
        f.write("{\"list\":[]}")
        f.close()

def add_vocab():
    chosen_file = chose_file()

    print("You have chosen: {}".format(chosen_file))
    print("Insert process start! (type \"exit!\" to stop the process!)")
    next_word = ""
    word_list = []
    searched_before = []
    counter = 1
    while next_word != "exit!":
        next_word = input("{}.\t".format(counter))
        counter+=1
        if next_word != "exit!":
            word_list.append(next_word)

    local_dict_json = open("local_dict.json", "r")
    vocab_list_json = open(get_full_dir(chosen_file), "r")

    local_dict = json.loads(local_dict_json.read())
    local_dict_json.close()
    vocab_list = json.loads(vocab_list_json.read())
    vocab_list_json.close()

    for e in word_list:
        if e in local_dict:
            searched_before.append(e)
        else:
            meaning = get_meaning(e)
            local_dict[e] = meaning
        
        if e not in vocab_list["list"]:
            vocab_list["list"].append(e)
    
    clear()
    if len(searched_before) != 0:
        print("You have searched these word before! These word will be saved into focus.xls file!")
        for e in searched_before:
            print("\t* {}".format(e))

    local_dict_json = open("local_dict.json", "w")
    vocab_list_json = open(get_full_dir(chosen_file), "w")
    local_dict_json.write(json.dumps(local_dict))
    vocab_list_json.write(json.dumps(vocab_list))
    local_dict_json.close()
    vocab_list_json.close()
    print("\nlocal dictionary updated!")
    print("{} updated!\n".format(chosen_file))

def export_list():
    chosen_file = chose_file()
    wb = xlwt.Workbook(encoding="UTF-8")
    ws = wb.add_sheet("Sheet 1")

    local_dict_json = open("local_dict.json", "r")
    vocab_list_json = open(get_full_dir(chosen_file), "r")
    local_dict = json.loads(local_dict_json.read())
    vocab_list = json.loads(vocab_list_json.read())
    local_dict_json.close()
    vocab_list_json.close()

    for i in range(len(vocab_list["list"])):
        word = vocab_list["list"][i]
        meaning = ""
        for e in local_dict[word]:
            meaning += "{}\n".format(e)
        ws.write(i, 0, word)
        ws.write(i, 1, meaning)

    wb.save("{}.xls".format(chosen_file))
    clear()
    print("{}.xls has been exported to the program root directory!\n".format(chosen_file))

def main():
    leave_program = False
    
    if "local_dict.json" not in os.listdir("./"):
        f = open("local_dict.json", "w")
        f.write("{}")
        f.close()

    if not os.path.isdir("./list"):
        os.mkdir("./list")
        
    while not leave_program:
        opt = print_menu()
        if opt == "1":
            create_list()
        elif opt == "2":
            add_vocab();
        elif opt == "3":
            export_list()
        elif opt == "4":
            print("Bye bye")
            leave_program = True
        else:
            print("Opsie! Invalid option found!")
        

if __name__ == "__main__":
    main()
