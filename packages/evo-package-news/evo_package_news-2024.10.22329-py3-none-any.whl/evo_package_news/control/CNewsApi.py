#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework import *
from evo_package_news.entity import *
from evo_package_news.utility import *

# ---------------------------------------------------------------------------------------------------------------------------------------
# CNewsApi
# ---------------------------------------------------------------------------------------------------------------------------------------
"""CNewsApi
"""
class CNewsApi(CApi):
	__instance = None
# ---------------------------------------------------------------------------------------------------------------------------------------
	def __init__(self):   
		if CNewsApi.__instance != None:
			raise Exception("ERROR:SINGLETON")
		else:
			super().__init__()
			CNewsApi.__instance = self
			self.currentPath = os.path.dirname(os.path.abspath(__file__))
			
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""getInstance Singleton

	Raises:
		Exception:  api exception

	Returns:
		_type_: CNewsApi instance
	"""
	@staticmethod
	def getInstance():
		if CNewsApi.__instance is None:
			cObject = CNewsApi()  
			cObject.doInit()  
		return CNewsApi.__instance
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""doInit

	Raises:
		Exception: api exception

	Returns:

	"""   
	def doInit(self):   
		try:			
			UNewsApi.getInstance()
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
			
			api0 = self.newApi("news-api0", callback=self.onApi0, input=ENewsInput, output=ENewsOutput )
			api0.description="news-api0 _DESCRIPTION_"
			api0.required="*"
  
		except Exception as exception:
			IuLog.doException(__name__, exception)
			raise
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""onApi0 api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def onApi0(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"onApi0: {eAction} ")

					
			async for eActionOutput in UNewsApi.getInstance().doOnApi0(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------
