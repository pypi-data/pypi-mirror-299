import os
import platform
import subprocess
from time import sleep
import click
from utp.checkport import isPortUsed
from utp.utils import OS, readCommand

def checkAppium():
    """check appium installed and is running"""
    
    if isPortUsed(4723): 
        click.secho("appium have running before", bg='black', fg='yellow')
        return None
    
    #check appium is installed
    if platform.system() == OS.WINDOWS.value:
        appiumStatus, appiumError = readCommand("where.exe appium")
    elif platform.system() == OS.LINUX.value:
        appiumStatus, appiumError = readCommand("which appium")
    else:
        appiumStatus, appiumError = readCommand("which appium | grep $(npm config get prefix)")
        
    click.secho("Check appium", bg='black', fg='white')
       
    if appiumError:
        if appiumError.count("Could not find") > 0:
            click.secho("Prepare facilitator", bg='black', fg='yellow')
            os.popen("npm install -g appium").read()
        else:
            click.secho(appiumError, bg='black', fg='yellow')
            exit(1)            
    elif not (appiumStatus and appiumStatus.strip()):
        click.secho("Prepare facilitator", bg='black', fg='yellow')
        os.popen("npm install -g appium").read()
    
    driverInstalled, driverInstalledError = readCommand("appium driver list --installed")
    click.secho("Check Driver", bg='black', fg='white')
    
    if platform.system() == OS.LINUX.value:
       driverInstalled= driverInstalled or driverInstalledError
    
    if driverInstalled.count("uiautomator2") <= 0:
        click.secho("installing uiautomator2", bg='black', fg='green')
        os.popen("appium driver install uiautomator2").read()
        
    click.secho("Check Device farm", bg='black', fg='white')
    
    appiumStatus, appiumStatusError = readCommand("appium plugin list --installed")
    #check device farm is installed
    if platform.system() == OS.LINUX.value:
       appiumStatus= appiumStatus or appiumStatusError
       
    if appiumStatus.count("device-farm") <= 0:
        click.secho("Prepare local device-farm", bg='black', fg='yellow')
        subprocess.Popen(["appium", "plugin", "install", "--source", "npm", "appium-device-farm"], shell= platform.system() == OS.WINDOWS.value).wait()
        # subprocess.Popen(["appium", "plugin", "install", "--source", "npm", "appium-dashboard"]).wait()
        # os.popen("appium plugin install --source=npm appium-dashboard").read()
        click.secho("Prepared", bg='black', fg='yellow')
    
    click.secho("Run Appium", bg='black', fg='white')

    handler= subprocess.Popen(["appium", "server", "-ka", "800",  "--use-plugins", "device-farm", "-pa", "/wd/hub", "--plugin-device-farm-platform","android"], shell= platform.system() == OS.WINDOWS.value, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                            
    
    sleep(5)
    click.secho("http://127.0.0.1:4723/device-farm", bg='black', fg='green')
    
    return handler