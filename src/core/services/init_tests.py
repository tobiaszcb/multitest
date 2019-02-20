import os, sys
from platform import system
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TestServiceHelper:
    """Lists tests, creates commands to run using Popen, generates ID"""

    def __init__(self):
        sys.path.append(self.getMainDirPath())

    def getScripts(self):
        declTypes = ['SUIT1', 'SUIT2']
        scripts = []
        for file in os.listdir(self.getMainDirPath()):
            if not '.py' in file:
                continue
            for decl in declTypes:
                if file.find(decl) == -1:
                    continue
                else:
                    scripts.append(file)
        return scripts

    def getMainDirPath(self):
        core = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))
        test_scripts_path = os.path.join(core, 'test_scripts')
        return test_scripts_path

    def getMsgFilesFolder(self):
        return "{}{}additional".format(self.getMainDirPath(),
                                       self.whichSlash())

    def whichSlash(self):
        return "\\" if system() == 'Windows' else '/'

    def whichPython(self):
        return 'py' if system() == 'Windows' else 'python3'

    def getCommand(self, script):
        """
        Creates a command, which will be passed to subprocess.Popen() in order to
        launch a test.
        """
        logger.info("Creating command in TestServiceHelper: {}".format(script))
        instance = self.importClass(script)
        logger.info("Instance in getCommand: {}".format(instance))
        return self.createCommand(numOfXmlsFiles=instance.num_of_xmls, script=script)

    def createCommand(self, numOfXmlsFiles, script):
        changeDir = "cd {} {} ".format(self.getMainDirPath().replace(" ", "\ "),
                                       "&" if system() == "Windows" else ";")
        if numOfXmlsFiles == 0:
            cmd = "{} {} cfgqa1.ini".format(self.whichPython(), script)
        elif numOfXmlsFiles == 1:
            cmd = "{} {} cfgqa1.ini \"{}\"".format(self.whichPython(),
                                                   script,
                                                   self.getXmlFilePath(script, 0))
        else:
            cmd = "{} {} cfgqa1.ini \"{}\" \"{}\"".format(self.whichPython(),
                                                          script, self.getXmlFilePath(script, 1),
                                                          self.getXmlFilePath(script, 2))
        return changeDir + cmd

    def importClass(self, script: str):
        try:
            module = __import__(script.split('.')[0], fromlist=list(self.getMainDirPath()))
            return module.Test
        except Exception as e:
            logger.error("Exception occured: {}".format(e))

    def getXmlFilePath(self, script, option):
        endings = {0: '.xml',
                   1: '-1.xml',
                   2: '-2.xml'}
        return self.getMsgFilesFolder() + self.whichSlash() + script.replace(".py", endings[option])

    def generateId(self):
        return "{}".format(datetime.now().strftime('%y%m%d%H%M'))