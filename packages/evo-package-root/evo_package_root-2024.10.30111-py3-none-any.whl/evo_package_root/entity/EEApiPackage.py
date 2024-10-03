#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git | 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_framework.core.evo_core_api.entity.EApi import EApi
#========================================================================================================================================
"""EEApiPackage

	EEApiPackage _DOC_
	
"""
class EEApiPackage(EObject):

	VERSION:int = 4176741325721557773

	def __init__(self):
		super().__init__()
		self.Version:int = self.VERSION
		
		self.name:str = None
		self.language:str = None
		self.mapEApi:EvoMap = EvoMap()
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteStr(self.name, stream)
		self._doWriteStr(self.language, stream)
		self._doWriteMap(self.mapEApi, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.name = self._doReadStr(stream)
		self.language = self._doReadStr(stream)
		self.mapEApi = self._doReadMap(EApi, stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\tname:{self.name}",
				f"\tlanguage:{self.language}",
				f"\tmapEApi:{self.mapEApi}",
							]) 
		return strReturn
	