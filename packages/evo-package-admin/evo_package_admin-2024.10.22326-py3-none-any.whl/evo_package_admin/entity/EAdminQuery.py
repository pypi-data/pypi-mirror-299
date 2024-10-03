#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EAdminQuery

	EAdminInput _DOC_
	
"""
class EAdminQuery(EObject):

	VERSION:int = 5476703423514004390

	def __init__(self):
		super().__init__()
		self.Version:int = self.VERSION
		
		self.queryID:str = None
		self.queryCollection:str = None
		self.query:str = None
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteStr(self.queryID, stream)
		self._doWriteStr(self.queryCollection, stream)
		self._doWriteStr(self.query, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.queryID = self._doReadStr(stream)
		self.queryCollection = self._doReadStr(stream)
		self.query = self._doReadStr(stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\tqueryID:{self.queryID}",
				f"\tqueryCollection:{self.queryCollection}",
				f"\tquery:{self.query}",
							]) 
		return strReturn
	