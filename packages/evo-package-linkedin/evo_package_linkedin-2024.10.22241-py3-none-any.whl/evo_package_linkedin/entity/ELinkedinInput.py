#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""ELinkedinInput

	ELinkedinOutput DESCRIPTION
	
"""
class ELinkedinInput(EObject):

	VERSION:str="3df04049ed0e4be67074a5310962c596d234888ae39822a2912cef1524389afe"

	def __init__(self):
		super().__init__()
		
		self.token:str = None
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteStr(self.token, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.token = self._doReadStr(stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\ttoken:{self.token}",
							]) 
		return strReturn
	