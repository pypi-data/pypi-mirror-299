#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git | 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_package_chat.entity.EChatInput import EChatInput
from evo_package_assistant.entity.EAssistant import EAssistant
from evo_package_chat.entity.EChatMapSession import EChatMapSession
#========================================================================================================================================
"""EAnthropicInfo

	EAnthropicInfo _DOC_
	
"""
class EAnthropicInfo(EObject):

	VERSION:int = 4434488346578872929

	def __init__(self):
		super().__init__()
		self.Version:int = self.VERSION
		
		self.eChatInput:EChatInput = None
		self.eAssistantID:str = None
		self.eAssistantSessionID:str = None
		self.eAssistantRagID:str = None
		self.eAssistant:EAssistant = None
		self.eChatMapSession:EChatMapSession = None
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteEObject(self.eChatInput, stream)
		self._doWriteStr(self.eAssistantID, stream)
		self._doWriteStr(self.eAssistantSessionID, stream)
		self._doWriteStr(self.eAssistantRagID, stream)
		self._doWriteEObject(self.eAssistant, stream)
		self._doWriteEObject(self.eChatMapSession, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.eChatInput = self._doReadEObject(EChatInput, stream)
		self.eAssistantID = self._doReadStr(stream)
		self.eAssistantSessionID = self._doReadStr(stream)
		self.eAssistantRagID = self._doReadStr(stream)
		self.eAssistant = self._doReadEObject(EAssistant, stream)
		self.eChatMapSession = self._doReadEObject(EChatMapSession, stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\teChatInput:{self.eChatInput}",
				f"\teAssistantID:{self.eAssistantID}",
				f"\teAssistantSessionID:{self.eAssistantSessionID}",
				f"\teAssistantRagID:{self.eAssistantRagID}",
				f"\teAssistant:{self.eAssistant}",
				f"\teChatMapSession:{self.eChatMapSession}",
							]) 
		return strReturn
	