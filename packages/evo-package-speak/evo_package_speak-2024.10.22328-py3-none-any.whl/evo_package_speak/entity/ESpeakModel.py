#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_package_speak.entity.EnumSpeakGender import EnumSpeakGender
#========================================================================================================================================
"""ESpeakModel

	ESpeakModel _DOC_
	
"""
class ESpeakModel(EObject):

	VERSION:int = 2064565816451797525

	def __init__(self):
		super().__init__()
		self.Version:int = self.VERSION
		
		self.enumSpeakGender:EnumSpeakGender = EnumSpeakGender.FEMALE
		self.name:str = None
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteInt(self.enumSpeakGender.value, stream)
		self._doWriteStr(self.name, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.enumSpeakGender = EnumSpeakGender(self._doReadInt(stream))
		self.name = self._doReadStr(stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\tenumSpeakGender:{self.enumSpeakGender}",
				f"\tname:{self.name}",
							]) 
		return strReturn
	