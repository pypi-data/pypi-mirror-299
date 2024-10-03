#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_framework.core.evo_core_api.entity.EApiText import EApiText
#========================================================================================================================================
"""ESpeakInput

	ESpeakInput _DOC_
	
"""
class ESpeakInput(EObject):

	VERSION:int = 3493840629674045204

	def __init__(self):
		super().__init__()
		self.Version:int = self.VERSION
		
		self.eSpeakModelID:str = None
		self.eApiText:EApiText = None
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteStr(self.eSpeakModelID, stream)
		self._doWriteEObject(self.eApiText, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.eSpeakModelID = self._doReadStr(stream)
		self.eApiText = self._doReadEObject(EApiText, stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\teSpeakModelID:{self.eSpeakModelID}",
				f"\teApiText:{self.eApiText}",
							]) 
		return strReturn
	