#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EApiOutput

	EApi output
	
"""
class EApiOutput(EObject):

	VERSION:int = 4579839825006626100

	def __init__(self):
		super().__init__()
		self.Version:int = self.VERSION
		
		self.eObjectClass:str = None
		self.version:bytes = None
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteStr(self.eObjectClass, stream)
		self._doWriteBytes(self.version, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.eObjectClass = self._doReadStr(stream)
		self.version = self._doReadBytes(stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\teObjectClass:{self.eObjectClass}",
				f"\tversion length:{len(self.version) if self.version else 'None'}",
							]) 
		return strReturn
	