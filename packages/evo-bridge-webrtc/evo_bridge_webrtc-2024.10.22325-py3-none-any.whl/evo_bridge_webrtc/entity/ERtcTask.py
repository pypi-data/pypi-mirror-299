#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git | 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_bridge_webrtc.entity.ERtc import ERtc
#<
from aiortc import RTCDataChannel
#>
#========================================================================================================================================
"""ERtcTask

	ERtcTask _DOC_
	
"""
class ERtcTask(EObject):

	VERSION:int = 5886902736120184298

	def __init__(self):
		super().__init__()
		self.Version:int = self.VERSION
		
		self.eRtc:ERtc = None
		
#<
		self.channel: RTCDataChannel = None
		self.data:bytes = None
		self.task = None
		self.evoCallBack = None
#>
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteEObject(self.eRtc, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.eRtc = self._doReadEObject(ERtc, stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\teRtc:{self.eRtc}",
							]) 
		return strReturn
	