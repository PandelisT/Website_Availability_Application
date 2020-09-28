import sys
import time
from colorama import Fore, init
import functions as f
from views import View
from views import ChooseOptions
init(autoreset=True)

if "--help" in sys.argv:
    f.instructions()
    time.sleep(10)
else:
    pass

print(40*"*")
print(Fore.GREEN + """
Welcome to the Website Availability
Python Terminal Application!
""")
print(40*"*")

while True:
    website_address = input("Which website would you like to check? \n")
    get_new_website = View(website_address)
    new_website = get_new_website.get_website()
    print("*"*40)
    print(new_website[1])
    print("*"*40)

    if new_website[0] is True:
        break
    elif new_website[0] is False:
        continue

while True:
    try:
        get_new_website = View(website_address)
        options = get_new_website.show_options()
        individual_website_response = input(options)
        option = ChooseOptions(website_address, individual_website_response)
        print(option.choose_options())
        time.sleep(2)
    except Exception:
        print("Error in the program")
