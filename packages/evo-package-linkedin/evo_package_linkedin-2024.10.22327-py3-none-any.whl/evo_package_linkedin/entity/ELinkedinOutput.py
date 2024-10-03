#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""ELinkedinOutput

	ELinkedinOutput DESCRIPTION
	
"""
class ELinkedinOutput(EObject):

	VERSION:int = 2393539669185471327

	def __init__(self):
		super().__init__()
		self.Version:int = self.VERSION
		
		self.urnID:str = None
		self.isError:bool = None
		self.error:str = None
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteStr(self.urnID, stream)
		self._doWriteBool(self.isError, stream)
		self._doWriteStr(self.error, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.urnID = self._doReadStr(stream)
		self.isError = self._doReadBool(stream)
		self.error = self._doReadStr(stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\turnID:{self.urnID}",
				f"\tisError:{self.isError}",
				f"\terror:{self.error}",
							]) 
		return strReturn
	