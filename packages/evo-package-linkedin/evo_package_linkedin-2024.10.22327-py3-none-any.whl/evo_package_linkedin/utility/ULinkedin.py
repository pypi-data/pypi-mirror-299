#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git # 
#========================================================================================================================================
#https://www.linkedin.com/developers/tools/oauth/token-generator
from evo_framework import *
from evo_package_linkedin.entity import *
from linkedin_api.clients.restli.client import RestliClient
from linkedin_api.clients.auth.client import AuthClient
import urllib
# ---------------------------------------------------------------------------------------------------------------------------------------
class ULinkedin:
    __instance = None

    def __init__(self):
        if ULinkedin.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            # self.restli_client = Client(access_token=access_token)
            ULinkedin.__instance = self
            self.restli_client = RestliClient()
            self.LINKEDIN_VERSION = "202404.01"
            self.URL_USERID = "/me"
            self.URL_UGCPOST = "/ugcPosts"
            self.URL_POST = "/posts"
            self.URL_INITIALIZE_UPLOAD_IMAGE = "https://api.linkedin.com/rest/images?action=initializeUpload"
            self.URL_INITIALIZE_UPLOAD_VIDEO = "https://api.linkedin.com/rest/videos?action=initializeUpload"
            self.URL_INITIALIZE_UPLOAD_FILE = "https://api.linkedin.com/rest/documents?action=initializeUpload"
            #self.URL_REGISTER_UPLOAD = "https://api.linkedin.com/rest/assets?action=registerUpload"
            self.URL_GETIMAGE = "https://api.linkedin.com/rest/images/"
            
            self.URL_GETFILE = "https://api.linkedin.com/rest/documents/"
            self.URL_GETVIDEO = "https://api.linkedin.com/rest/videos/"
# ---------------------------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def getInstance():
        if ULinkedin.__instance == None:
            ULinkedin()
        return ULinkedin.__instance

# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doGetUserID(self, ACCESS_TOKEN):
        try:
            userID_response = self.restli_client.get(
                resource_path=self.URL_USERID, access_token=ACCESS_TOKEN)
            print(
                f"Successfully fetched profile: {json.dumps(userID_response.entity)}")
            return userID_response.entity['id']
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------      
    async def doPost(self,eLinkedinPost:ELinkedinPost) -> ELinkedinOutput:
        try:
            
            if eLinkedinPost is None:
                raise Exception("ERROR_ELinkedinPost_NONE")
            
            IuLog.doInfo(__name__,f"eLinkedinPost:\n{eLinkedinPost.isCompany}")
            
            if eLinkedinPost.isCompany:
                urn = f"urn:li:organization:{eLinkedinPost.urnId}"
            else:
                urn = f"urn:li:person:{eLinkedinPost.urnId}"
                
            eLinkedinOutput = ELinkedinOutput()
            eLinkedinOutput.doGenerateID()
            
            if eLinkedinPost.eApiFile is not None:
                
                if eLinkedinPost.eApiFile.ext == ".png" or eLinkedinPost.eApiFile.ext == ".jpg":
                    urnID = await self.doPostImage(eLinkedinPost.token,urn, eLinkedinPost.eApiFile.data, eLinkedinPost.text, eLinkedinPost.visibility)
                    eLinkedinOutput.urnID = urnID
                    return eLinkedinOutput
           
                elif eLinkedinPost.eApiFile.ext == ".pdf":
                    urnID = await self.doPostFile(eLinkedinPost.token, urn, eLinkedinPost.eApiFile.data, eLinkedinPost.text, eLinkedinPost.visibility)
                    eLinkedinOutput.urnID = urnID
                    return eLinkedinOutput
            else: 
                urnID = await self.doPostText(eLinkedinPost.token, urn, eLinkedinPost.text, eLinkedinPost.visibility)
                eLinkedinOutput.urnID = urnID
                return eLinkedinOutput
                    
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise
            
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doPostText(self, ACCESS_TOKEN,urn:str, comment, visibility='PUBLIC'):
        try:
            
            entity = {
                "author": f"{urn}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": f"{comment}",
                        },
                        "shareMediaCategory": "NONE",
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": f"{visibility}"},
            }
            
            IuLog.doVerbose(__name__,f"entity:\n{entity}")

            ugc_posts_create_response = self.restli_client.create(
                resource_path=self.URL_UGCPOST,
                entity=entity,
                access_token=ACCESS_TOKEN,
            )
            postId= ugc_posts_create_response.entity_id
            IuLog.doDebug(__name__,f"Successfully created post : {postId}")
           
            return postId
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise

# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doGetUrlUploadImage(self, ACCESS_TOKEN, urn):
        try:
            
            headers = {
                'X-Restli-Protocol-Version': '2.0.0',
                'LinkedIn-Version': self.LINKEDIN_VERSION,
                'Authorization': 'Bearer ' + ACCESS_TOKEN,
            }

            data = {
                "initializeUploadRequest": {
                    "owner": f"{urn}"
                }
            }
            IuLog.doVerbose(__name__,f"data:{data}")
            
            response = requests.post(
                self.URL_INITIALIZE_UPLOAD_IMAGE, data=json.dumps(data), headers=headers)
            IuLog.doVerbose(__name__,f"response.json():{response.json()}")

         
            responseJson = response.json()
            urlUpload = responseJson['value']['uploadUrl']
            imageID = responseJson['value']['image']

            return imageID, urlUpload
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise

# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doUploadImage(self, ACCESS_TOKEN, urlUpload, dataImage):# pathImage):
        try:

            headers = {
                'X-Restli-Protocol-Version': '2.0.0',
                'LinkedIn-Version': self.LINKEDIN_VERSION,
                'Authorization': 'Bearer ' + ACCESS_TOKEN,
                'media-type-family': 'STILLIMAGE',
            }

           # with open(pathImage, "rb") as image_file:
            #    dataImage = image_file.read()
            IuLog.doVerbose(__name__,f"len(dataImage):{len(dataImage)}")
         
            response = requests.put(urlUpload, data=dataImage, headers=headers)
            IuLog.doVerbose(__name__,f"response.status_code:{response.status_code}")
        
            return response.status_code, urlUpload
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise

# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doGetImage(self, ACCESS_TOKEN, imageID):
        try:
            
            headers = {
                'X-Restli-Protocol-Version': '2.0.0',
                'LinkedIn-Version': self.LINKEDIN_VERSION,
                'Authorization': 'Bearer ' + ACCESS_TOKEN,
                'Content-Type': 'application/json'
                # 'media-type-family': 'STILLIMAGE',
            }

            imageIDEncode = urllib.parse.quote(imageID)
            urlImage = self.URL_GETIMAGE + imageIDEncode
            IuLog.doVerbose(__name__,f"urlImage:{urlImage}")

            response = requests.get(urlImage, headers=headers)
            
            downloadUrl = response.json()["downloadUrl"]
            return downloadUrl
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise

# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doPostImage(self, ACCESS_TOKEN, urn,  dataImage, comment, visibility='PUBLIC'):
        try:
            
            imageID, urlUpload = await self.doGetUrlUploadImage(ACCESS_TOKEN, urn)
            IuLog.doVerbose(__name__,f"urlUpload: {urlUpload}")
            

            await self.doUploadImage(ACCESS_TOKEN, urlUpload, dataImage)

           # downloadUrl = await self.doGetImage(ACCESS_TOKEN, imageID)
          
           # IuLog.doVerbose(__name__,f"downloadUrl: {downloadUrl}")
            entity = {
                "author": f"{urn}",
                "commentary": f"{comment}",
                "visibility": visibility,
                "distribution": {
                    "feedDistribution": "MAIN_FEED",
                    "targetEntities": [],
                    "thirdPartyDistributionChannels": []
                },
                "content": {
                    "media": {
                        "title": "image",
                        "id": f"{imageID}",
                    }
                },
                "lifecycleState": "PUBLISHED",
            #"isReshareDisabledByAuthor": False
            }
            IuLog.doVerbose(__name__,f"entity: {entity}")
         
  
            ugc_posts_create_response = self.restli_client.create(
                resource_path=self.URL_POST,
                entity=entity,
                access_token=ACCESS_TOKEN,
            )
            IuLog.doVerbose(__name__,f"ugc_posts_create_response.status_code: {ugc_posts_create_response.status_code}")
           

            statusCode=ugc_posts_create_response.status_code
            
            IuLog.doVerbose(__name__,f"ugc_posts_create_response.entity: {ugc_posts_create_response.entity}")
            if statusCode==200 or statusCode==201:
                postId= ugc_posts_create_response.entity_id
                IuLog.doDebug(__name__,f"Successfully created post : {postId}")
                return postId
            else:
                raise Exception("ERROR_POST_IMAGE_STATUS_CODE_{statusCode}")
              
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise
        
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doGetUrlUploadFile(self, ACCESS_TOKEN, urn):
        try:
            
            headers = {
                'X-Restli-Protocol-Version': '2.0.0',
                'LinkedIn-Version': self.LINKEDIN_VERSION,
                'Authorization': 'Bearer ' + ACCESS_TOKEN,
            }

            data = {
                "initializeUploadRequest": {
                    "owner": f"{urn}"
                }
            }
            IuLog.doVerbose(__name__,f"data:{data}")
            
            response = requests.post(
                self.URL_INITIALIZE_UPLOAD_FILE, data=json.dumps(data), headers=headers)
            IuLog.doVerbose(__name__,f"response.json():{response.json()}")

         
            responseJson = response.json()
            print(responseJson)
            urlUpload = responseJson['value']['uploadUrl']
            fileID = responseJson['value']['document']

            return fileID, urlUpload
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise

# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doUploadFile(self, ACCESS_TOKEN, urlUpload, dataFile):# pathImage):
        try:
            #userID = self.doGetUserID(ACCESS_TOKEN)
            #print(userID)
            #print(urlUpload, pathImage)
            #curl -i --upload-file ~/Desktop/Mydoc.pdf -H 'Authorization: Bearer Redacted' "https://www.linkedin.com/dms-uploads/D5510AQHXjcP8QBYD9A/ads-uploadedDocument/0?ca=vector_ads&cn=uploads&sync=0&v=beta&ut=36ezHi_Pod5aM1"
            '''
            headers = {
                'X-Restli-Protocol-Version': '2.0.0',
                'LinkedIn-Version': self.LINKEDIN_VERSION,
                'Authorization': 'Bearer ' + ACCESS_TOKEN,
                'media-type-family': 'STILLIMAGE',
            }
            '''
            headers = {
                'Authorization': 'Bearer Redacted'
            }

           # with open(pathImage, "rb") as image_file:
            #    dataImage = image_file.read()
            IuLog.doVerbose(__name__,f"len(dataFile):{len(dataFile)}")
         
            # image = open(pathImage, "rb").read()

            response = requests.put(urlUpload, data=dataFile, headers=headers)
            IuLog.doVerbose(__name__,f"response.status_code:{response.status_code}")
        
            return response.status_code, urlUpload
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise

# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doGetFile(self, ACCESS_TOKEN, id):
        try:
         
            headers = {
                'X-Restli-Protocol-Version': '2.0.0',
                'LinkedIn-Version': self.LINKEDIN_VERSION,
                'Authorization': 'Bearer ' + ACCESS_TOKEN,
                'Content-Type': 'application/json'
                # 'media-type-family': 'STILLIMAGE',
            }

            fileIDEncode = urllib.parse.quote(id)
            urlFile = self.URL_GETFILE + fileIDEncode
            IuLog.doVerbose(__name__,f"urlFile:{urlFile}")

            response = requests.get(urlFile, headers=headers)
            IuLog.doVerbose(__name__,f"response.json():{response.json()}")
            downloadUrl = response.json()["downloadUrl"]
            return downloadUrl
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise

# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doPostFile(self, ACCESS_TOKEN, urn,  dataFile, comment, visibility='PUBLIC'):
        try:
            
            fileID, urlUpload = await self.doGetUrlUploadFile(ACCESS_TOKEN, urn)
            IuLog.doVerbose(__name__,f"urlUpload: {urlUpload} fileID:{fileID}")

            await self.doUploadFile(ACCESS_TOKEN, urlUpload, dataFile)

           # downloadUrl = await self.doGetFile(ACCESS_TOKEN, fileID)
          
            #IuLog.doVerbose(__name__,f"downloadUrl: {downloadUrl}")
            entity = {
                "author": f"{urn}",
                "commentary": f"{comment}",
                "visibility": visibility,
                "distribution": {
                    "feedDistribution": "MAIN_FEED",
                    "targetEntities": [],
                    "thirdPartyDistributionChannels": []
                },
                "content": {
                    "media": {
                        "title": "file",
                        "id": f"{fileID}",
                    }
                },
                "lifecycleState": "PUBLISHED",
            #"isReshareDisabledByAuthor": False
            }
            IuLog.doVerbose(__name__,f"entity: {entity}")
         
  
            ugc_posts_create_response = self.restli_client.create(
                resource_path=self.URL_POST,
                entity=entity,
                access_token=ACCESS_TOKEN,
            )
            IuLog.doVerbose(__name__,f"ugc_posts_create_response.status_code: {ugc_posts_create_response.status_code}")
           

            statusCode=ugc_posts_create_response.status_code
            
            IuLog.doVerbose(__name__,f"ugc_posts_create_response.entity: {ugc_posts_create_response.entity}")
            if statusCode==200 or statusCode==201:
                postId= ugc_posts_create_response.entity_id
                IuLog.doDebug(__name__,f"Successfully created post : {postId}")
                return postId
            else:
                raise Exception("ERROR_POST_IMAGE_STATUS_CODE_{statusCode}")
              
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise
        
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doGetUrlUploadVideo(self, ACCESS_TOKEN, urn):
        try:
            
            headers = {
                'X-Restli-Protocol-Version': '2.0.0',
                'LinkedIn-Version': self.LINKEDIN_VERSION,
                'Authorization': 'Bearer ' + ACCESS_TOKEN,
            }

            data = {
                "initializeUploadRequest": {
                    "owner": f"{urn}"
                }
            }
            IuLog.doVerbose(__name__,f"data:{data}")
            
            response = requests.post(
                self.URL_INITIALIZE_UPLOAD_FILE, data=json.dumps(data), headers=headers)
            IuLog.doVerbose(__name__,f"response.json():{response.json()}")

         
            responseJson = response.json()
            print(responseJson)
            urlUpload = responseJson['value']['uploadUrl']
            fileID = responseJson['value']['document']

            return fileID, urlUpload
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise

# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doUploadVideo(self, ACCESS_TOKEN, urlUpload, dataFile):# pathImage):
        try:
            #userID = self.doGetUserID(ACCESS_TOKEN)
            #print(userID)
            #print(urlUpload, pathImage)
            #curl -i --upload-file ~/Desktop/Mydoc.pdf -H 'Authorization: Bearer Redacted' "https://www.linkedin.com/dms-uploads/D5510AQHXjcP8QBYD9A/ads-uploadedDocument/0?ca=vector_ads&cn=uploads&sync=0&v=beta&ut=36ezHi_Pod5aM1"
            '''
            headers = {
                'X-Restli-Protocol-Version': '2.0.0',
                'LinkedIn-Version': self.LINKEDIN_VERSION,
                'Authorization': 'Bearer ' + ACCESS_TOKEN,
                'media-type-family': 'STILLIMAGE',
            }
            '''
            headers = {
                'Authorization': 'Bearer Redacted'
            }

           # with open(pathImage, "rb") as image_file:
            #    dataImage = image_file.read()
            IuLog.doVerbose(__name__,f"len(dataFile):{len(dataFile)}")
         
            # image = open(pathImage, "rb").read()

            response = requests.put(urlUpload, data=dataFile, headers=headers)
            IuLog.doVerbose(__name__,f"response.status_code:{response.status_code}")
        
            return response.status_code, urlUpload
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise

# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doGetVideo(self, ACCESS_TOKEN, id):
        try:
         
            headers = {
                'X-Restli-Protocol-Version': '2.0.0',
                'LinkedIn-Version': self.LINKEDIN_VERSION,
                'Authorization': 'Bearer ' + ACCESS_TOKEN,
                'Content-Type': 'application/json'
                # 'media-type-family': 'STILLIMAGE',
            }

            fileIDEncode = urllib.parse.quote(id)
            urlFile = self.URL_GETFILE + fileIDEncode
            IuLog.doVerbose(__name__,f"urlFile:{urlFile}")

            response = requests.get(urlFile, headers=headers)
            IuLog.doVerbose(__name__,f"response.json():{response.json()}")
            downloadUrl = response.json()["downloadUrl"]
            return downloadUrl
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doPostVideo(self, ACCESS_TOKEN, urn,  dataImage, comment, visibility='PUBLIC'):
        try:
            
            imageID, urlUpload = await self.doGetUrlUploadImage(ACCESS_TOKEN, urn)
            IuLog.doVerbose(__name__,f"urlUpload: {urlUpload}")
            

            await self.doUploadImage(ACCESS_TOKEN, urlUpload, dataImage)

            #downloadUrl = await self.doGetImage(ACCESS_TOKEN, imageID)
          
           # IuLog.doVerbose(__name__,f"downloadUrl: {downloadUrl}")
            entity = {
                "author": f"{urn}",
                "commentary": f"{comment}",
                "visibility": visibility,
                "distribution": {
                    "feedDistribution": "MAIN_FEED",
                    "targetEntities": [],
                    "thirdPartyDistributionChannels": []
                },
                "content": {
                    "media": {
                        "title": "image",
                        "id": f"{imageID}",
                    }
                },
                "lifecycleState": "PUBLISHED",
            #"isReshareDisabledByAuthor": False
            }
            IuLog.doVerbose(__name__,f"entity: {entity}")
         
  
            ugc_posts_create_response = self.restli_client.create(
                resource_path=self.URL_POST,
                entity=entity,
                access_token=ACCESS_TOKEN,
            )
            IuLog.doVerbose(__name__,f"ugc_posts_create_response.status_code: {ugc_posts_create_response.status_code}")
           

            statusCode=ugc_posts_create_response.status_code
            
            IuLog.doVerbose(__name__,f"ugc_posts_create_response.entity: {ugc_posts_create_response.entity}")
            if statusCode==200 or statusCode==201:
                postId= ugc_posts_create_response.entity_id
                IuLog.doDebug(__name__,f"Successfully created post : {postId}")
                return postId
            else:
                raise Exception("ERROR_POST_IMAGE_STATUS_CODE_{statusCode}")
              
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
  