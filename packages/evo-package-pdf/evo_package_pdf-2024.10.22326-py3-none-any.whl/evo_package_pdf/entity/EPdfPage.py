#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_framework.core.evo_core_api.entity.EApiFile import EApiFile
from evo_framework.core.evo_core_api.entity.EApiText import EApiText
#========================================================================================================================================
"""EPdfPage

	
	
"""
class EPdfPage(EObject):

	VERSION:int = 4061980154747297981

	def __init__(self):
		super().__init__()
		self.Version:int = self.VERSION
		
		self.number:int = None
		self.title:str = None
		self.text:str = None
		self.mapEApiImage:EvoMap = EvoMap()
		self.mapEApiTextUri:EvoMap = EvoMap()
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteInt(self.number, stream)
		self._doWriteStr(self.title, stream)
		self._doWriteStr(self.text, stream)
		self._doWriteMap(self.mapEApiImage, stream)
		self._doWriteMap(self.mapEApiTextUri, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.number = self._doReadInt(stream)
		self.title = self._doReadStr(stream)
		self.text = self._doReadStr(stream)
		self.mapEApiImage = self._doReadMap(EApiFile, stream)
		self.mapEApiTextUri = self._doReadMap(EApiText, stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\tnumber:{self.number}",
				f"\ttitle:{self.title}",
				f"\ttext:{self.text}",
				f"\tmapEApiImage:{self.mapEApiImage}",
				f"\tmapEApiTextUri:{self.mapEApiTextUri}",
							]) 
		return strReturn
	