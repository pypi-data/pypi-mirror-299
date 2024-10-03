#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_package_speak.entity.ESpeakModel import ESpeakModel
#========================================================================================================================================
"""ESpeakMapModel

	ESpeakMapModel _DOC_
	
"""
class ESpeakMapModel(EObject):

	VERSION:int = 672667315554092558

	def __init__(self):
		super().__init__()
		self.Version:int = self.VERSION
		
		self.mapESpeakModel:EvoMap = EvoMap()
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteMap(self.mapESpeakModel, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.mapESpeakModel = self._doReadMap(ESpeakModel, stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\tmapESpeakModel:{self.mapESpeakModel}",
							]) 
		return strReturn
	