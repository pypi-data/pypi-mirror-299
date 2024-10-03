#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""ENewsInput

	ENewsInput _DOC_
	
"""
class ENewsInput(EObject):

	VERSION:str="e79eb037f8e727c1e6c90c134b04fec0dd96c623fb1f14cad580066cc30c0e15"

	def __init__(self):
		super().__init__()
		
		self.attribute0:str = None
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteStr(self.attribute0, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.attribute0 = self._doReadStr(stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\tattribute0:{self.attribute0}",
							]) 
		return strReturn
	