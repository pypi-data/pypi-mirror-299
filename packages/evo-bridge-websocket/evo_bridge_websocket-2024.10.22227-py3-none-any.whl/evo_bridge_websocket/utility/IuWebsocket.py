#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git | 
#========================================================================================================================================

from evo_framework import *
from evo_bridge_websocket.utility.UWebsocket import UWebsocket
# ---------------------------------------------------------------------------------------------------------------------------------------
# IuWebsocket
# ---------------------------------------------------------------------------------------------------------------------------------------
""" IuWebsocket
"""
class IuWebsocket(object):
   
    @staticmethod
    async def doMethod0():
        return await UWebsocket.getInstance().doMethod0()