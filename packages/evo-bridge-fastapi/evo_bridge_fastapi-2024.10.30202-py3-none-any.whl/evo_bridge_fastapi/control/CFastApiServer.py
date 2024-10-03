#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git |
#========================================================================================================================================


import importlib.metadata
import ssl
try:
    evo_framework_version = importlib.metadata.version('evo_framework')
    print(f"evo_framework version: {evo_framework_version}")
except importlib.metadata.PackageNotFoundError:
    raise Exception("ERROR_NOT_ISTALLED|evo_framework")

from evo_framework import *

import uvicorn
from fastapi import BackgroundTasks
from fastapi import FastAPI, HTTPException
from fastapi import Request as RequestFastApi
from fastapi.responses import FileResponse
from fastapi import Response as ResponseFastApi
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, MutableMapping
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime
from typing import BinaryIO
from fastapi import HTTPException, Request, status
from fastapi.responses import StreamingResponse
import struct

current_path = os.path.dirname(os.path.abspath(__file__))

class CustomStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope: MutableMapping[str, Any]):
        response = await super().get_response(path, scope)
        response.headers["ngrok-skip-browser-warning"] = "1234"

        if path.endswith(".mp4") and isinstance(response, FileResponse):
            response.headers["Content-Type"] = "video/mp4"

        if isinstance(response, FileResponse):
            print("response HEADER", path, response.headers)

        return response

#CORS ALLOW
origins = ["*"]

static_files_dir = f"{current_path}/../assets"
#templates = Jinja2Templates(directory=f"{current_path}/../assets_template")

# ----------------------------------------------------------------------------------------------------------------------------------------  
class CFastApiServer(CBridge):
    __instance = None

    def __init__(self):
        CFastApiServer.__instance = self
        self.version = "20240130"
        self.eApiConfig = CApiFlow.getInstance().eApiConfig
        self.app = FastAPI()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.app.mount(
            "/assets", CustomStaticFiles(directory=static_files_dir), name="assets"
        ) 
        self.mapEClass = {}
        self.mapEAction = {}
        self.currentPathCOnfig = os.path.dirname(os.path.abspath(__file__))
        self.actionPath = "do_action"
# ----------------------------------------------------------------------------------------------------------------------------------------  
    @staticmethod
    def getInstance():
        if CFastApiServer.__instance is None:
            cObject = CFastApiServer()
            # cObject.doInit()
        return CFastApiServer.__instance

# ----------------------------------------------------------------------------------------------------------------------------------------  
    async def doInit(self):
        try:
            CApiFlow.getInstance().doInit()
            
            if IuText.StringEmpty(self.eApiConfig.remoteUrl):
                if self.eApiConfig.enumApiTunnel ==  EnumApiTunnel.LOCAL:
                    if self.eApiConfig.localAddress == "0.0.0.0":
                        self.eApiConfig.remoteUrl = (
                            f"http://{IuSystem.get_local_ip()}:{str(self.eApiConfig.remotePort)}"
                        )
                    else:
                        self.eApiConfig.remoteUrl = (
                            f"http://{self.eApiConfig.localAddress}:{str(self.eApiConfig.remotePort)}"
                        )
        
                elif self.eApiConfig.enumApiTunnel == EnumApiTunnel.NGROK:
                    from evo_package_tunnel.utility.IuTunnelNGrok import IuTunnelNgrok
                    ENV_TUNNEL_TOKEN_NGROK = CSetting.getInstance().doGet("ENV_TUNNEL_TOKEN_NGROK")
                    if IuText.StringEmpty(ENV_TUNNEL_TOKEN_NGROK):
                        raise Exception("ERROR_REQUIRED_ENV|ENV_TUNNEL_TOKEN_NGROK")

                    self.eApiConfig.remoteUrl = await IuTunnelNgrok.do_use_ngrok(
                        ENV_TUNNEL_TOKEN_NGROK, self.eApiConfig.remotePort
                    )
                    
                elif self.eApiConfig.enumApiTunnel == EnumApiTunnel.PINGGY:
                    from evo_package_tunnel.utility.IuTunnelPinggy import IuTunnelPinggy
                    pinggyToken = ""  # CSetting.getInstance().mapSetting["ENV_TUNNEL_TOKEN_PINGGY"]
                    
                    self.eApiConfig.remoteUrl = await IuTunnelPinggy.do_use_pinggy(
                        pinggyToken, self.eApiConfig.remotePort
                    )
                    
                else:
                    raise Exception("SORRY_TUNNEL_NOT_STILL_SUPPORTED")
                
                '''
                elif self.eApiConfig.enumApiTunnel == EnumApiTunnel.CLOUDFLARE:
                    from evo_package_tunnel.utility.IuTunnelCloudFlare import IuTunnelCloudFlare
                    self.eApiConfig.remoteUrl = await IuTunnelCloudFlare.do_use_cloudflare(
                        self.eApiConfig.remotePort
                    )
                '''
                
               

            await CApiFlow.getInstance().doInitEApiConfig()
            
        except Exception as exception:
            IuLog.doException(__name__, exception)
            raise Exception


# ----------------------------------------------------------------------------------------------------------------------------------------  
    async def doRunServer(self):
        try:
            await self.doInit()

            # -----------------------------------------------------------------------------------------------------------------------------
            @self.app.post("/do_action", tags=["action"])
            async def do_action(
                request: RequestFastApi, background_tasks: BackgroundTasks
            ):
                try:
                    
                    ip_caller = request.client.host if request.client else "Unknown"
                     
                    IuLog.doVerbose(__name__, f"ipcaller:{ip_caller}")
                    
                    dataERequest = await request.body()
                    
                    return StreamingResponse(CApiFlow.getInstance().doEAction(dataERequest, isAddHeader=True),
                                            media_type="application/octet-stream"
                                            ,background=background_tasks
                                            )

                except Exception as exception:
                    IuLog.doException(__name__, exception)
                    return ResponseFastApi(content= "Error processing the action ", status_code=500)
                    
            # -----------------------------------------------------------------------------------------------------------------------------
            @self.app.on_event("shutdown")
            async def shutdown_event():
                try:
                    IuLog.doInfo(__name__, "Shutdown event")
                # await CRtcServer.getInstance().onShutdown()
                except Exception as exception:
                    IuLog.doException(__name__, exception)

            # -----------------------------------------------------------------------------------------------------------------------------
            CSetting.getInstance().eSettings.remoteUrl = self.eApiConfig.remoteUrl
            IuApi.doPrintPackage()
            #IuLog.doInfo(__name__, f"versionServer: {self.version}")
            IuLog.doDebug(__name__, f"eApiConfig: {self.eApiConfig}")
            IuLog.doInfo(
                __name__, f"remote_url: {CSetting.getInstance().eSettings.remoteUrl}"
            )
            
            self.doPrintMapEApi()

            pathQrCode = static_files_dir + "/qrcode.png"
            pathQrLogo = static_files_dir + "/logo.png"
            await IuQrCode.doGenerate(
                self.eApiConfig.cyborgaiToken, pathQrCode, pathQrLogo
            )
            print(f"▼{self.eApiConfig.cyborgaiToken}▲\n")
           
            
            ssl_key_password_env = CSetting.getInstance().doGet("CYBORGAI_SSL_KEY_PASSWORD")
            ssl_key_env = CSetting.getInstance().doGet("CYBORGAI_SSL_KEY")
            ssl_cert_env = CSetting.getInstance().doGet("CYBORGAI_SSL_CERT")
            
            isUseSSL = False
            
            sslCertPinning = ""
           
            if not IuText.StringEmpty(ssl_key_env) and not IuText.StringEmpty(ssl_cert_env):
                
                #FOR DOCKER env fix...
                ssl_keyPassword = ssl_key_password_env
                ssl_keyPem = ssl_key_env.replace('\\n', '\n')
                ssl_certPem= ssl_cert_env.replace('\\n', '\n')
                
                IuLog.doInfo(__name__, f"SSL cert sha256:{IuCryptHash.toSha256(ssl_certPem)}")

                IuLog.doDebug(__name__, f"SSL Cert:\n{ssl_certPem}\n")
                
                ssl_keyFile = "/tmp/cyborgai_key.pem"
                ssl_certFile = "/tmp/cyborgai_cert.pem"
                
                sslPkPinning = IuCryptHash.toSha256(ssl_certPem.encode())
                
                
                await IuFile.doWrite(ssl_keyFile, ssl_keyPem.encode())
                await IuFile.doWrite(ssl_certFile, ssl_certPem.encode())
                
             
                IuLog.doInfo(__name__, "use ssl certificate: true")
                config = uvicorn.Config(
                    app=self.app,
                    host=self.eApiConfig.localAddress,
                    port=self.eApiConfig.localPort,
                    ssl_keyfile_password= ssl_keyPassword,
                    ssl_keyfile=ssl_keyFile,
                    ssl_certfile=ssl_certFile,
                    loop="asyncio",
                )
                
                
                
                #os.remove(ssl_keyFile)
                #os.remove(ssl_certFile)
                
                self.eApiConfig.remoteUrl = self.eApiConfig.remoteUrl.replace("http:", "https:")
                isUseSSL = True
               
            else:
                
                IuLog.doInfo(__name__, "use ssl certificate: false")
                config = uvicorn.Config(
                    app=self.app,
                    host=self.eApiConfig.localAddress,
                    port=self.eApiConfig.localPort,
                    loop="asyncio",
                )
                
            IuLog.doInfo(__name__, f"QRCode: {self.eApiConfig.remoteUrl}/assets/qrcode.png")
            IuLog.doInfo(__name__, f"Type: {self.eApiConfig.enumEApiBridgeType.name}")
            IuLog.doInfo(__name__, f"Visibility: {self.eApiConfig.enumApiVisibility.name}")
            IuLog.doInfo(__name__, f"Local: {self.eApiConfig.localAddress}:{self.eApiConfig.localPort}")
            IuLog.doInfo(__name__, f"Remote port: {self.eApiConfig.remotePort}")
            IuLog.doInfo(__name__, f"Remote url: {self.eApiConfig.remoteUrl}/{self.actionPath}")
            IuLog.doInfo(__name__, f"🔒 Public key ECC: {self.eApiConfig.publicKey.hex()}")
            
            if isUseSSL:
                IuLog.doInfo(__name__, f"🔏 SSL Pinning: {not IuText.StringEmpty(sslPkPinning)}")
            
                
            print(f"\n\x1b[32mReady 🚀 \x1b[0m")
                     
            #IuLog.doVerbose(__name__,f"config:\n{config}")

            server = uvicorn.Server(config)
            await server.serve()

        except Exception as exception:
            IuLog.doException(__name__, exception)
# ---------------------------------------------------------------------------------------------------------------------------------------- 
