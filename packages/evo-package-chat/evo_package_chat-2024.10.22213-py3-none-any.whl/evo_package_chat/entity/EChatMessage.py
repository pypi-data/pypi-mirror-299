#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_package_chat.entity.EnumChatRole import EnumChatRole
from evo_framework.core.evo_core_api.entity.EApiText import EApiText
from evo_framework.core.evo_core_api.entity.EApiText import EApiText
from evo_framework.core.evo_core_api.entity.EApiFile import EApiFile
#========================================================================================================================================
"""EChatMessage

    EChatMessage _DOC_
    
"""
class EChatMessage(EObject):

    VERSION:str="73468a97f539f80746b2b14e20ae9e32d11f556ecefcb2e329d6aa6e8aeb04a6"

    def __init__(self):
        super().__init__()
        
        self.enumChatRole:EnumChatRole = EnumChatRole.USER
        self.model:str = None
        self.eAssistantID:bytes = None
        self.sessionID:bytes = None
        self.eApiText:EApiText = None
        self.isError:bool = None
        self.error:str = None
        self.mapEApiText:EvoMap = EvoMap()
        self.mapEApiFile:EvoMap = EvoMap()
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteInt(self.enumChatRole.value, stream)
        self._doWriteStr(self.model, stream)
        self._doWriteBytes(self.eAssistantID, stream)
        self._doWriteBytes(self.sessionID, stream)
        self._doWriteEObject(self.eApiText, stream)
        self._doWriteBool(self.isError, stream)
        self._doWriteStr(self.error, stream)
        self._doWriteMap(self.mapEApiText, stream)
        self._doWriteMap(self.mapEApiFile, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.enumChatRole = EnumChatRole(self._doReadInt(stream))
        self.model = self._doReadStr(stream)
        self.eAssistantID = self._doReadBytes(stream)
        self.sessionID = self._doReadBytes(stream)
        self.eApiText = self._doReadEObject(EApiText, stream)
        self.isError = self._doReadBool(stream)
        self.error = self._doReadStr(stream)
        self.mapEApiText = self._doReadMap(EApiText, stream)
        self.mapEApiFile = self._doReadMap(EApiFile, stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tenumChatRole:{self.enumChatRole}",
                f"\tmodel:{self.model}",
                f"\teAssistantID length:{len(self.eAssistantID) if self.eAssistantID else 'None'}",
                f"\tsessionID length:{len(self.sessionID) if self.sessionID else 'None'}",
                f"\teApiText:{self.eApiText}",
                f"\tisError:{self.isError}",
                f"\terror:{self.error}",
                f"\tmapEApiText:{self.mapEApiText}",
                f"\tmapEApiFile:{self.mapEApiFile}",
                            ]) 
        return strReturn
    