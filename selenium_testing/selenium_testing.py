import sys
import subprocess
try:
    from selenium import webdriver
    import selenium
    from selenium.webdriver.firefox.options import Options
except ModuleNotFoundError:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "selenium"])
        from selenium import webdriver
        import selenium
    except:
        print("Unable to import dependencies. Run program as admin or install selenium for python to resolve.")
        raise SystemExit
import random
import time
import string
import re
import os
alphabet = string.ascii_lowercase
def main():
    first_run = False
    #Look for config:
    try:
        tmpx = open("config.uwu", "r")
        tmpx.close()
    except:
        first_run = True
        with open("config.uwu", "w+") as config_defaults:
            config_defaults.writelines("This is your config! UwU\n[\nfirst_run : True\nchrome : \"\"\nfirefox : \"\"\ntimer : 2\n]\n")
    
    #Initial setup values:
    chrome_opt = webdriver.ChromeOptions()
    chrome_opt.add_experimental_option("excludeSwitches", ['enable-logging'])
    first_time_run = ""
    driver_paths = config_setread()
    visited_urls = {}
    output_visited_urls = ""
    run_count = 0
    if first_run:
        settings_menu()
    uin = str(input("Main menu: \n\t1: Launch Firefox\n\t2: Launch Chrome\n\t3: Enter settings\n:")).lower()
    
    #Handle menu choice and setup:
    if uin == "settings" or uin == "3":
        settings_menu()
        uin = str(input("Main menu: \n\t1: Launch Firefox\n\t2: Launch Chrome\n:")).lower()
    if uin == "firefox" or uin == "1":
        try:
            br = webdriver.Firefox(executable_path=driver_paths[0], service_log_path="nul")
        except:
            try:
                default_path = "../seleniumdrivers/geckodriver.exe"
                br = webdriver.Firefox(executable_path=default_path, service_log_path="nul")
                write_to_config(default_path, "firefox")
            except:
                print("Cannot find driver path, please add the path to config file")
                raise SystemExit
    elif uin == "chrome" or uin == "2":
        try:
            br = webdriver.Chrome(executable_path=driver_paths[1], options=chrome_opt)
        except:
            try:
                default_path = "../seleniumdrivers/chromedriver.exe"
                br = webdriver.Chrome(executable_path=default_path, options=chrome_opt)
                write_to_config(default_path, "chrome")
            except:
                print("Cannot find driver path, please add the path to config file")
                raise SystemExit
    else:
        print("Invalid input")
        raise SystemExit
    
    #Main program loop
    go_back = False
    internal_timer = cfg_get_line(5)
    while run_count != -1:
        print("CTRL + C to stop program")
        try:
            if go_back == False:
                url = generate_url()
                br.get(str(url))
                visited_urls[run_count] = [url]
            print("URL:", url)
            br.execute_script("window.stop()")
            if internal_timer == "timer : m\n" or internal_timer == "timer : manual\n":
                uin3 = str(input("Press enter for next image, type \"quit\" (or q) to stop\nType \"back\" (or b) to visit last URL\n")).lower()
                go_back = False
                if uin3 == "":
                    pass
                elif uin3 == "back" or uin3 == "b":
                    try:
                        br.get(str(visited_urls[run_count-1])[2:len(visited_urls[run_count-1])-3])
                        run_count -= 1
                        go_back = True
                    except KeyError:
                        print("No previous URL to visit")
                        pass
                elif uin3 == "quit" or uin3 == "q":
                    raise KeyboardInterrupt
                run_count += 1
            else:
                time.sleep(int(internal_timer[8:len(internal_timer)-1]))
                run_count += 1
        except KeyboardInterrupt:
            run_count = -1
    print("\nURLs visited this session:\n")
    #Format visited urls
    for key in range(len(visited_urls)):
        output_visited_urls += str(key+1) + " : " + str(visited_urls[key]) + "\n"
    print(output_visited_urls)
    uin2 = str(input("\nWrite urls to a text file? (Y/N)\n: ")).lower()
    #Filesaving section
    if uin2 == "y" or uin2 == "yes":
        try:
            filename = save_file(output_visited_urls)
        except Exception as ex:
            print(ex)
            print("Something went wrong attempting to save file")
            raise SystemExit
        print("Saving file with name ", filename, ".txt", sep="")
    else:
        print("Program completed, goodbye!")
        raise SystemExit

def config_setread():
    with open("config.uwu", "r") as rconfig:
        rconfig = rconfig.read()
        dpaths = parse_config(rconfig)
        if dpaths is None:
            print("Config file doesn't have driver paths correctly set")
        return dpaths
        try:
            print("hi")
        except:
            print("Error attempting to read and write to local folder. Ensure python has permissions and try again")

def write_to_config(path, browser):
    with open("config.uwu", "r") as read_cfg:
        cfg_data = read_cfg.readlines()
        if browser == "chrome":
            cfg_data[3] = "chrome : \""+os.path.abspath(path)+"\"\n"
        elif browser == "firefox":
            cfg_data[4] =  "firefox : \""+os.path.abspath(path)+"\"\n"
        elif browser == "timer":
            cfg_data[5] = "timer : "+path+"\n"
    with open("config.uwu", "w") as write_cfg:
        write_cfg.writelines(cfg_data)

def parse_config(cfg):
    start_point = cfg.find("[")
    end_point = cfg.find("]")
    chrome_path_find = re.search("chrome : \"(.+?)\"\\n", cfg)
    if chrome_path_find:
        chrome_path = chrome_path_find.group(1)
    else:
        print("No chrome path specified in config")
        chrome_path = "empty"
    firefox_path_find = re.search("firefox : \"(.+?)\"\\n", cfg)
    if firefox_path_find:
        firefox_path = firefox_path_find.group(1)
    else:
        print("No firefox path specified in config")
        firefox_path = "empty"
    dpaths = [str(firefox_path), str(chrome_path)]
    return dpaths

def cfg_get_line(line_number):
    with open("config.uwu", "r") as read_cfg:
        cfg_data = read_cfg.readlines()
    return cfg_data[line_number]

def save_file(output_visited_urls):
    filename = generate_filename()
    file_create = open(filename+".txt", "w")
    file_create.write(str(output_visited_urls))
    file_create.close()
    return filename

def generate_url():
    letter1 = random.randrange(0,16)
    letter2 = random.randrange(0,len(alphabet))
    base_url = ("https://prnt.sc/" 
    + str(alphabet[letter1:letter1+1])
    + str(alphabet[letter2:letter2+1])
    + str(random.randrange(0,10)) 
    + str(random.randrange(0,10)) 
    + str(random.randrange(0,10)) 
    + str(random.randrange(0,10)))
    return base_url

def generate_filename():
    user_filename = str(input("Enter filename (or leave blank for random)\n: "))
    if user_filename != "":
        return user_filename
    fname = []
    alphabet_with_nums = alphabet + "0123456789"
    for i in range(10):
        random_var = random.randrange(len(alphabet_with_nums))
        tmp_var = str(alphabet_with_nums[random_var:random_var+1])
        fname.append(tmp_var)
    return ''.join(fname)

def settings_menu():
    loop_this = 1
    while loop_this == 1:
        uin4 = str(input("\nSettings menu: \n\t1: Modify default chrome driver path\n\t2: Modify default firefox path\n\t3: Change timer mode or duration\n\t4: Reset config to defaults\n:")).lower()
        if uin4 == "1":
            nchrome_path = str(input("\nEnter new chrome driver path, format C:/user/desktop/driver.exe or ../mydrivers/driver.exe or \"q\" to cancel\n:")).lower()
            if nchrome_path != "q":
                write_to_config(nchrome_path, "chrome")
            rmenu = str(input("\nReturn to settings menu? (Y/N)\n:")).lower()
            if rmenu == "n":
                loop_this = -1
        elif uin4 == "2":
            nfirefox_path = str(input("\nEnter new chrome driver path, format C:/user/desktop/driver.exe or ../mydrivers/driver.exe or \"q\" to cancel\n:")).lower()
            if nchrome_path != "q":
                write_to_config(nfirefox_path, "firefox")
            rmenu = str(input("\nReturn to settings menu? (Y/N)\n:")).lower()
            if rmenu == "n":
                loop_this = -1
        elif uin4 == "3":
            ntimer = str(input("Enter a number for duration between url changes, or \"m\" for manual switching\n:")).lower()
            if ntimer:
                write_to_config(ntimer, "timer")
            else:
                print("Invalid input")
            rmenu = str(input("\nReturn to settings menu? (Y/N)\n:")).lower()
            if rmenu == "n":
                loop_this = -1
        elif uin4 == "4":
            with open("config.uwu", "w+") as config_defaults:
                config_defaults.writelines("This is your config! UwU\n[\nfirst_run : True\nchrome : \"\"\nfirefox : \"\"\ntimer : 2\n]\n")
            rmenu = str(input("\nReturn to settings menu? (Y/N)\n:")).lower()
            if rmenu == "n":
                loop_this = -1
if __name__ == "__main__":
    main()