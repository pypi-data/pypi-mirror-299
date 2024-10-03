#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework import *
from evo_package_openai.entity import *
from evo_package_openai.utility import *
from evo_package_chat.entity.EChatInput import EChatInput
from evo_package_chat.entity.EChatMessage import EChatMessage
from evo_package_chat.entity.EChatModelMapOld import EChatModelMap
from evo_package_chat.entity.EChatMapMessage import EChatMapMessage
from evo_package_chat.entity.EChatMapSession import EChatMapSession

# ---------------------------------------------------------------------------------------------------------------------------------------
# COpenaiApi
# ---------------------------------------------------------------------------------------------------------------------------------------
"""COpenaiApi
"""
class COpenaiApi(CApi):
	__instance = None
# ---------------------------------------------------------------------------------------------------------------------------------------
	def __init__(self):   
		if COpenaiApi.__instance != None:
			raise Exception("ERROR:SINGLETON")
		else:
			super().__init__()
			COpenaiApi.__instance = self
			self.currentPath = os.path.dirname(os.path.abspath(__file__))
			
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""getInstance Singleton

	Raises:
		Exception:  api exception

	Returns:
		_type_: COpenaiApi instance
	"""
	@staticmethod
	def getInstance():
		if COpenaiApi.__instance is None:
			cObject = COpenaiApi()  
			cObject.doInit()  
		return COpenaiApi.__instance
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""doInit

	Raises:
		Exception: api exception

	Returns:

	"""   
	def doInit(self):   
		try:			
			UOpenaiApi.getInstance()
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
			
			api0 = self.newApi("openai-chatstream", callback=self.onChatStream, input=EChatInput, output=EChatMessage )
			api0.description="openai-chatstream _DESCRIPTION_ [USE evo.package.chat API]"
			api0.required="*"

			api1 = self.newApi("openai-get_mapmodel", callback=self.onGetMapModel, input=EChatInput, output=EChatModelMap )
			api1.description="openai-get_mapmodel _DESCRIPTION_ [USE evo.package.chat API]"
			api1.required="eChatInput.token"

			api2 = self.newApi("openai-get_mapmessage", callback=self.onGetMapMessage, input=EChatInput, output=EChatMapMessage )
			api2.description="openai-get_mapmessage _DESCRIPTION_ [USE evo.package.chat API]"
			api2.required="eChatInput.token|eChatInput.sessionID"

			api3 = self.newApi("openai-get_mapsession", callback=self.onGetMapSession, input=EChatInput, output=EChatMapSession )
			api3.description="openai-get_mapsession _DESCRIPTION_ [USE evo.package.chat API]"
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

					
			async for eActionOutput in UOpenaiApi.getInstance().doOnChatStream(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


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

					
			async for eActionOutput in UOpenaiApi.getInstance().doOnGetMapModel(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


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

					
			async for eActionOutput in UOpenaiApi.getInstance().doOnGetMapMessage(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


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

					
			async for eActionOutput in UOpenaiApi.getInstance().doOnGetMapSession(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------
