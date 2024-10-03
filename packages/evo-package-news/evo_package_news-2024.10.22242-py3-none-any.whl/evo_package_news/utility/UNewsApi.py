#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework import *
from evo_package_news.entity import *

#<
#OTHER IMPORTS ...
#>
# ---------------------------------------------------------------------------------------------------------------------------------------
# UNewsApi
# ---------------------------------------------------------------------------------------------------------------------------------------
"""UNewsApi
"""
class UNewsApi():
    __instance = None
# ---------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self):   
        if UNewsApi.__instance != None:
            raise Exception("ERROR:SINGLETON")
        else:
            super().__init__()
            UNewsApi.__instance = self
            self.currentPath = os.path.dirname(os.path.abspath(__file__))
            
# ---------------------------------------------------------------------------------------------------------------------------------------
    """getInstance Singleton

    Raises:
        Exception:  api exception

    Returns:
        _type_: UNewsApi instance
    """
    @staticmethod
    def getInstance():
        if UNewsApi.__instance is None:
            uObject = UNewsApi()  
            uObject.doInit()  
        return UNewsApi.__instance
# ---------------------------------------------------------------------------------------------------------------------------------------
    """doInit

    Raises:
        Exception: api exception

    Returns:

    """   
    def doInit(self):   
        try:
#<
            #INIT ...
            pass
#>   
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnApi0(self, eAction:EAction) -> EAction:
        """doOnApi0 utility callback
            input: ENewsInput
            output: ENewsOutput

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

            eNewsInput:ENewsInput = eAction.doGetInput(ENewsInput)
           
            #Dispose eAction.input for free memory
            eAction.input = b''

            if eNewsInput is None:
                raise Exception("ERROR_REQUIRED|eNewsInput|")

#<        
            #Add other check
            '''
            if eNewsInput. is None:
                raise Exception("ERROR_REQUIRED|eNewsInput.|")
            '''
   
            eNewsOutput = ENewsOutput()
            eNewsOutput.doGenerateID()
            eNewsOutput.doGenerateTime()

            eAction.enumApiAction = EnumApiAction.COMPLETE
            eAction.doSetOutput(eNewsOutput)        
            yield eAction
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------

#<
#OTHER METHODS ...
#>
# ---------------------------------------------------------------------------------------------------------------------------------------
