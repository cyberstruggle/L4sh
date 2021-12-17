class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def print_red(text):
    print(bcolors.FAIL + str(text) + bcolors.ENDC)

def print_green(text):
    print(bcolors.OKGREEN + str(text) + bcolors.ENDC)

def print_blue(text):
    print(bcolors.OKBLUE + str(text) + bcolors.ENDC)
