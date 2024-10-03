#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git # 
#========================================================================================================================================

from evo_framework import *
from evo_package_linkedin.entity import *
from evo_package_linkedin.utility.ULinkedin import ULinkedin
# --------------------------------------------------------------------------------------------------------------------------------------     
class IuLinkedin:
# --------------------------------------------------------------------------------------------------------------------------------------     
    @staticmethod
    async def doGetUserID(token:str):
       return await ULinkedin.getInstance().doGetUserID(token)
   
   # --------------------------------------------------------------------------------------------------------------------------------------     
    @staticmethod
    async def doPost(eLinkedinPost:ELinkedinPost):
       return await ULinkedin.getInstance().doPost(eLinkedinPost)
   