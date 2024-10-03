#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework import *
from evo_package_linkedin.entity import *

#<
from linkedin_api.clients.restli.client import RestliClient
from linkedin_api.clients.auth.client import AuthClient
import urllib
import math
#>
# ---------------------------------------------------------------------------------------------------------------------------------------
# ULinkedinApi
# ---------------------------------------------------------------------------------------------------------------------------------------
"""ULinkedinApi
"""
class ULinkedinApi():
    __instance = None
# ---------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self):   
        if ULinkedinApi.__instance != None:
            raise Exception("ERROR:SINGLETON")
        else:
            super().__init__()
            ULinkedinApi.__instance = self
            self.currentPath = os.path.dirname(os.path.abspath(__file__))
#<
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
# ---------------------------------------------------------------------------
#>
            
# ---------------------------------------------------------------------------------------------------------------------------------------
    """getInstance Singleton

    Raises:
        Exception:  api exception

    Returns:
        _type_: ULinkedinApi instance
    """
    @staticmethod
    def getInstance():
        if ULinkedinApi.__instance is None:
            uObject = ULinkedinApi()  
        return ULinkedinApi.__instance
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
    async def doDoPost(self, eAction:EAction) -> EAction:
        """doDoPost utility callback
            input: ELinkedinPost
            output: ELinkedinOutput

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

            eLinkedinPost:ELinkedinPost = eAction.doGetInput(ELinkedinPost)
            IuLog.doVerbose(__name__, eLinkedinPost )
           
            #Dispose eAction.input for free memory
            eAction.input = b''

            if eLinkedinPost is None:
                raise Exception("ERROR_REQUIRED|eLinkedinPost|")

#<        
            #Add other check
            '''
            if eLinkedinPost. is None:
                raise Exception("ERROR_REQUIRED|eLinkedinPost.|")
            '''
   
            eLinkedinOutput = await self.doPost(eLinkedinPost)
       

            eAction.enumApiAction = EnumApiAction.COMPLETE
            eAction.doSetOutput(eLinkedinOutput)        
            yield eAction
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doDoGetMe(self, eAction:EAction) -> EAction:
        """doDoGetMe utility callback
            input: ELinkedinInput
            output: ELinkedinOutput

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

            eLinkedinInput:ELinkedinInput = eAction.doGetInput(ELinkedinInput)
           
            #Dispose eAction.input for free memory
            eAction.input = b''

            if eLinkedinInput is None:
                raise Exception("ERROR_REQUIRED|eLinkedinInput|")

#<        
            #Add other check
            '''
            if eLinkedinInput. is None:
                raise Exception("ERROR_REQUIRED|eLinkedinInput.|")
            '''
   
            eLinkedinOutput = ELinkedinOutput()
            eLinkedinOutput.doGenerateID()
            eLinkedinOutput.doGenerateTime()

            eAction.enumApiAction = EnumApiAction.COMPLETE
            eAction.doSetOutput(eLinkedinOutput)        
            yield eAction
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------

#<
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
    async def doPost(self, eLinkedinPost: ELinkedinPost) -> ELinkedinOutput:
        try:
            if eLinkedinPost is None:
                raise ValueError("ERROR_ELinkedinPost_NONE")
            
            IuLog.doInfo(__name__, f"eLinkedinPost: {eLinkedinPost.isCompany}")
            
            urn = f"urn:li:{'organization' if eLinkedinPost.isCompany else 'person'}:{eLinkedinPost.urnId}"
            
            eLinkedinOutput = ELinkedinOutput()
            eLinkedinOutput.doGenerateID()
            
            if eLinkedinPost.eApiFile:
                ext = eLinkedinPost.eApiFile.ext.lower()
                       
                if ext in [".png", ".jpg"]:
                    urnID = await self.doPostImage(eLinkedinPost.token, urn, eLinkedinPost.eApiFile.data, eLinkedinPost.text, eLinkedinPost.visibility)
                elif ext == ".pdf":
                    urnID = await self.doPostFile(eLinkedinPost.token, urn, eLinkedinPost.eApiFile.data, eLinkedinPost.text, eLinkedinPost.visibility)
                elif ext in [".mp4", ".mov"]:
                    urnID = await self.doPostVideo(eLinkedinPost.token, urn, eLinkedinPost.eApiFile.data, len(eLinkedinPost.eApiFile.data), eLinkedinPost.text, eLinkedinPost.visibility)
                else:
                    raise ValueError(f"Unsupported file extension: {ext}")
                
                eLinkedinOutput.urnID = urnID
                return eLinkedinOutput

            # If no file is present, post text content
            urnID = await self.doPostText(eLinkedinPost.token, urn, eLinkedinPost.text, eLinkedinPost.visibility)
            eLinkedinOutput.urnID = urnID
            return eLinkedinOutput

        except Exception as ex:
            IuLog.doException(__name__, ex)
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
    async def doUploadVideo(self, ACCESS_TOKEN, upload_url, data_video, part_size=4194304):
        """Upload the video data to LinkedIn using multipart upload."""
        try:
            headers = {
                'Authorization': 'Bearer ' + ACCESS_TOKEN,
                'Content-Type': 'application/octet-stream'
            }

            total_size = len(data_video)
            part_count = math.ceil(total_size / part_size)
            uploaded_part_ids = []

            for part_number in range(part_count):
                start_byte = part_number * part_size
                end_byte = min(start_byte + part_size, total_size)
                part_data = data_video[start_byte:end_byte]

                IuLog.doVerbose(__name__, f"Uploading part {part_number + 1}/{part_count}, bytes {start_byte}-{end_byte - 1}")

                response = requests.put(upload_url, data=part_data, headers=headers)
                IuLog.doVerbose(__name__, f"response.status_code for part {part_number + 1}: {response.status_code}")

                if response.status_code == 200:
                    # Retrieve the part ID (etag) from the response headers
                    part_id = response.headers.get('etag')
                    if part_id:
                        uploaded_part_ids.append(part_id)
                        IuLog.doVerbose(__name__, f"Part {part_number + 1} uploaded successfully with part ID (etag): {part_id}")
                    else:
                        IuLog.doVerbose(__name__, "No part ID (etag) returned in the response for this part.")
                else:
                    raise Exception(f"Failed to upload part {part_number + 1}. Status code: {response.status_code}")

            # Return the part IDs for the uploaded video parts
            return uploaded_part_ids
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doFinalizeVideoUpload(self, ACCESS_TOKEN, video_id, uploaded_part_ids, upload_token=None):
        """Finalize the video upload with uploaded part IDs."""
        try:
            headers = {
                'X-Restli-Protocol-Version': '2.0.0',
                'LinkedIn-Version': self.LINKEDIN_VERSION,
                'Authorization': 'Bearer ' + ACCESS_TOKEN,
                'Content-Type': 'application/json'
            }

            data = {
                "finalizeUploadRequest": {
                    "video": video_id,
                    "uploadedPartIds": uploaded_part_ids,
                    "uploadToken": upload_token or ""
                }
            }

            IuLog.doVerbose(__name__, f"Finalizing upload for video: {video_id} with parts: {uploaded_part_ids}")

            response = requests.post(
                f"https://api.linkedin.com/rest/videos?action=finalizeUpload",
                data=json.dumps(data),
                headers=headers
            )

            IuLog.doVerbose(__name__, f"Finalization response status code: {response.status_code}, response: {response.text}")
            return response.status_code
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doPostVideo(self, ACCESS_TOKEN, urn, data_video, file_size_bytes, comment, visibility='PUBLIC', upload_captions=False, upload_thumbnail=False):
        """Post the video to LinkedIn with options for captions and thumbnails."""
        try:
            # Step 1: Get the upload URL
            video_id, upload_url = await self.doGetUrlUploadVideo(ACCESS_TOKEN, urn, file_size_bytes, upload_captions, upload_thumbnail)
            IuLog.doVerbose(__name__, f"Upload URL: {upload_url}, Video ID: {video_id}")

            # Step 2: Upload the video (multipart)
            uploaded_part_ids = await self.doUploadVideo(ACCESS_TOKEN, upload_url, data_video)
            IuLog.doVerbose(__name__, f"Uploaded part IDs: {uploaded_part_ids}")

            # Step 3: Finalize the video upload with part IDs
            finalize_status_code = await self.doFinalizeVideoUpload(ACCESS_TOKEN, video_id, uploaded_part_ids)
            IuLog.doVerbose(__name__, f"Finalize upload status code: {finalize_status_code}")
            if finalize_status_code != 200:
                raise Exception(f"Failed to finalize video upload. Status code: {finalize_status_code}")

            # Step 4: Create the LinkedIn post
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
                        "title": "Video Post",
                        "id": f"{video_id}",
                    }
                },
                "lifecycleState": "PUBLISHED",
            }

            IuLog.doVerbose(__name__, f"Post entity: {entity}")

            # Create the post on LinkedIn
            ugc_posts_create_response = self.restli_client.create(
                resource_path=self.URL_POST,
                entity=entity,
                access_token=ACCESS_TOKEN,
            )
            IuLog.doVerbose(__name__, f"Post creation response status code: {ugc_posts_create_response.status_code}")

            if ugc_posts_create_response.status_code in [200, 201]:
                post_id = ugc_posts_create_response.entity_id
                IuLog.doDebug(__name__, f"Successfully created post: {post_id}")
                return post_id
            else:
                raise Exception(f"ERROR_POST_VIDEO_STATUS_CODE_{ugc_posts_create_response.status_code}")

        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doGetUrlUploadVideo(self, ACCESS_TOKEN, urn, file_size_bytes, upload_captions=False, upload_thumbnail=False):
        """Initialize the video upload by getting the upload URL, with options for captions and thumbnail."""
        try:
            headers = {
                'X-Restli-Protocol-Version': '2.0.0',
                'LinkedIn-Version': self.LINKEDIN_VERSION,
                'Authorization': 'Bearer ' + ACCESS_TOKEN,
                'Content-Type': 'application/json'
            }

            data = {
                "initializeUploadRequest": {
                    "owner": f"{urn}",
                    "fileSizeBytes": file_size_bytes,
                    "uploadCaptions": upload_captions,
                    "uploadThumbnail": upload_thumbnail
                }
            }

            IuLog.doVerbose(__name__, f"data: {data}")

            response = requests.post(
                self.URL_INITIALIZE_UPLOAD_VIDEO, data=json.dumps(data), headers=headers
            )

            if response.status_code != 200:
                error_message = response.json().get('message', 'Unknown error')
                raise Exception(f"Video upload initialization failed: {error_message}")

            response_json = response.json()
            IuLog.doVerbose(__name__, f"response.json(): {response_json}")

            video_id = response_json['value']['video']
            upload_url = response_json['value']['uploadInstructions'][0]['uploadUrl']

            return video_id, upload_url
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise
#>
# ---------------------------------------------------------------------------------------------------------------------------------------
