import os
from typing import Optional

from utp.getConfig import getConfig


def appVariables(androidApp: str, androidPlatformVersion: Optional[str], remote: Optional[bool]=False, path: Optional[str] = None, noReset: Optional[bool] = None):
    ip = getConfig().get("server","").strip()
    
    my_env = os.environ
    my_env["ANDROID_AUTOMATION_NAME"] = 'UIAutomator2'
    my_env["ANDROID_APP"] = androidApp or f'http://{ip}:4723/device-farm/apps/file-1717336325068.apk'
    my_env["ANDROID_PLATFORM_NAME"] = 'Android'
    my_env["ANDROID_PLATFORM_VERSION"] = androidPlatformVersion or ""
    my_env['REMOTE'] = str(remote) if remote else ""
    my_env['TEST_PATH'] = path if path else ""
    my_env['NO_RESET'] = str(noReset) if noReset else ""
    
    return my_env
    