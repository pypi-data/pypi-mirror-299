#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git | 
#========================================================================================================================================

from evo_framework import *
from evo_package_anthropic.entity import *
from EChatInput import EChatInput
from EChatMessage import EChatMessage
from EChatModelMap import EChatModelMap
from EChatMapMessage import EChatMapMessage
from EChatMapSession import EChatMapSession

#<
from anthropic import 
#>
# ---------------------------------------------------------------------------------------------------------------------------------------
# UAnthropicApi
# ---------------------------------------------------------------------------------------------------------------------------------------
"""UAnthropicApi
"""
class UAnthropicApi():
    __instance = None
# ---------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self):   
        if UAnthropicApi.__instance != None:
            raise Exception("ERROR:SINGLETON")
        else:
            super().__init__()
            UAnthropicApi.__instance = self
            self.currentPath = os.path.dirname(os.path.abspath(__file__))
            
# ---------------------------------------------------------------------------------------------------------------------------------------
    """getInstance Singleton

    Raises:
        Exception:  api exception

    Returns:
        _type_: UAnthropicApi instance
    """
    @staticmethod
    def getInstance():
        if UAnthropicApi.__instance is None:
            uObject = UAnthropicApi()  
            uObject.doInit()  
        return UAnthropicApi.__instance
# ---------------------------------------------------------------------------------------------------------------------------------------
    """doInit

    Raises:
        Exception: api exception

    Returns:

    """   
    def doInit(self):   
        try:
#<
            #INIT ...
            pass
#>   
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnChatStream(self, eChatInput:EChatInput) -> EChatMessage :
        try:
            if eChatInput is None:
                raise Exception("ERROR_REQUIRED|eChatInput|")

#<        
            #Add other check
            '''
            if eChatInput. is None:
                raise Exception("ERROR_REQUIRED|eChatInput.|")
            '''
   
            eChatMessage = EChatMessage()
            eChatMessage.doGenerateID()
            
            
            yield eChatMessage
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnGetMapModel(self, eChatInput:EChatInput) -> EChatModelMap :
        try:
            if eChatInput is None:
                raise Exception("ERROR_REQUIRED|eChatInput|")

#<        
            #Add other check
            '''
            if eChatInput. is None:
                raise Exception("ERROR_REQUIRED|eChatInput.|")
            '''
   
            eChatModelMap = EChatModelMap()
            eChatModelMap.doGenerateID()
            
            
            yield eChatModelMap
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnGetMapMessage(self, eChatInput:EChatInput) -> EChatMapMessage :
        try:
            if eChatInput is None:
                raise Exception("ERROR_REQUIRED|eChatInput|")

#<        
            #Add other check
            '''
            if eChatInput. is None:
                raise Exception("ERROR_REQUIRED|eChatInput.|")
            '''
   
            eChatMapMessage = EChatMapMessage()
            eChatMapMessage.doGenerateID()
            
            
            yield eChatMapMessage
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnGetMapSession(self, eChatInput:EChatInput) -> EChatMapSession :
        try:
            if eChatInput is None:
                raise Exception("ERROR_REQUIRED|eChatInput|")

#<        
            #Add other check
            '''
            if eChatInput. is None:
                raise Exception("ERROR_REQUIRED|eChatInput.|")
            '''
   
            eChatMapSession = EChatMapSession()
            eChatMapSession.doGenerateID()
            
            
            yield eChatMapSession
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------

#<
#OTHER METHODS ...
#>
# ---------------------------------------------------------------------------------------------------------------------------------------
