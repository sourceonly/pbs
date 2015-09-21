#!/usr/bin/python



'''

Copyright (C) 2003-2010 Altair Engineering, Inc. All rights reserved.

'''



import os
import sys
import ConfigurationUtils
import ApplicationManager
import xml.dom.minidom

from xml.dom.minidom import Node



class SoapEnvelopeError(Exception):
    pass
  

class MandatoryParameterNotFound(SoapEnvelopeError):
    pass 

    
class InvalidParameter(SoapEnvelopeError):
    pass 


class SoapEnvelope(object):


    def __init__(self):#{{{
        self.__xmlVersionTag = """<?xml version="1.0" encoding="UTF-8"?>"""
        self.__soapenvStartTag = """<soapenv:Envelope xmlns:app="http://schemas.altair.com/pbs/2007/02/app-def" xmlns:por="http://schemas.altair.com/pbs/2007/03/portal" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">"""
        self.__soapenvEndTag = """</soapenv:Envelope>"""
        self.__appDefXmlns = """http://schemas.altair.com/pbs/2007/02/app-def"""
    #}}}

            

    def getHeader(self):#{{{
        cofigUtils = ConfigurationUtils.ConfigurationUtils()
        user = cofigUtils.getUser()
        passwd = cofigUtils.getPassword()
      
        header = """
                <soapenv:Header>
                <wsse:Security soapenv:mustUnderstand="1" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
                <wsse:UsernameToken wsu:Id="UsernameToken-29445027" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                <wsse:Username>"""
        header = header + user
        header = header + """</wsse:Username>
        <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">"""
        header = header + passwd
        header = header + """</wsse:Password>
            <wsse:Nonce>uwt9yGeT4PqfBsnvac/9nQ==</wsse:Nonce>
            <wsu:Created>2009-11-11T10:47:03.609Z</wsu:Created>
            </wsse:UsernameToken>
            </wsse:Security>
            </soapenv:Header>
                 """
        return header
    #}}}
    # End of method getHeader()

        

    def getJobSubmitBody(self, parametersMap):#{{{
        body = """<soapenv:Body>
              <ns5:SubmitJob xmlns:ns5="http://schemas.altair.com/pbs/2007/03/portal">
              <job>"""        
      
        body = body + self.createAndValidateJob(parametersMap)
        body = body + """</job>
              </ns5:SubmitJob>
              </soapenv:Body>"""
        return body
    #}}}
    # End of method getHeader()


    def createAndValidateJob(self, parametersMap):#{{{
        appMgr = ApplicationManager.ApplicationManager()
#        application = parametersMap["ApplicationName"]
        application = parametersMap["ApplicationId"]
        appDef = appMgr.getApplicationDef(application)        

     
        #Set xmlns for applicationId tag
        appIdNode = appDef.getElementsByTagName("ApplicationId")[0]                
        appIdNode.setAttribute("xmlns", self.__appDefXmlns)
        argChoiceList = appDef.getElementsByTagName("ArgumentChoice")
        userKeys = parametersMap.keys()        
      
        name_list=[];
        for argChoice in argChoiceList:            
            name = argChoice.getElementsByTagName("Name")            
            name = self.getElementValue(name[0].toxml())            
            name_list+=[name];
		
            InputRequired = argChoice.getElementsByTagName("InputRequired")
            if(len(InputRequired) != 0):
                InputRequired = self.getElementValue(InputRequired[0].toxml())                
            else:
                InputRequired = None
                                  
            # Check if the "Name" tag value is specified in user input
		
            if name in userKeys:
                userValue = parametersMap[name]                
		
                #if user key contains blank value throw exception
                if(len(userValue) == 0 and InputRequired == "true"):
                    msg = "should specify value for mandatory parameter: " + name 
                    raise InvalidParameter, msg                      
                else:
                    #User has specifed mandatory value
                    # Now we can add the value in soap request
                    if userValue.strip() == "":
                        #Remove those elements(ArgumentChoise) from app def which are not supplied by user
                        rootNode = appDef.getElementsByTagName("return")[0]
                        rootNode.removeChild(argChoice)                                                
                    elif argChoice.getElementsByTagName("ArgumentDateTime").length != 0:
                        if ';' not in userValue:
                            msg = "Input for ArgumentDateTime should be in DATE;TIME format"
                            raise InvalidParameter, msg
                        dateTag = argChoice.firstChild.getElementsByTagName("Date")
                        if dateTag.length != 0:
                            date = appDef.createTextNode(userValue.split(';')[0])
                            dateTag[0].replaceChild(date,dateTag[0].firstChild)
                        else:
                            ele = appDef.createElement("Date")                       
                            txt = appDef.createTextNode(userValue.split(';')[0])
                            ele.appendChild(txt)
                            argChoice.childNodes[0].appendChild(ele)
                            argChoice.setAttribute("xmlns", self.__appDefXmlns)
                        timeTag = argChoice.firstChild.getElementsByTagName("Time")
                        if timeTag.length != 0:
                            time = appDef.createTextNode(userValue.split(';')[1])
                            timeTag[0].replaceChild(time,timeTag[0].firstChild)
                        else:
                            ele = appDef.createElement("Time")                       
                            txt = appDef.createTextNode(userValue.split(';')[1])
                            ele.appendChild(txt)
                            argChoice.childNodes[0].appendChild(ele)
                            argChoice.setAttribute("xmlns", self.__appDefXmlns)
                    elif argChoice.getElementsByTagName("ArgumentBooleanWithDescription").length != 0:
                        featureList = argChoice.firstChild.getElementsByTagName("FeatureEnabled")
                        if featureList.length != 0:
                            txt = appDef.createTextNode(userValue)
                            featureList[0].replaceChild(txt,featureList[0].firstChild)
                        else:
                            ele = appDef.createElement("FeatureEnabled")                       
                            txt = appDef.createTextNode(userValue)
                            ele.appendChild(txt)
                            argChoice.childNodes[0].appendChild(ele)
                            argChoice.setAttribute("xmlns", self.__appDefXmlns)
                    else:
                        ele = appDef.createElement("Value")                       

                        txt = appDef.createTextNode(userValue)
                        ele.appendChild(txt)
                        argChoice.childNodes[0].appendChild(ele)
                        argChoice.setAttribute("xmlns", self.__appDefXmlns)
                  
            elif (InputRequired == "true"):
                msg = "should specify mandatory parameter: " + name 
                raise MandatoryParameterNotFound, msg                
                  

	appDef_doc=appDef	
        appDef = appDef.getElementsByTagName("return")[0]  

	for this_key in userKeys:
		if this_key in name_list: 
			continue
		ele = appDef_doc.createElement("Value")
		txt = appDef_doc.createTextNode(parametersMap[this_key])
		ele.appendChild(txt)
	
		nln = appDef_doc.createElement("Name")
		txt = appDef_doc.createTextNode(this_key)
		nln.appendChild(txt)
		arg=appDef_doc.createElement("ArgumentChoice")
		arg.appendChild(ele);
		arg.appendChild(nln);
		appDef.appendChild(arg);	


        childList = appDef.childNodes
        returnAppDefString = ""
        for child in childList:        
            returnAppDefString = returnAppDefString + child.toxml()        

	#print returnAppDefString
        return returnAppDefString                       
    #}}}
    #End of method createJob()




    



   #}}}

    def getElementValue(self, xmlString):#{{{   
        startIndex = xmlString.find(">")+1
        endIndex = xmlString.rfind("<")
        value = xmlString[startIndex : endIndex]
        return value
    #}}}


    '''
    Creates SOAP envelop for submitting job
    '''
    def createJobSubmitEnvelop(self, parametersMap):#{{{
        # a soap message
        soapMessage = None
        soapMessage = self.__xmlVersionTag
        soapMessage = soapMessage + self.__soapenvStartTag
        soapMessage = soapMessage + self.getHeader()
        soapMessage = soapMessage + self.getJobSubmitBody(parametersMap)
        soapMessage = soapMessage + self.__soapenvEndTag        
        return soapMessage
    #}}}
    # End of method createJobSubmitEnvelop()

    

  
    def createGetApplicationEnvelop(self, application = None):#{{{
        # a soap message
        soapMessage = None
        soapMessage = self.__xmlVersionTag
        soapMessage = soapMessage + self.__soapenvStartTag
        soapMessage = soapMessage + self.getHeader()
        soapMessage = soapMessage + self.getApplicationBody(application)
        soapMessage = soapMessage + self.__soapenvEndTag        
        return soapMessage
    #}}}
    # End of method createGetApplicationEnvelop()

   
    
    def getApplicationBody(self, application = None):#{{{
        body = """<soapenv:Body>      
        <por:GetApplicationDefinitions>                          
               <extensions>"""
        if application != None:
            body = body + application
        body = body + """</extensions>      
               </por:GetApplicationDefinitions>   
               </soapenv:Body>"""
        return body       
    #}}}
    #End of method getApplicationBody()
   
  
    def createGetJobStatusEnvelop(self, jobId = None):#{{{
            # a soap message
            soapMessage = None
            soapMessage = self.__xmlVersionTag
            soapMessage = soapMessage + self.__soapenvStartTag
            soapMessage = soapMessage + self.getHeader()
            soapMessage = soapMessage + self.getJobStatusBody(jobId)
            soapMessage = soapMessage + self.__soapenvEndTag        
            return soapMessage
    #}}}
    # End of method createGetJobStatusEnvelop()


    def createGetJobSummaryEnvelop(self, jobId = None):#{{{
            soapMessage = None
            soapMessage = self.__xmlVersionTag
            soapMessage = soapMessage + self.__soapenvStartTag
            soapMessage = soapMessage + self.getHeader()
            soapMessage = soapMessage + self.getJobSummaryBody(jobId)
            soapMessage = soapMessage + self.__soapenvEndTag
            return soapMessage
    #}}}
    # End of method createGetJobSummaryEnvelop()


    def createJobDelete(self, jobId):#{{{
            # a soap message
            soapMessage = None
            soapMessage = self.__xmlVersionTag
            soapMessage = soapMessage + self.__soapenvStartTag
            soapMessage = soapMessage + self.getHeader()
            soapMessage = soapMessage + self.getJobDeleteBody(jobId)
            soapMessage = soapMessage + self.__soapenvEndTag
            return soapMessage
        #}}}
    # End of method createcreateJobDelete()


    def getJobDeleteBody(self, jobId):
        body = """<soapenv:Body>
        <por:TerminateJob>
            <jobId>"""
        body = body + jobId
        body = body + """</jobId>
            </por:TerminateJob>
            </soapenv:Body>"""
        return body



    def getJobStatusBody(self, jobId = None):#{{{
        body = """<soapenv:Body>
        <por:GetJobs>"""
        if jobId != None:
            body = body + """<filter>
                    <currentFilter>JOB_ID</currentFilter>
                    <filterValuesStr>"""
            body = body + jobId
            body = body + """</filterValuesStr>
                </filter>"""
            body = body + """<filter>
                    <currentFilter>SUB_JOBS</currentFilter>
                    <filterValuesStr>true</filterValuesStr>
                </filter>"""
              
        body = body + """</por:GetJobs>
                  </soapenv:Body>"""         
        return body       
    #}}}

    def getJobSummaryBody(self, jobId = None):#{{{
            body = """<soapenv:Body>
            <por:GetJobsSummary>"""
            if jobId != None:
                body = body + """<filter>
                <currentFilter>JOB_ID</currentFilter>
                <filterValuesStr>"""
                body = body + jobId
                body = body + """</filterValuesStr>
                </filter>"""
            body = body + """</por:GetJobsSummary>
                  </soapenv:Body>"""
            return body    
    #}}}
    def createPingServerSOAP(self):
            # a soap message
            soapMessage = None
            soapMessage = self.__xmlVersionTag
            soapMessage = soapMessage + self.__soapenvStartTag
            soapMessage = soapMessage + self.getPingHeader()
            soapMessage = soapMessage + self.getPingServerBody()
            soapMessage = soapMessage + self.__soapenvEndTag
            return soapMessage
        #}}}
    # End of method createcreateJobDelete()

    def getPingServerBody(self):
            body = """<soapenv:Body>
              <por:PingServer>
                  </por:PingServer>
                  </soapenv:Body>"""
            return body

    def getPingHeader(self):#{{{
        user = "dummy1"
        passwd = "dummy1"

        header = """
                 <soapenv:Header>
             <wsse:Security soapenv:mustUnderstand="1" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
             <wsse:UsernameToken wsu:Id="UsernameToken-29445027" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
             <wsse:Username>"""
        header = header + user
        header = header + """</wsse:Username>
             <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">"""
        header = header + passwd
        header = header + """</wsse:Password>
             <wsse:Nonce>uwt9yGeT4PqfBsnvac/9nQ==</wsse:Nonce>
             <wsu:Created>2009-11-11T10:47:03.609Z</wsu:Created>
             </wsse:UsernameToken>
             </wsse:Security>
                 </soapenv:Header>
                 """
        return header
    #}}}
    # End of method getHeader()

