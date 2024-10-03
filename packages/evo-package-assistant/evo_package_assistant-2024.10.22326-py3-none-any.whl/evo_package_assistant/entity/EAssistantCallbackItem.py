#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git # 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EAssistantCallbackItem

	EAssistantTool DESCRIPTION
	
"""
class EAssistantCallbackItem(EObject):

	VERSION:int = 4231467523048814406

	def __init__(self):
		super().__init__()
		self.Version:int = self.VERSION
		
		self.name:str = None
		self.type:str = None
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteStr(self.name, stream)
		self._doWriteStr(self.type, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.name = self._doReadStr(stream)
		self.type = self._doReadStr(stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\tname:{self.name}",
				f"\ttype:{self.type}",
							]) 
		return strReturn
	