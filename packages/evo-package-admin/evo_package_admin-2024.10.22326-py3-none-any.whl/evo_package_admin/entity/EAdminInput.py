#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_framework.core.evo_core_api.entity.EApiAdmin import EApiAdmin
#========================================================================================================================================
"""EAdminInput

	EAdminInput _DOC_
	
"""
class EAdminInput(EObject):

	VERSION:int = 4422381950373688605

	def __init__(self):
		super().__init__()
		self.Version:int = self.VERSION
		
		self.eApiAdmin:EApiAdmin = None
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteEObject(self.eApiAdmin, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.eApiAdmin = self._doReadEObject(EApiAdmin, stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\teApiAdmin:{self.eApiAdmin}",
							]) 
		return strReturn
	