#           _____ ____     _____                 _
#     /\   / ____|___ \   |  __ \               | |
#    /  \ | |  __  __) |  | |__) |_____   _____ | | _____ _ __
#   / /\ \| | |_ ||__ <   |  _  // _ \ \ / / _ \| |/ / _ \ '__|
#  / ____ \ |__| |___) |  | | \ \  __/\ V / (_) |   <  __/ |
# /_/    \_\_____|____/   |_|  \_\___| \_/ \___/|_|\_\___|_|
#                Made by illuminator3
import os
import os.path as path
import platform
import re
import shutil
import subprocess
import sys
from typing import AnyStr


def installPackage(package: AnyStr) -> None:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '--quiet'])


def boolInput(question: AnyStr) -> bool:
    done = False
    output = False
    valRE = re.compile('^([yY]|[yY][eE][sS])|([nN]|[nN][oO])$')
    yesRE = re.compile('^([yY]|[yY][eE][sS])$')

    while not done:
        inp = input(question)

        if valRE.match(inp):
            done = True

            output = yesRE.match(inp.lower())

    return output


def start() -> None:
    version = '1.4-SNAPSHOT'
    versionRegex = re.compile('\\d.\\d.\\d{2}(\\d|$)')
    defaultPackageJson = '{"name":"discord_desktop_core","version":"0.0.0","private":"true","main":"index.js"}'
    defaultIndexJS = 'module.exports = require(\'./core.asar\');'

    print('----------------------------------------------------------------')
    print('AG3 Revoker [v' + version + ']')
    print('Made by illuminator3')
    print('Contact me on discord for more information: illuminator3#0001')
    print('----------------------------------------------------------------')
    print('Disclaimer: I\'m not responsible for any harm or damage that is being caused by this software. Use at your own risk!')

    if not boolInput('Do you want to proceed (y/n)? '):
        return

    verbose = boolInput('Verbose (y/n)? ')

    print('Installing required packages...')

    installPackage('psutil')

    import psutil

    print('Detecting os...')

    system = platform.system()

    print('OS: ' + system)

    if system != 'Windows':
        print('Cannot run on anything other than Windows!')

        return

    appdata = os.getenv('APPDATA').replace('\\', '/')

    if verbose:
        print('AppData: ' + appdata)

    for file1 in os.listdir(appdata):
        basename1 = path.basename(file1)

        if verbose:
            print('Discovered file: ' + basename1)

        bnsm = basename1.lower()

        if bnsm == 'discord' or bnsm == 'discordptb' or bnsm == 'discordcanary':
            print('Found discord build: ' + basename1)

            for file2 in os.listdir(appdata + '/' + file1):
                basename2 = path.basename(file2)

                if verbose:
                    print('Discovered file: ' + basename2)

                if versionRegex.match(basename2) and path.isdir(appdata + '/' + file1 + '/' + file2):
                    print('Found discord version: ' + basename2)

                    for file3 in os.listdir(appdata + '/' + file1 + '/' + file2):
                        basename3 = path.basename(file3)

                        if verbose:
                            print('Discovered file: ' + basename3)

                        if basename3 == 'modules':
                            print('Found module folder: ' + basename3)

                            for file4 in os.listdir(appdata + '/' + file1 + '/' + file2 + '/' + file3):
                                basename4 = path.basename(file4)

                                if verbose:
                                    print('Found module: ' + basename4)

                                if basename4 == 'discord_desktop_core':
                                    print('Found desktop core: ' + basename4)

                                    files = []

                                    for file5 in os.listdir(appdata + '/' + file1 + '/' + file2 + '/' + file3 + '/' + file4):
                                        basename5 = path.basename(file5)

                                        if verbose:
                                            print('Discovered file: ' + basename5)

                                        files.append(appdata + '/' + file1 + '/' + file2 + '/' + file3 + '/' + file4 + '/' + file5)

                                    detectedFiles = [path.basename(f) for f in files]

                                    print('Found files: ' + str(detectedFiles))

                                    normalFiles = ['core.asar', 'index.js', 'package.json']

                                    print('Checking for unexpected files...')

                                    foundUnexpected = False
                                    removedUnexpected = 0
                                    foundFiles = 0

                                    for file in files:
                                        basename = path.basename(file)

                                        if basename not in normalFiles:
                                            foundFiles += 1

                                            if not foundUnexpected:
                                                foundUnexpected = True

                                            print('Found unexpected file: ' + basename)

                                            if boolInput('Delete this file (y/n)? '):
                                                if path.isdir(file):
                                                    shutil.rmtree(file)
                                                else:
                                                    os.remove(file)

                                                removedUnexpected += 1

                                    if foundUnexpected:
                                        print('Found ' + str(foundFiles) + ' unexpected file(s)')
                                        print('Removed ' + str(removedUnexpected) + ' of them')
                                    else:
                                        print('Found no unexpected files')

                                    print('Checking for missing files...')

                                    rFiles = []

                                    for file in files:
                                        rFiles.append(path.basename(file))

                                    base = appdata + '/' + file1 + '/' + file2 + '/' + file3 + '/' + file4

                                    foundMissing = False
                                    foundMissingCount = 0
                                    createdMissing = 0

                                    for file in normalFiles:
                                        if file not in rFiles:
                                            foundMissingCount += 1

                                            if not foundMissing:
                                                foundMissing = True

                                            print('Found missing file: ' + file)

                                            # worst case scenario
                                            if file == 'core.asar':
                                                print('Couldn\'t find \'core.asar\' which is the core of discord. You\'ll need to reinstall discord :(')

                                                return

                                            if boolInput('Create this file (y/n)? '):
                                                createdMissing += 1

                                                fo = open(base + '/' + file, 'w+')

                                                if file == 'package.json':
                                                    fo.write(defaultPackageJson)
                                                elif file == 'index.js':
                                                    fo.write(defaultIndexJS)

                                                fo.close()

                                    if foundMissing:
                                        print('Found ' + str(foundMissingCount) + ' missing file(s)')
                                        print('Created ' + str(removedUnexpected) + ' of them')
                                    else:
                                        print('Found no missing files')

                                    print('Checking for edited files...')

                                    index = base + '/' + 'index.js'

                                    edited = False

                                    if path.exists(index):
                                        fr = open(index, 'r')

                                        lines = fr.readlines()

                                        fr.close()

                                        if len(lines) != 1:
                                            edited = True
                                        else:
                                            for line in lines:
                                                if line != defaultIndexJS:
                                                    edited = True

                                    if edited:
                                        print('Found edited file: index.js')

                                        print('Found 1 edited file(s)')

                                        if boolInput('Repair them (y/n)? '):
                                            os.remove(index)

                                            fo = open(index, 'w+')

                                            fo.write(defaultIndexJS)

                                            fo.close()

                                            print('Successfully repaired them!')
                                    else:
                                        print('Found no edited files')

    print('Checking if discord is running...')

    found = False

    for proc in psutil.process_iter():
        try:
            name = proc.name()

            if name.lower() == 'discord.exe':
                found = True

                print('Found discord process: ' + str(proc.pid))

                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if found:
        print('Starting discord...')

        discordFile = appdata + '/Microsoft/Windows/Start Menu/Programs/Discord Inc/Discord.lnk'

        os.startfile(discordFile)
    else:
        print('No discord process is running!')

    print('Have a nice day and goodbye!')
    print('(╯°□°）╯︵ ┻━┻')


if __name__ == '__main__':
    start()
