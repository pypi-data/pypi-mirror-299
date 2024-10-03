#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_framework.core.evo_core_api.entity.EApiConfig import EApiConfig
#========================================================================================================================================
"""EEApiConfigMap

	EEApiConfigMap _DOC_
	
"""
class EEApiConfigMap(EObject):

	VERSION:int = 6717356383822701842

	def __init__(self):
		super().__init__()
		self.Version:int = self.VERSION
		
		self.mapEApiConfig:EvoMap = EvoMap()
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteMap(self.mapEApiConfig, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.mapEApiConfig = self._doReadMap(EApiConfig, stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\tmapEApiConfig:{self.mapEApiConfig}",
							]) 
		return strReturn
	