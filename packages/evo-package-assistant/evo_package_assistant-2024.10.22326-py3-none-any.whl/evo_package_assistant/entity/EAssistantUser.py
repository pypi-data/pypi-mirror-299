#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_package_assistant.entity.EAssistantMessage import EAssistantMessage
#========================================================================================================================================
"""EAssistantUser

	EAssistant _DOC_
	
"""
class EAssistantUser(EObject):

	VERSION:int = 3774955153310886413

	def __init__(self):
		super().__init__()
		self.Version:int = self.VERSION
		
		self.eAssistanID:str = None
		self.mapEAssistantMessage:EvoMap = EvoMap()
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteStr(self.eAssistanID, stream)
		self._doWriteMap(self.mapEAssistantMessage, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.eAssistanID = self._doReadStr(stream)
		self.mapEAssistantMessage = self._doReadMap(EAssistantMessage, stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\teAssistanID:{self.eAssistanID}",
				f"\tmapEAssistantMessage:{self.mapEAssistantMessage}",
							]) 
		return strReturn
	