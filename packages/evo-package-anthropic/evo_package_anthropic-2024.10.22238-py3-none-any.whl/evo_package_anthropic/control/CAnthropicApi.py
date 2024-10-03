#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git | 
#========================================================================================================================================

from evo_framework import *
from evo_package_anthropic.entity import *
from evo_package_anthropic.utility import *
from EChatInput import EChatInput
from EChatMessage import EChatMessage
from EChatModelMap import EChatModelMap
from EChatMapMessage import EChatMapMessage
from EChatMapSession import EChatMapSession

# ---------------------------------------------------------------------------------------------------------------------------------------
# CAnthropicApi
# ---------------------------------------------------------------------------------------------------------------------------------------
"""CAnthropicApi
"""
class CAnthropicApi(CApi):
	__instance = None
# ---------------------------------------------------------------------------------------------------------------------------------------
	def __init__(self):   
		if CAnthropicApi.__instance != None:
			raise Exception("ERROR:SINGLETON")
		else:
			super().__init__()
			CAnthropicApi.__instance = self
			self.currentPath = os.path.dirname(os.path.abspath(__file__))
			
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""getInstance Singleton

	Raises:
		Exception:  api exception

	Returns:
		_type_: CAnthropicApi instance
	"""
	@staticmethod
	def getInstance():
		if CAnthropicApi.__instance is None:
			cObject = CAnthropicApi()  
			cObject.doInit()  
		return CAnthropicApi.__instance
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""doInit

	Raises:
		Exception: api exception

	Returns:

	"""   
	def doInit(self):   
		try:			
			UAnthropicApi.getInstance()
		except Exception as exception:
			IuLog.doException(__name__, exception)
			raise	  
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""doAddApi

	Raises:
		Exception: api exception

	Returns:

	"""
	@override   
	def doAddApi(self):
		try:			
			
			api0 = self.newApi("anthropic-chatstream", callback=self.onChatStream, input=EChatInput, output=EChatMessage )
			api0.description="anthropic-chatstream _DESCRIPTION_ [USE evo.package.chat API]"
			api0.required="*"

			api1 = self.newApi("anthropic-get_mapmodel", callback=self.onGetMapModel, input=EChatInput, output=EChatModelMap )
			api1.description="anthropic-get_mapmodel _DESCRIPTION_ [USE evo.package.chat API]"
			api1.required="eChatInput.token"

			api2 = self.newApi("anthropic-get_mapmessage", callback=self.onGetMapMessage, input=EChatInput, output=EChatMapMessage )
			api2.description="anthropic-get_mapmessage _DESCRIPTION_ [USE evo.package.chat API]"
			api2.required="eChatInput.token|eChatInput.sessionID"

			api3 = self.newApi("anthropic-get_mapsession", callback=self.onGetMapSession, input=EChatInput, output=EChatMapSession )
			api3.description="anthropic-get_mapsession _DESCRIPTION_ [USE evo.package.chat API]"
			api3.required="eChatInput.token"
  
		except Exception as exception:
			IuLog.doException(__name__, exception)
			raise
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onChatStream api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onChatStream(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onChatStream: {eAction} ")
				
			eChatInputInput:EChatInput = eAction.doGetInput(EChatInput)
			
			#Remove eAction input for free memory
			eAction.input = None
					
			async for eChatMessageOutput in UAnthropicApi.getInstance().doOnChatStream(eChatInputInput):
				eAction.doSetOutput(eChatMessageOutput)
				yield eAction	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onGetMapModel api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onGetMapModel(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onGetMapModel: {eAction} ")
				
			eChatInputInput:EChatInput = eAction.doGetInput(EChatInput)
			
			#Remove eAction input for free memory
			eAction.input = None
					
			async for eChatModelMapOutput in UAnthropicApi.getInstance().doOnGetMapModel(eChatInputInput):
				eAction.doSetOutput(eChatModelMapOutput)
				yield eAction	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onGetMapMessage api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onGetMapMessage(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onGetMapMessage: {eAction} ")
				
			eChatInputInput:EChatInput = eAction.doGetInput(EChatInput)
			
			#Remove eAction input for free memory
			eAction.input = None
					
			async for eChatMapMessageOutput in UAnthropicApi.getInstance().doOnGetMapMessage(eChatInputInput):
				eAction.doSetOutput(eChatMapMessageOutput)
				yield eAction	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onGetMapSession api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onGetMapSession(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onGetMapSession: {eAction} ")
				
			eChatInputInput:EChatInput = eAction.doGetInput(EChatInput)
			
			#Remove eAction input for free memory
			eAction.input = None
					
			async for eChatMapSessionOutput in UAnthropicApi.getInstance().doOnGetMapSession(eChatInputInput):
				eAction.doSetOutput(eChatMapSessionOutput)
				yield eAction	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------
