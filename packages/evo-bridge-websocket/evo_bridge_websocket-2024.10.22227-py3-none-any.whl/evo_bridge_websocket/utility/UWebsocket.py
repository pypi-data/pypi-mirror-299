#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git | 
#========================================================================================================================================

from evo_framework import *
# ---------------------------------------------------------------------------------------------------------------------------------------
# UWebsocket
# ---------------------------------------------------------------------------------------------------------------------------------------
""" UWebsocket
"""
class UWebsocket:  
    __instance = None

    def __init__(self):
        if UWebsocket.__instance != None:
            raise Exception("ERROR_SINGLETON")
        else:
            UWebsocket.__instance = self       
# -----------------------------------------------------------------------------
    @staticmethod
    def getInstance():
        if UWebsocket.__instance == None:
            uObject = UWebsocket()
            uObject.doInit()
            
        return UWebsocket.__instance
# -----------------------------------------------------------------------------
    def doInit(self):
        try:
            pass
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# -----------------------------------------------------------------------------   
    async def doMethod0(self):
        try:
            return None
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
