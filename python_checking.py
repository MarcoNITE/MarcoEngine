import platform
import sys
from colorama import init, Fore

init(autoreset=True)

def linux_distribution():
  try:
    return platform.linux_distribution()
  except:
    return "N/A"

def check():
    print(Fore.BLUE + """Python version: {}
    linux_distribution: {}
    system: {}
    machine: {}
    platform: {}
    uname: {}
    version: {}
    mac_ver: {}
    """.format(
    sys.version.split('\n'),
    linux_distribution(),
    platform.system(),
    platform.machine(),
    platform.platform(),
    platform.uname(),
    platform.version(),
    platform.mac_ver(),
    ))

    if platform.system() == "Windows":
        print(Fore.RED + 'Sorry, only Linux supported.')

    else:
        print(Fore.GREEN + 'Check done!')

if __name__ == "__main__":
    check()
