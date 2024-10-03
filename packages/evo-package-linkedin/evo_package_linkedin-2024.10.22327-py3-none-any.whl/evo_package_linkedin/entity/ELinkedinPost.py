#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_framework.core.evo_core_api.entity.EApiFile import EApiFile
#========================================================================================================================================
"""ELinkedinPost

	
	
"""
class ELinkedinPost(EObject):

	VERSION:int = 5130445934194925531

	def __init__(self):
		super().__init__()
		self.Version:int = self.VERSION
		
		self.urnId:str = None
		self.token:str = None
		self.isCompany:bool = None
		self.visibility:str = "PUBLIC"
		self.language:str = "en_US"
		self.text:str = None
		self.eApiFile:EApiFile = None
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteStr(self.urnId, stream)
		self._doWriteStr(self.token, stream)
		self._doWriteBool(self.isCompany, stream)
		self._doWriteStr(self.visibility, stream)
		self._doWriteStr(self.language, stream)
		self._doWriteStr(self.text, stream)
		self._doWriteEObject(self.eApiFile, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.urnId = self._doReadStr(stream)
		self.token = self._doReadStr(stream)
		self.isCompany = self._doReadBool(stream)
		self.visibility = self._doReadStr(stream)
		self.language = self._doReadStr(stream)
		self.text = self._doReadStr(stream)
		self.eApiFile = self._doReadEObject(EApiFile, stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\turnId:{self.urnId}",
				f"\ttoken:{self.token}",
				f"\tisCompany:{self.isCompany}",
				f"\tvisibility:{self.visibility}",
				f"\tlanguage:{self.language}",
				f"\ttext:{self.text}",
				f"\teApiFile:{self.eApiFile}",
							]) 
		return strReturn
	