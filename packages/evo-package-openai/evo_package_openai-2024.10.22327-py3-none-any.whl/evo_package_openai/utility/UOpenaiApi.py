#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International  https://github.com/cyborg-ai-git 
#========================================================================================================================================

from evo_framework import *
from evo_package_openai.entity import *
from evo_package_chat.entity.EChatInput import EChatInput
from evo_package_chat.entity.EChatMessage import EChatMessage
from evo_package_chat.entity.EChatModelMapOld import EChatModelMap
from evo_package_chat.entity.EChatMapMessage import EChatMapMessage
from evo_package_chat.entity.EChatMapSession import EChatMapSession

#<
from evo_package_chat.entity.EChatModel import EChatModel
from evo_package_chat.entity.EChatSession import EChatSession

from openai import OpenAI, AuthenticationError, AssistantEventHandler, AsyncAssistantEventHandler
from openai.types.beta import Assistant, Thread, AssistantStreamEvent
from openai.types.beta.threads.message import Message
from evo_package_assistant import *
from evo_package_chat import *
#>
# ---------------------------------------------------------------------------------------------------------------------------------------
# UOpenaiApi
# ---------------------------------------------------------------------------------------------------------------------------------------
"""UOpenaiApi
"""
class UOpenaiApi():
    __instance = None
# ---------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self):   
        if UOpenaiApi.__instance != None:
            raise Exception("ERROR:SINGLETON")
        else:
            super().__init__()
            UOpenaiApi.__instance = self
            self.currentPath = os.path.dirname(os.path.abspath(__file__))
#<
            self.isUseDefault:bool = False
            self.defaultModelID:str = None
            self.defaultAssistantID:str = None
            self.clientOpenai:OpenAI = None
            self.sessionApi:str = "openai"
            self.mapAssistantOpenAI:dict = {}
            
#>
            
# ---------------------------------------------------------------------------------------------------------------------------------------
    """getInstance Singleton

    Raises:
        Exception:  api exception

    Returns:
        _type_: UOpenaiApi instance
    """
    @staticmethod
    def getInstance():
        if UOpenaiApi.__instance is None:
            uObject = UOpenaiApi()  
            uObject.doInit()  
        return UOpenaiApi.__instance
# ---------------------------------------------------------------------------------------------------------------------------------------
    """doInit

    Raises:
        Exception: api exception

    Returns:

    """   
    def doInit(self):   
        try:
#<
            defaultOpenaiToken = CSetting.getInstance().doGet("ACCESS_TOKEN_OPENAI")
            self.defaultModelID = CSetting.getInstance().doGet("OPENAI_DEFAULT_MODELID")
            self.defaultAssistantID = CSetting.getInstance().doGet("OPENAI_DEFAULT_ASSISTANTID")
            
            isUseDefault:bool = True

            if IuText.StringEmpty(defaultOpenaiToken):
                isUseDefault=False
                
            if  IuText.StringEmpty(self.defaultModelID):
                isUseDefault=False
                   
            if  IuText.StringEmpty(self.defaultAssistantID):
                isUseDefault=False
                
            self.isUseDefault = isUseDefault
            
            if self.isUseDefault:
                self.clientOpenai = OpenAI(api_key=defaultOpenaiToken)
                IuLog.doWarning(__name__, "OPENAI_DEFAULT ENV is SET")
            else:
                IuLog.doWarning(__name__,"OPENAI_DEFAULT is none will use only client token input")
                
#>   
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnChatStream(self, eAction:EAction) -> EAction:
        """doOnChatStream utility callback
            input: EChatInput
            output: EChatMessage

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

            eChatInput:EChatInput = eAction.doGetInput(EChatInput)
           
            #Dispose eAction.input for free memory
            eAction.input = b''

            if eChatInput is None:
                raise Exception("ERROR_REQUIRED|eChatInput|")

#<        
            if eChatInput.text is None:
                raise Exception("ERROR_REQUIRED|eChatInput.text|")
              
            eChatMessage = EChatMessage()
            eChatMessage.doGenerateID()
              
              
            eOpenaiInfo = await self.__doGetEOpenaiInfo(eChatInput, 
                                                        isGetAssistantOpenAI=True,
                                                        isGetThreadOpenAI=True,
                                                        isGetEMapMessage=False
                                                        )
            
            clientOpenaAI = eOpenaiInfo.clientOpenaAI     
            assistantIDOpenAI = eOpenaiInfo.assistantIDOpenAI
            threadOpenAI = eOpenaiInfo.threadOpenAI
            
            eChatMessage.sessionID = eOpenaiInfo.threadOpenAI.id
            
            message = clientOpenaAI.beta.threads.messages.create(
              thread_id=threadOpenAI.id,
              role="user",
              content=eChatInput.text
            )
            
            with clientOpenaAI.beta.threads.runs.stream(
                thread_id = threadOpenAI.id,
                assistant_id = assistantIDOpenAI,
            ) as stream:
                for event in stream:
                    #print(event.event)
                    eApiText = self.__doGetEApiTextEvent(eOpenaiInfo, event)
                    if eApiText is not None:
                        eChatMessage.eApiText=eApiText
                        eChatMessage.doGenerateTime()
                        eAction.enumApiAction = EnumApiAction.COMPLETE
                        eAction.doSetOutput(eChatMessage)        
                        yield eAction
                        if eApiText.isError:
                            break
                
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnGetMapModel(self, eAction:EAction) -> EAction:
        """doOnGetMapModel utility callback
            input: EChatInput
            output: EChatModelMap

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

            eChatInput:EChatInput = eAction.doGetInput(EChatInput)
           
            #Dispose eAction.input for free memory
            eAction.input = b''

            if eChatInput is None:
                raise Exception("ERROR_REQUIRED|eChatInput|")

#<        
            eOpenaiInfo = await self.__doGetEOpenaiInfo(eChatInput, 
                                                        isGetAssistantOpenAI=False,
                                                        isGetThreadOpenAI=False,
                                                        isGetEMapMessage=False
                                                        )
            clientOpenaAI = eOpenaiInfo.clientOpenaAI
            arrayModel = (clientOpenaAI.models.list())
   
            eChatModelMap = EChatModelMap()
            eChatModelMap.doGenerateID()
            
            for model in arrayModel:
                eChatModel = EChatModel()
                eChatModel.id = model.id
                eChatModel.name = model.id
                eChatModel.created = model.created
                eChatModelMap.mapEChatModel.doSet(eChatModel)
           

            eAction.enumApiAction = EnumApiAction.COMPLETE
            eAction.doSetOutput(eChatModelMap)        
            yield eAction
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnGetMapMessage(self, eAction:EAction) -> EAction:
        """doOnGetMapMessage utility callback
            input: EChatInput
            output: EChatMapMessage

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

            eChatInput:EChatInput = eAction.doGetInput(EChatInput)
           
            #Dispose eAction.input for free memory
            eAction.input = b''

            if eChatInput is None:
                raise Exception("ERROR_REQUIRED|eChatInput|")

#<        
            eOpenaiInfo = await self.__doGetEOpenaiInfo(eChatInput, 
                                                        isGetAssistantOpenAI=False,
                                                        isGetThreadOpenAI=True,
                                                        isGetEMapMessage=True
                                                        )
           
            eAction.enumApiAction = EnumApiAction.COMPLETE
            eAction.doSetOutput(eOpenaiInfo.eChatMapMessage)        
            yield eAction
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnGetMapSession(self, eAction:EAction) -> EAction:
        """doOnGetMapSession utility callback
            input: EChatInput
            output: EChatMapSession

            Raises:
                Exception: api exception

            Returns:
                EAction:  EObject 
        """   
        try:

            eChatInput:EChatInput = eAction.doGetInput(EChatInput)
           
            #Dispose eAction.input for free memory
            eAction.input = b''

            if eChatInput is None:
                raise Exception("ERROR_REQUIRED|eChatInput|")

#<        
            eOpenaiInfo = await self.__doGetEOpenaiInfo(eChatInput, 
                                                        isGetAssistantOpenAI=False,
                                                        isGetThreadOpenAI=False,
                                                        isGetEMapMessage=False,
                                                        isGetEMapSession=True
                                                        )
          
            eAction.enumApiAction = EnumApiAction.COMPLETE
            eAction.doSetOutput(eOpenaiInfo.eChatMapSession)        
            yield eAction
#>
        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------

#<

# ---------------------------------------------------------------------------------------------------------------------------------------
    async def doOnDelAllAssistantOpenAI(self, eChatInput:EChatInput) -> bool:
        try:
            if eChatInput is None:
                raise Exception("ERROR_REQUIRED|eChatInput|")

      
            eOpenaiInfo = await self.__doGetEOpenaiInfo(eChatInput, 
                                                        isGetAssistantOpenAI=False,
                                                        isGetThreadOpenAI=False,
                                                        isGetEMapMessage=False,
                                                        isGetEMapSession=False
                                                        )
            await self.__doDelAllAssistantOpenAI(eOpenaiInfo.clientOpenaAI)
            
            yield True

        except Exception as exception:
            IuLog.doException(__name__,exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def __doGetEOpenaiInfo(self, 
                                 eChatInput:EChatInput, 
                                 isGetAssistantOpenAI=False,
                                 isGetThreadOpenAI=False,
                                 isGetEMapMessage=False,
                                 isGetEMapSession=False,
                                 ) -> EOpenaiInfo:
        try:
           
            #Default value        
            if self.isUseDefault and self.clientOpenai is not None :
                #Default value 
                clientOpenaAI = self.clientOpenai    
            else:
                #Client value
                #DO NOT COPY OR USE USER INFORMATION, OTHERWISE YOU WILL BE PROSECUTED LEGALLY.
                
                if eChatInput is None:
                     raise Exception("ERROR_REQUIRED|eChatInput|")
                 
                if eChatInput.token is None:
                     raise Exception("ERROR_REQUIRED|eChatInput.token|")
            
                if IuText.StringEmpty(eChatInput.apiToken):
                     raise Exception("ERROR_REQUIRED|eChatInput.apiToken|")
                
                clientOpenaAI = OpenAI(api_key=eChatInput.apiToken)
              
          
            eOpenaiInfo = EOpenaiInfo()
            eOpenaiInfo.doGenerateID(clientOpenaAI.api_key)
            
            eOpenaiInfo.eChatInput = eChatInput
            eOpenaiInfo.clientOpenaAI = clientOpenaAI

            if isGetAssistantOpenAI:
                eOpenaiInfo.eAssistant = await self.__doGetEAssistant(eOpenaiInfo.eChatInput)
                eOpenaiInfo.cAssistantParser = await self.__doGetCAssistantCallbackStream(eOpenaiInfo.eAssistant)
                eOpenaiInfo.assistantIDOpenAI = await self.__doGetAssistantOpenAI(eOpenaiInfo.clientOpenaAI, eOpenaiInfo.eChatInput, eOpenaiInfo.eAssistant) 
                         
            if isGetThreadOpenAI or isGetEMapMessage:
                eOpenaiInfo.threadOpenAI = await  self.__doGetThreadOpenAI(eOpenaiInfo.clientOpenaAI, eOpenaiInfo.eChatInput)
                
            if isGetEMapMessage:
                eOpenaiInfo.eChatMapMessage = await self.__doGetMapMessage(eOpenaiInfo.clientOpenaAI, eOpenaiInfo.threadOpenAI)
                
            if isGetEMapSession:
                eOpenaiInfo.eChatMapSession = await self.__doGetMapSession(eOpenaiInfo.eChatInput)
            
            
            return eOpenaiInfo
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise
          
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def __doGetThreadOpenAI(self, clientOpenaAI:OpenAI, eChatInput:EChatInput) -> Thread :
        try:
            
            if not IuText.StringEmpty(eChatInput.sessionID):
                threadOpenAI = clientOpenaAI.beta.threads.retrieve(eChatInput.sessionID)
                if threadOpenAI is None:
                    raise Exception(f"ERROR_NOT_VALID_SESSIONID|{eChatInput.sessionID}|")
            else:
                threadOpenAI = clientOpenaAI.beta.threads.create()
            
            #SAVE SESSION TREAD
            eChatMapSession = await self.__doGetMapSession(eChatInput)
            eChatSession = EChatSession()
            eChatSession.doGenerateID(threadOpenAI.id)
            eChatSession.sessionID = threadOpenAI.id
            eChatSession.sessionApi = self.sessionApi
            eChatMapSession.mapEChatSession.doSet(eChatSession)

            IuLog.doVerbose(__name__, f"eChatMapSession:\n{eChatMapSession}\n{eChatSession}")
            return threadOpenAI
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise

# ---------------------------------------------------------------------------------------------------------------------------------------
    async def __doGetMapMessage(self, clientOpenaAI:OpenAI, threadOpenAI:Thread ) -> EChatMapMessage :
        try:
            
            thread_messages = clientOpenaAI.beta.threads.messages.list(threadOpenAI.id)
            #print("thread_messages:\n",thread_messages.data, "\n")
            
            eMapMessage = EChatMapMessage()
            eMapMessage.doGenerateID(threadOpenAI.id)
            eMapMessage.sessionID=threadOpenAI.id
                 
            for message in thread_messages.data:
                eApiText = EApiText()
                eApiText.doGenerateID(message.id)
                eApiText.text = f"{message.content}"
                eMessage = EChatMessage()
                eMessage.id = message.id
                eMessage.eApiText = eApiText 
                eMapMessage.mapEChatMessage.doSet(eMessage)

            return eMapMessage
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def __doGetMapSession(self, eChatInput:EChatInput) -> EChatMapSession:
        try:
            #Default value        
            if self.isUseDefault and self.clientOpenai is not None :
                #Default value  RETURN EMPTY for privacy 
                eChatMapSession = EChatMapSession()
                eChatMapSession.doGenerateID()
              
            else:
                #Client value
                #DO NOT COPY OR USE USER INFORMATION, OTHERWISE YOU WILL BE PROSECUTED LEGALLY.
                if IuText.StringEmpty(eChatInput.token):
                    raise Exception("ERROR_REQUIRED|eChatInput.token|")
                IuLog.doVerbose(__name__, f"token:{eChatInput.token}\nUChatApi.getInstance().mapEChatMapSession:\n{UChatApi.getInstance().mapEChatMapSession}")
                
                eChatMapSession = UChatApi.getInstance().mapEChatMapSession.doGet(eChatInput.token)
                
                if eChatMapSession is None:
                    eChatMapSession = EChatMapSession()
                    eChatMapSession.id = eChatInput.token
                    
                    UChatApi.getInstance().mapEChatMapSession.doSet(eChatMapSession)
         
            return eChatMapSession
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise   
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def __doGetModelID(self, eChatInput:EChatInput) -> str:
        try:
            #Default value        
            if self.isUseDefault and self.clientOpenai is not None :
                #Default value 
                openaiModelID = self.defaultModelID
              
            else:
                #Client value
                #DO NOT COPY OR USE USER INFORMATION, OTHERWISE YOU WILL BE PROSECUTED LEGALLY.
                if IuText.StringEmpty(eChatInput.modelID):
                    raise Exception("ERROR_REQUIRED|eChatInput.modelID|")
                
                openaiModelID=eChatInput.modelID
            
            return openaiModelID
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise      
          
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def __doGetEAssistant(self, eChatInput:EChatInput) -> EAssistant:
        try:
          
            if IuText.StringEmpty(eChatInput.eAssistantID):
                eAssistantID = self.defaultAssistantID
            else:
                eAssistantID= eChatInput.eAssistantID

            if IuText.StringEmpty(eAssistantID):
              raise Exception("ERROR_REQUIRED|eChatInput.eAssistantID|")
            
            eAssistant= await UAssistant.getInstance().doGetEAssistant(eAssistantID)
            
            return eAssistant
            
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise
          
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def __doSetAssistantOpenAI(self, clientOpenaAI:OpenAI, eChatInput:EChatInput, eAssistant:EAssistant, ) -> str:
        try:
            
            modelID = await self.__doGetModelID(eChatInput)
            
            print(eAssistant)
            
            eMessageSystem:EAssistantMessage = eAssistant.mapEAssistantMessage.doGet(eAssistant.systemID)
            IuLog.doVerbose(__name__, f"eMessageSystem:{eMessageSystem}")
            
            assistant = clientOpenaAI.beta.assistants.create(
              name=eAssistant.id.hex(),
              instructions=eMessageSystem.message,
              ##tools=[{"type": "code_interpreter"}],
              model=modelID,
            )
 
            return assistant.id
            
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def __doGetAssistantOpenAI(self,clientOpenAI:OpenAI, eChatInput:EChatInput, eAssistant:EAssistant) -> str: # Assistant:
        try:
            
            assistantID:str = None
            if eAssistant.id in self.mapAssistantOpenAI:
                assistantID=self.mapAssistantOpenAI[eAssistant.id]
          
            else:
                listAssistant = await self.__doQueryAssistantOpenAI(clientOpenAI)
                
                IuLog.doVerbose(__name__, f"assistantQuery:{len(listAssistant)}")
                
                #Sorry O(n) request at this moment no OpenAI api for get by name 
                for assistant in listAssistant:
                    IuLog.doVerbose(__name__, f"\t{assistant.id} => {assistant.name}")
                    if assistant.name == eAssistant.id:
                        assistantID = assistant.id
                        break
                             
                if assistantID is None:
                    assistantID = await self.__doSetAssistantOpenAI(clientOpenAI, eChatInput, eAssistant)
                            
               #assistantOpenAI = client.beta.assistants.retrieve("assistantID")
            
            return assistantID
            
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise 
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def __doQueryAssistantOpenAI(self,clientOpenAI:OpenAI, limit=10) -> List[Assistant]:
        try:
          
            #Sorry O(n) request at this moment no OpenAI api for get by name             
            assistantQuery = clientOpenAI.beta.assistants.list(
                order="desc",
                limit=limit,
            )
            
            IuLog.doVerbose(__name__, f"assistantQuery:{assistantQuery.data}")
            return assistantQuery.data
           
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise 
# ---------------------------------------------------------------------------------------------------------------------------------------
    async def __doDelAllAssistantOpenAI(self,clientOpenAI:OpenAI):
        try:
          
            #Sorry O(n) request at this moment no OpenAI api for get by name             
            assistantQuery = clientOpenAI.beta.assistants.list(
                order="desc",
                limit=100,
            )
            
            IuLog.doVerbose(__name__, f"assistantQuery:{len(assistantQuery.data)}")
            
            for assistant in assistantQuery.data:
                response = clientOpenAI.beta.assistants.delete(assistant.id)
                IuLog.doVerbose(__name__, f"del:{assistant.id} => {response}")
            
            return True
           
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise   

# ---------------------------------------------------------------------------------------------------------------------------------------
    async def __doGetCAssistantCallbackStream(self, eAssistant:EAssistant) -> CAssistantCallbackStream:
        try:
            if eAssistant.callback is not None:
                cAssistantParser = eAssistant.callback()
            else:
                cAssistantParser = CAssistantCallbackStream()
                
            return cAssistantParser
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise 
# ---------------------------------------------------------------------------------------------------------------------------------------      
    def __doGetEApiTextEvent(self,eOpenaiInfo:EOpenaiInfo,event:AssistantStreamEvent) -> EApiText:
        try:
            
            cAssistantParser=eOpenaiInfo.cAssistantParser
            #IuLog.doVerbose(__name__, event.event)
            #IuLog.doVerbose(__name__, event)
            #TODO:O(n) move to map callback O(1)
            if event.event == 'thread.message.delta':
                        #data is a message delta
                        #Occurs when parts of a Message are being streamed.
                        text= event.data.delta.content[0].text.value        
                        eApiText = cAssistantParser.doParser(text)
                        return eApiText
                               
            elif event.event == 'thread.message.created':                        
                #data is a message
                #Occurs when a message is created.
                cAssistantParser.onMessageCreated()
                return None
            
            elif event.event == 'thread.message.in_progress':                        
                #data is a message
                #Occurs when a message moves to an in_progress state.
                cAssistantParser.onMessageInProgess()
                return None
            
            elif event.event == 'thread.message.completed':                        
                #data is a message
                #Occurs when a message is completed.
                cAssistantParser.onMessageCompleted()
                return None
            
            elif event.event == 'thread.message.incomplete':
                #data is a message
                #Occurs when a message ends before it is completed.
                cAssistantParser.onMessageIncomplete()
                return None
            
            elif event.event == 'thread.created':
                #data is a thread
                #Occurs when a new thread is created.
                cAssistantParser.onThreadCreated()
                return None
            
            elif event.event == 'thread.run.created':
                #data is a run
                #Occurs when a new run is created.
                cAssistantParser.onRunCreated()
                return None
            
            elif event.event == 'thread.run.queued':
                #data is a run
                #Occurs when a run moves to a queued status.
                cAssistantParser.onRunQuequed()
                return None
            
            elif event.event == 'thread.run.in_progress':
                #data is a run
                #Occurs when a run moves to an in_progress status.
                cAssistantParser.onRunInProgress()
                return None
            
            elif event.event == 'thread.run.requires_action':
                #data is a run
                #Occurs when a run moves to a requires_action status.
                cAssistantParser.onRequiresAction()
                return None
            
            elif event.event == 'thread.run.completed':
                #data is a run
                #Occurs when a run is completed.
                cAssistantParser.onRunCompleted()
                return None
            
            elif event.event == 'thread.run.incomplete':
                #data is a run
                #Occurs when a run ends with status incomplete.
                cAssistantParser.onRunIncomplete()
                return None
            
            elif event.event == 'thread.run.failed':
                #data is a run
                #Occurs when a run fails.
                cAssistantParser.onRunFailed()
                return None
            
            elif event.event == 'thread.run.cancelling':
                #data is a run
                #Occurs when a run moves to a cancelling status.
                cAssistantParser.onRunCancelling()
                return None
            
            elif event.event == 'thread.run.cancelled':
                #data is a run
                #Occurs when a run is cancelled.
                cAssistantParser.onRunCancelled()
                return None
            
            elif event.event == 'thread.run.expired':
                #data is a run
                #Occurs when a run expires.
                cAssistantParser.onRunExpired()
                return None
            
            elif event.event == 'thread.run.step.created':
                #data is a run step
                #Occurs when a run step is created.
                cAssistantParser.onRunStepCreated()
                return None
            
            elif event.event == 'thread.run.step.in_progress':
                #data is a run step
                #Occurs when a run step moves to an in_progress state.
                cAssistantParser.onRunStepInProgress()
                return None
            
            elif event.event == 'thread.run.step.delta':
                #data is a run step delta
                #Occurs when parts of a run step are being streamed.
                cAssistantParser.onRunStepDelta()
                return None
            
            elif event.event == 'thread.run.step.completed':
                #data is a run step
                #Occurs when a run step is completed.
                cAssistantParser.onRunStepCompleted()
                return None
            
            elif event.event == 'thread.run.step.failed':
                #data is a run step
                #Occurs when a run step fails.
                cAssistantParser.onRunStepFailed()
                return None
            
            elif event.event == 'thread.run.step.cancelled':
                #data is a run step
                #Occurs when a run step is cancelled.
                cAssistantParser.onRunStepCancelled()
                return None
            
            elif event.event == 'thread.run.step.expired':
                #data is a run step
                #Occurs when a run step expires.
                cAssistantParser.onRunStepExpired()
                return None
            
            elif event.event == 'error':
                #data is an error
                #Occurs when an error occurs. This can happen due to an internal server error or a timeout.
                cAssistantParser.onError()
                return None
            
            elif event.event == 'done':
                #data is [DONE]
                #Occurs when a stream ends.
                cAssistantParser.onDone()
                return None
            
            return None
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise  
#>
# ---------------------------------------------------------------------------------------------------------------------------------------