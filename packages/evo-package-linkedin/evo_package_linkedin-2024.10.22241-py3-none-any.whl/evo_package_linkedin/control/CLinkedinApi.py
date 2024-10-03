#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework import *
from evo_package_linkedin.entity import *
from evo_package_linkedin.utility import *

# ---------------------------------------------------------------------------------------------------------------------------------------
# CLinkedinApi
# ---------------------------------------------------------------------------------------------------------------------------------------
"""CLinkedinApi
"""
class CLinkedinApi(CApi):
	__instance = None
# ---------------------------------------------------------------------------------------------------------------------------------------
	def __init__(self):   
		if CLinkedinApi.__instance != None:
			raise Exception("ERROR:SINGLETON")
		else:
			super().__init__()
			CLinkedinApi.__instance = self
			self.currentPath = os.path.dirname(os.path.abspath(__file__))
			
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""getInstance Singleton

	Raises:
		Exception:  api exception

	Returns:
		_type_: CLinkedinApi instance
	"""
	@staticmethod
	def getInstance():
		if CLinkedinApi.__instance is None:
			cObject = CLinkedinApi()  
			cObject.doInit()  
		return CLinkedinApi.__instance
# ---------------------------------------------------------------------------------------------------------------------------------------
	"""doInit

	Raises:
		Exception: api exception

	Returns:

	"""   
	def doInit(self):   
		try:			
			ULinkedinApi.getInstance().doInit()
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
			
			api0 = self.newApi("linkedin-post", callback=self.doPost, input=ELinkedinPost, output=ELinkedinOutput )
			api0.description=""
			api0.required="*"

			api1 = self.newApi("linkedin-get_me", callback=self.doGetMe, input=ELinkedinInput, output=ELinkedinOutput )
			api1.description=""
			api1.required="*"
  
		except Exception as exception:
			IuLog.doException(__name__, exception)
			raise
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""doPost api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def doPost(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"doPost: {eAction} ")

					
			async for eActionOutput in ULinkedinApi.getInstance().doDoPost(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------

	"""doGetMe api callback

	Raises:
		Exception: api exception

	Returns:
		EAction:  EObject 
	"""   
	async def doGetMe(self,  eAction: EAction) -> EAction:
		try:
			IuLog.doDebug(__name__,f"doGetMe: {eAction} ")

					
			async for eActionOutput in ULinkedinApi.getInstance().doDoGetMe(eAction):
				IuLog.doVerbose(__name__, f"{eActionOutput}")
				yield eActionOutput	


		except Exception as exception:
			IuLog.doException(__name__, exception)
			eAction.doSetError(f"{exception}")
			yield eAction
# ---------------------------------------------------------------------------------------------------------------------------------------
