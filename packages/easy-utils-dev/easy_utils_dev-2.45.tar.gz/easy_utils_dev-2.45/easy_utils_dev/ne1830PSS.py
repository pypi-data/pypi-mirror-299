
# This script is used to collect data from Nokia 1830PSS WDM
# update on 15-12-2022 : 10:53

import traceback
import paramiko , csv ,sys
from time import sleep
from datetime import datetime
from easy_utils_dev.debugger import DEBUGGER
from easy_utils_dev.encryptor import initCryptor
from easy_utils_dev.utils import pingAddress
from easy_utils_dev import exceptions


class PSS1830 :
    def __init__(self , sim=False , debug_name='Auto1830PSS' , auto_enable_tcp_forward=False,file_name=None,debug_home_path=None ) -> None:
        self.port = 22
        self.logger = DEBUGGER(debug_name,file_name=file_name, homePath=debug_home_path)
        self.connected = False
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.channel = None
        self.nodeName = None
        self.prompt = None
        self.encryptor = initCryptor(True)
        self.TIMEOUT = 120
        self.isjumpserver = False
        self.jumpserver = {}
        self.sim = sim
        self.jumpServerInSameInstance  = False
        self.requireAknow=None
        self.gmre = False
        self.isGmreLogin=False
        self.gmrePrompt=None
        self.lastPrompt=None
        self.allBuffer=''
        self.pssRelease = None
        self.auto_enable_tcp_forward=auto_enable_tcp_forward
        self.tcpForwardStatus=None
        self.resetRequired = False
        self.screenBuffer = ""
        if self.auto_enable_tcp_forward :
            self.logger.info(f'***WARNING*** : Auto enable tcp forwarding is enabled. This will allow tcp fowarding in target machine then restarting sshd service agent.')
        


    def set_debug_level( self , level ) :
        self.logger.set_level(level)

    def nfmtJumpServer(self, ip , usr , pw  ) :
        self.logger.info(f"""ssh to WSNOC VM nested/jumpserver ssh  [ IP => {ip} ]..""")
        try :
            self.jumpServerInSameInstance = True
            self.jumpserver  = paramiko.SSHClient()
            self.jumpserver.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.logger.info(f'connecting to VM jumpserver with {usr}@{ip} port=[{self.port}] ..')
            self.jumpserver.connect(ip  , self.port , usr , pw )
            self.isjumpserver = True
            self.nfmtip = ip 
            self.nfmtsshuser = usr
            self.nfmtsshpw = pw
            self.logger.debug(f"""check if tcpfowarding is allowed or not .. """)
            isEnabled , result  = self.checkIfTcpForwardingEnabled()
            self.logger.debug(f"""check if tcpfowarding is allowed or not. Result : {result}""")
            if not isEnabled :
                self.logger.debug(f"""check if tcpfowarding is allowed or not. result is disallowed. fixing .. """)
                self.fixTcpSSH()
                self.jumpserver.close()
                self.logger.debug(f"""re-establish the connection [ JUMPSERVER ] after modifying the sshd file and restarting the sshd service ..""")
                self.jumpserver  = paramiko.SSHClient()
                self.jumpserver.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.jumpserver.connect(ip  , self.port , usr , pw , banner_timeout=200 , timeout=200, auth_timeout=200)
            self.logger.info(f"""Connecting to WSNOC/NFMT as [JUMPSERVER] [{ip}][CONNECTED]""")
            self.connected = True
            self.jumpserver.nfmtip = ip
            return self.jumpserver
        except Exception as error:
            self.logger.debug(f"""Connecting to WSNOC/NFMT as [JUMPSERVER] [{ip}][FAILED] debug={traceback.format_exc()}""") 
            self.logger.error(f"""Connecting to WSNOC/NFMT as [JUMPSERVER] [{ip}] [FAILED] [more details in debug] [force exit with status code -1] error={error}""") 
            raise exceptions.JumpServerConnectionFailure(f"connection failure address : {ip}")

    def getTcpForwardStatus(self) :
        status , result = self.checkIfTcpForwardingEnabled()
        self.tcpForwardStatus= status
        return self.tcpForwardStatus

    def fixTcpSSH(self) :
        self.tcpForwardStatus = 'disabled'
        if not self.auto_enable_tcp_forward :
            return
        self.logger.info(f"""Enabling TCP forwarding on target machine ..""")
        status , result = self.checkIfTcpForwardingEnabled()
        self.logger.debug(f"""Current AllowTcpForwarding result = {result}""") 
        cli1 = f"sed -i 's/#AllowTcpForwarding yes/AllowTcpForwarding yes/g' /etc/ssh/sshd_config"
        cli2 = "sed -i 's/#AllowTcpForwarding no/AllowTcpForwarding yes/g' /etc/ssh/sshd_config"
        cli3 = "sed -i 's/AllowTcpForwarding no/AllowTcpForwarding yes/g' /etc/ssh/sshd_config "
        self.logger.debug(f'executing {cli1}')
        self.logger.debug(f'executing {cli2}')
        self.logger.debug(f'executing {cli3}')
        self.jumpserver.exec_command(f"{cli1} ; {cli2} ; {cli3} ; service sshd restart")
        self.logger.debug('executing fixtcpforward commands are done. service ssh restart also done.')
        self.logger.debug('checking again the status of tcp forward status after executing fix commands.')
        status , result = self.checkIfTcpForwardingEnabled()
        self.logger.debug(f"""Tcp Forward Fix process completed. AllowTcpForwarding result  = {result}""") 

    def rollbackTcp(self) :
        self.logger.info(f"""fixing tcp disable tcpforwarding .. """)
        stdin, stdout, stderr = self.jumpserver.exec_command("cat /etc/ssh/sshd_config | grep -i AllowTcpForwarding")
        result = stdout.read()
        self.logger.debug(f"""Current AllowTcpForwarding result = {result}""") 
        cli1 = f"sed -i 's/AllowTcpForwarding yes/#AllowTcpForwarding no/g' /etc/ssh/sshd_config"
        cli2 = "sed -i 's/#AllowTcpForwarding no/AllowTcpForwarding yes/g' /etc/ssh/sshd_config"
        cli3 = "sed -i 's/AllowTcpForwarding yes/AllowTcpForwarding no/g' /etc/ssh/sshd_config "
        self.logger.debug(f'executing {cli1}')
        self.logger.debug(f'executing {cli2}')
        self.logger.debug(f'executing {cli3}')
        self.jumpserver.exec_command(f"{cli1} ; {cli2} ; {cli3} ; service sshd restart")
        self.logger.debug('executing rollback fixtcpforward commands are done. service ssh restart also done.')
        self.logger.debug('checking again the status of tcp forward status after executing rollback commands.')
        status , result = self.checkIfTcpForwardingEnabled()
        self.logger.debug(f"""Tcp Forward rollback process completed. AllowTcpForwarding result  = {result}""") 

    def checkIfTcpForwardingEnabled(self) :
        """check if port forwarding is enabled in linux machine
        returns True : if it is enabled. as boolean
        returns False : if it is not enabled. as boolean
        returns None : if it cannot be determined. as None
        returns the result as string 
        """
        cli = f'''sshd -T | grep -i  allowtcpforwarding'''
        self.logger.debug(f'executing {cli} to check the tcp forwarding if enabled or not ...')
        ssh = self.jumpserver
        result = self.ssh_execute( ssh , cli )
        self.logger.debug(f'result in checkIfTcpForwardingEnabled is {result}')
        if 'no' in result.lower() :
            self.logger.debug(f'allowtcpforwarding is no, returning False ')
            return False, result
        elif 'yes' in result.lower() :
            self.logger.debug(f'allowtcpforwarding is yes, returning True ')
            return True , result
        else :
            self.logger.error(f'allowtcpforwarding is not returning yes or no. maybe configuration is not correct.')
            return None , result


    def enter_login_prompt(self) :
        self.logger.debug("enter_login_prompt Started ..")
        for i in range(10) :
            sleep(.5)
            new_data = self.channel.recv(2048).decode('utf-8')
            self.logger.debug(f"Enter Login Prompt is waiting the UserName input buffer: {new_data}")
            if ("Username:") in str(new_data) : 
                self.logger.debug(f"tool will enter {self.cliUser} to username field.")
                self.channel.sendall(self.cliUser + '\n')
                break

        for i in range(10) :
            sleep(.5)
            if self.resetRequired and self.tmpPassword:
                cliPw = self.tmpPassword
            else:
                cliPw = self.cliPw
            new_data = self.channel.recv(2048).decode('utf-8')
            self.logger.debug(f"Enter Login Prompt is waiting the Password input: {new_data}")
            if ("password:") in str(new_data).lower() : 
                self.channel.sendall(cliPw + '\n')
                break
            if ("authentication failed") in str(new_data).lower() : 
                raise Exception("Authentication [cli] Failed")

        if self.resetRequired:
            buffer = self.newUserPwdReset()
            sleep(1)
            
        if self.requireAknow :
            for i in range(10) :
                sleep(1)
                self.logger.debug(f"Waiting Result for the required Acknowledgement Try: {i}")
                if self.resetRequired :
                    new_data = buffer
                else :
                    new_data = self.channel.recv(2048).decode('utf-8')
                if "authentication failed" in new_data :
                    raise Exception("Authentication [cli] Failed")
                        
                self.logger.debug(f"Enter Login Prompt is waiting the acknowledgement: {new_data}")
                if ("acknowledge") in str(new_data).lower() : 
                    self.channel.sendall('yes' + '\n')
                    break
        return True

    def determine_prompt(self) :
        for i in range(30) :
            sleep(.5)
            if self.resetRequired :
                new_data = self.allBuffer
            else :
                new_data = self.channel.recv(4096).decode('utf-8')
            if "#" in new_data :
                new_data = new_data.split('\n')
                self.prompt = new_data[-1]
                self.logger.debug('prompt detected => '+self.prompt)
                self.nodeName = self.prompt.replace('#' , '')
                self.disable_paging(skip_buffer_clear=True)
                return True


    def ssh_execute(self , ssh ,command ,  merge_output=False , hide_output=False) :
        self.logger.info(f"executing {command}")
        try :
            stdin_ , stdout_ , stderr_ = ssh.exec_command(command)
            r = stdout_.read().decode()
            e = stderr_.read().decode()
            if r.endswith('\n') :
                r = r[ : -1]
            if hide_output : 
                self.logger.debug(f""" 
                =========================
                +command = '{command}'
                -stdout = {r}
                -stderr = {e}
                =========================
                """)
            else :
                self.logger.debug(f""" 
                =========================
                +command = '{command}'
                -stdout = {r}
                -stderr = {e}
                =========================
                """)
            if merge_output :
                return str(r) + str(e)
            return r 
        except Exception as error :
            self.logger.error(str(error))
            self.logger.debug(traceback.format_exc())
            return str(error)
 
    def deleteUser(self , affectedUsername) :
        self.logger.info(f'Deleting username {affectedUsername}')
        userProfile = self.getUser(affectedUsername)
        self.logger.info(f'user brief is {userProfile}')
        if not userProfile.get('username') :
            self.logger.info(f"Warnning : {affectedUsername} DID NOT found in NE Users list. Skip Deletion")
            return ''
        group = userProfile['group']
        if group != 'administrator' :
            self.logger.error(f"User {affectedUsername} is not admin user. it is {group}")
            raise Exception("Insufficient permissions. Check logs.")
        cli = f'config admin user delete {affectedUsername}'
        result = self.cli_execute(cli)
        self.logger.debug(f'user deleted with buffer resutn {result}')
        return result

    def changePassword(self,username,newPassword) :
        # self.logger.set_level('debug')
        self.logger.info(f'Changing password ...')
        userProfile = self.getUser(username)
        self.logger.info(f'user brief are {userProfile}')
        group = userProfile['group']
        if group != 'administrator' :
            self.logger.error(f"User {username} is not admin user. it is {group}")
            raise Exception("Insufficient permissions. Check logs.")
        cli = f'config admin users edit {username} passwd force'
        self.cli_execute(cli , expect='password')
        sleep(.5)
        if self.cliUser != username :
            self.cli_execute("Nokia@20981" , expect='password' , ifPassword=True )
            sleep(.5)
            self.cli_execute("Nokia@20981" , expect='password' , ifPassword=True )
            pss = PSS1830(self.sim)
            if self.logger.currentDebugLevel == 'debug' :
                pss.set_debug_level('debug')
            pss.connect(self.mode , neip=self.neip , user=username , pw=newPassword , rootpw=self.rootPw , jumpserver=self.jumpserver , resetRequired=True,tmpPassword="Nokia@20981")
            pss.disconnect()
        else :
            self.cli_execute(self.cliPw , expect='password' , ifPassword=True )
            sleep(.5)
            self.cli_execute(newPassword , expect='password' , ifPassword=True )
            sleep(.5)
            result = self.cli_execute(newPassword , expect='password' , ifPassword=True )
            return result  

    def newUserPwdReset(self):
        self.logger.debug(f'Changing Password for the Newely Created User')
        for i in range(30) :
            self.logger.debug(f"Try {i}/30 to change the password on login ..")
            sleep(1)
            new_data = self.channel.recv(4096).decode('utf-8')
            self.logger.debug(f"buffer in newUserPwdReset : {new_data}")
            if "Change Password Now" in new_data :
                new_data = new_data.split('\n')
                self.logger.debug(f'Prompt for Password Change is: {new_data}')
                self.logger.debug(f"Tool will enter new password for try 1 ")
                self.cli_execute(self.cliPw, ifPassword=True,wait=False)
                sleep(1)
                self.logger.debug(f"Tool will enter new password for try 2")
                self.cli_execute(self.cliPw, ifPassword=True,wait=False)
                sleep(1)
                break
        d= self.buffer()
        self.logger.debug(f'changing password should be done, buffer is {d}')
        if 'Error:' in d:
            self.logger.error(f"Password Change Failed due to Error: {d}")
            raise Exception("Password Change Failed due to Error.")
        return d

    def loginToGmre(self) :
        self.logger.debug(f"login to gmre started ...")
        self.cli_execute('tools gmre_cli' , wait=True , error="telnet: gmremgmt: Name or service not known" , errorMessage=f"No GMRE Activated on {self.neip}" , expect='username')
        sleep(.5)
        self.logger.debug('tool will enter gmre username ..')
        pw = self.encryptor.dec_base64('Z21yZQ==')
        self.cli_execute( pw , wait=True , expect='password')
        self.logger.debug('tool will enter gmre password ..')
        self.cli_execute( pw , wait=False)
        sleep(1.5)
        response = self.buffer().splitlines()
        self.logger.debug(f'gmre first login response is {response}')
        response = [ line for line in response if line != '']
        self.gmrePrompt = response[-1]
        self.lastPrompt = self.prompt
        self.prompt = self.gmrePrompt
        self.logger.debug(f'gmrePrompt={self.gmrePrompt}')
        self.gmre=True
        self.isGmreLogin= True
        self.logger.debug(f"login to gmre completed.")

    def getGmreInformation(self) :
        self.logger.info(f'getting gmre node details')
        result = self.cli_execute('show node').splitlines()
        data= {}
        for line in result :
            if ': ' in line :
                key = line.split(': ')[0].replace(' ' , '')
                value = line.replace(key , '').replace(': ' , '').replace('\n' , '').lstrip()
                data[key] = value
        return data

    def checkPinngableFromParamiko(self,neip,ssh) :
        pingCommand = f'''ping {neip} -c 3 | grep -i '100%' '''
        self.logger.debug(f'checking node reachability using {pingCommand}')
        stdin, stdout, stderr = ssh.exec_command(pingCommand)
        result = stdout.read().decode("utf-8").replace("\n", "")
        self.logger.debug(f'checking node reachability using {pingCommand} result={result}')
        if '100%' in result :
            self.logger.debug(f"Network Element {neip} is not reachable. PingResult={result}")
            return False
        else :
            self.logger.debug(f"Network Element {neip} is reachable. PingResult={result}")
            return True

    def activateGmreRelease(self , release ) :
        self.logger.info(f'Warning:- activateGmreRelease {release}')
        cli = f"config node activenetworkversion {release}"
        self.logger.debug(f'activating gmre release using {cli}')
        result = self.cli_execute(cli)
        self.logger.debug(f'activating gmre release using {cli}')

    def connect(self , mode='cli' , neip=None , port=22  , user = 'admin', pw ='YWRtaW4=' , rootpw='QUx1MTIj',  jumpserver = None , resetRequired = False, tmpPassword = None) :
        if mode not in ['cli' , 'ssh' , 'direct_cli'] :
            raise exceptions.NotValid1830PssConnectionMode(f'mode {mode} is not a valid input')
        if pw == 'YWRtaW4=' :
            self.logger.debug(f"pw specified is obfuscated. Switch to plain text ...")
            pw = self.encryptor.dec_base64(pw)
            self.logger.debug(f"pw specified is obfuscated. Switch to plain text result {pw}")
        if rootpw == 'QUx1MTIj' :
            self.logger.debug(f"rootpw specified is obfuscated. Switch to plain text ...")
            rootpw = self.encryptor.dec_base64(rootpw)
            self.logger.debug(f"pw specified is obfuscated. Switch to plain text result {rootpw}")
        self.logger.info(f'Opening SSH  connection to NE {neip} mode={mode}, resetRequired={resetRequired}')
        self.cliUser = user
        self.mode = mode
        self.cliPw = pw
        self.neip= neip
        self.rootPw = rootpw
        self.resetRequired = resetRequired
        self.tmpPassword = tmpPassword
        if self.sim == True :
            port = 22 
        elif self.sim == False :
            port = 5122
        # another method is to inject the jumpserver inside the connect itself.
        if jumpserver != None  and self.jumpServerInSameInstance == False :
            self.isjumpserver = True
            self.jumpserver = jumpserver
            self.nfmtip = jumpserver.nfmtip 
        if  self.isjumpserver == False :
            if not pingAddress(neip) :
                self.logger.error(f"Network Element {neip} is not reachable. PingResult=False")
                raise exceptions.NetworkElementNotReachable(f'Network Element Address : {neip}')
            else :
                self.logger.debug(f"Network Element {neip} not reachable. PingResult=True")

            try :
                if mode == 'direct_cli' :
                    self.client.connect(neip , port , "cli" , None , banner_timeout=200 )
                elif mode == 'cli' or mode == 'ssh' :
                    self.client.connect(neip , port , "root" , rootpw , banner_timeout=200  )
            except Exception as error :
                self.logger.error(f'Error connecting to {self.neip} as mode={mode} while jumpserver is disabled. Error={error}')
                self.logger.debug(traceback.format_exc() , source=self.neip)
                self.connected=False
                raise exceptions.NetworkElementConnectionFailure(self.neip)
            
        elif self.isjumpserver :
            if not self.checkPinngableFromParamiko(neip , self.jumpserver) :
                raise exceptions.NetworkElementNotReachable(f'Network Element Address : {neip}')

            jump_transport = self.jumpserver.get_transport()
            src_addr = (self.nfmtip, 22 )
            dest_addr = (neip , port )
            jump_channel = jump_transport.open_channel("direct-tcpip", dest_addr, src_addr , timeout=200)
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try :
                if mode == 'direct_cli' :
                    self.client.connect(neip , port , "cli" , None  , sock=jump_channel , banner_timeout=200)
                elif mode == 'cli' or mode == 'ssh' :
                    self.client.connect(neip , port , "root" , rootpw , sock=jump_channel , banner_timeout=200)
            except Exception as error :
                self.logger.error(f'Error connecting to {self.neip} as mode={mode} while jumpserver is enabled. Error={error}')
                self.logger.debug(traceback.format_exc() , source=self.neip)
                self.connected=False
                raise exceptions.NetworkElementConnectionFailure(self.neip)
            
            self.connected = True
        if mode == 'ssh' : 
            self.connected = True
            return self.client
        # getting the ne version.
        result = self.get_neversion()
        if '-' in result :
            self.logger.debug(f'partitioning release response as - in result .. ')
            self.pssRelease = float(result.partition('-')[2].partition('-')[0])
            self.logger.debug(f'paritioned release response as float is {self.pssRelease}')
            self.logger.info(f"Detected release is {self.pssRelease}")
            isRequired = self.isRequireAknowledge(self.pssRelease)
            if isRequired :
                self.logger.debug(f'switching to require aknow mode as release is less than 23.6')
                self.requireAknow = True
            elif not isRequired :
                self.logger.debug(f'switching to NOT require aknow mode as release is not less than 23.6')
                self.requireAknow = False
            else :
                self.logger.debug(f'isRequired is not defined. ERROR')
        else :
            self.logger.error(f'PSS release is undefined due to detection pattern is not found. no "-" char found in pss release result. result {result}')
            raise Exception('undefined PSS Release return output. check logs ')         
        self.channel = self.client.invoke_shell()
        self.logger.debug(f'set timeout in srv channel to {self.TIMEOUT}')
        self.channel.settimeout(self.TIMEOUT)
        if mode == 'cli' :
            self.logger.debug(f'mode cli detected. "su - cli" command will be executed to enter NE cli.')
            cmd = 'su - cli\n'
            self.channel.sendall(cmd)
            sleep(.1)
            self.logger.debug(f'switching user to cli mode completed.')
        self.logger.debug(f'Starting/Processing login window handler to enter username, password and aknowledge message if appears ...')
        self.enter_login_prompt()
        self.logger.debug(f'Starting/Processing to auto detect the NE prompt NE_NAME+# ...')
        self.determine_prompt()
        self.connected = True
        self.logger.debug(f'Processing handler to enter username, password completed. returning self.client object ')
        return self.client
    
    def isRequireAknowledge(self , newRelease) : 
        if '-' in str(newRelease) :
            newRelease = float(newRelease.split('-')[0])
        if int(newRelease) in range( 0 , 15 ) :
            return True
        elif int(newRelease) >= 23 :
            return False
        else : 
            return True

    def getTime(self) :
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
        return dt_string

    

    def get_neversion(self) :
        self.logger.debug(f'Getting NE version.. ')
        cli = "cat /pureNeApp/EC/swVerInfoAscii"
        self.logger.debug(f'executing from get_neversion:: {cli}')
        result = self.ssh_execute( self.client , cli ).replace('\n' , '')
        self.logger.debug(f'received release response in get_neversion {result}')
        self.logger.debug(f'received release response in get_neversion length = {len(result)}')
        if len(result) < 5 :
            self.logger.error(f'PSS release response is not valid or too short.')
            raise Exception('PSS Release is not valid')
        return result

    def disconnect(self) :
        try :
            if self.connected :
                self.close_cliconnection()
                self.client.close()
            else :
                self.logger.debug(f'No need to disconnect from SSH IP={self.neip}. Connection was not up anyway.')
            self.logger.debug('closing logger instance ...')
            self.logger.close()
        except :
            pass


    def disable_paging(self,skip_buffer_clear=False) :
        cli = f'paging status disable'
        self.cli_execute(cli , wait=False)
        sleep(1)
        if skip_buffer_clear :
            self.logger.debug(f"skip_buffer_clear in disable_paging set to clear. clear now")
            self.buffer()
        self.logger.debug('paging disabled.')
        

    def channels_report(self, exportCsv=False) :
        self.logger.info('Generating Channels Report .. ')
        channels = self.get_xcs()
        header = ['NE', 'shelf', 'slot', 'port' , 'powerRx' , "powerTx" , "channel" , "prefec"  ,"postFec" , "shape" , "phase" , "trackMode"]
        csvFpath = f"channels_report_{self.host}_{self.getTime()}.csv"
        if exportCsv :        
            csvFile = open(csvFpath, 'w', encoding='UTF8' , newline='')
            csvFile = csv.writer(csvFile)
            csvFile.writerow(header)
        for channel in channels :
            otPort = None
            if not "LINE" in channel['aEnd'].upper() : otPort = channel['aEnd']
            if not "LINE" in channel['zEnd'].upper() : otPort = channel['zEnd']
            file = self.cli_execute(f"show interface {otPort} detail").splitlines()
            for line in file :
                breakIt = False 
                try :
                    nodeName = self.prompt.replace("#" , "")
                    if "Shelf:" in line :
                        details = line.split(": ")
                        shelf = details[1].replace(' Slot' , "")
                        slot = details[2].replace(' Port' , "")
                        port = details[3].split(' -')[0]
                    if "Received Power" in line :
                        powerRx = line.split(':')[1].split(" ")[1]
                    if "Transmitted Power" in line :
                        powerTx = line.split(':')[1].split(" ")[1]
                    if "Channel Tx   " in line :
                        channel = line.split(':')[1].split(" ")[1].replace('\n' , '')
                    if "pre" in line.lower() and 'fec' in line.lower() :
                        prefec = line.split(':')[1].split(" ")[1].replace('\n' , '')
                    if "post" in line.lower() and 'fec' in line.lower() :
                        postFec = line.split(':')[1].split(" ")[1].replace('\n' , '')
                    if "Txshape" in line :
                        shape = line.split(':')[1].split(" ")[1].replace('\n' , '')
                    if "Phase encoding Mode" in line :
                        phase = line.split(':')[1].split(" ")[1].replace('\n' , '')
                    if "TrackPolar" in line or "Track Polar" in line :
                        trackMode = line.split(':')[1].split(" ")[1].replace('\n' , '')
                        breakIt = True
                    if breakIt and  exportCsv :
                        output = f"{nodeName} => [ {shelf} / {slot} / {port}  ] {channel} => TX : {powerTx} ,  RX : {powerRx} prefec => {prefec}  "
                        data = [nodeName , shelf , slot , port , powerRx , powerTx , channel , prefec  ,postFec , shape , phase , trackMode]
                        csvFile.writerow(data)
                        self.logger.debug(output)
                except Exception as error:
                    self.logger.error(f'error [MAY SKIP/IGNORE] : {error}')
                    continue
        self.logger.info('Generating Channels Report Terminated. ')
            

    def cli_execute(self , command , wait=True ,ifPassword=False,expect=None,errorMessage=None,error=None) :
        '''
        cli_execute method is executing pss cli commands inside pss machines.
        command : example : show software upgrade status
        wait : default is True. if wait is False then cli_execute will not wait for command completion and will return immediately.
        ifPassword : hide the password logs.
        '''
        if self.gmre and not self.isGmreLogin :
            self.logger.error(f"GMRE not logged in. No command will be executed gmre={self.gmre} isGmreLogin={self.isGmreLogin}")
            return ''
        if not self.connected :
            self.logger.warning(f"No action is allowed to execute. Connection is not established.")
            return
        self.channel.sendall(command + '\r\n')
        if not ifPassword :
            self.logger.debug('executing :'+command)
        if wait :
            result = self.wait_result(command=command , expect=expect, expectError=error,errorMessage=errorMessage)
            return result
        
    def buffer(self) :
        try :
            data= self.channel.recv(4096).decode('utf-8')
            self.allBuffer += data
            return data
        except :
            return ''
    
    def config_database(self , ip , user, password , protocol , path , backupname="BACKUP") :
        self.cli_execute(f'config database server ip {ip}')
        self.cli_execute(f'config database server protocol {protocol}')
        self.cli_execute(f'config database path {path}{backupname}')
        self.cli_execute(f'config database server userid {user}' , wait=False)
        sleep(.5)
        self.cli_execute(password, ifPassword=True)
  
    def config_swserver(self , ip , user, password , protocol , path ) :
        self.cli_execute(f'config software server ip {ip}')
        self.cli_execute(f'config software server protocol {protocol}')
        self.cli_execute(f'config software server root {path}')
        self.cli_execute(f'config software server userid {user}' , wait=False)
        sleep(.5)
        self.cli_execute(password , ifPassword=True)
  
    def backToCliRoot(self) :
        '''
        backToCliRoot = backMainMenu, same functionality with different function name for more meaningful function name.
        '''
        self.cli_execute('mm')
    
    def backMainMenu( self ) :
        self.backToCliRoot()
        
    def wait_result(self , command,expect,expectError=None,errorMessage=None,autoError = True) :
        self.logger.debug(f"""WAIT RESULT : command = {command} | Begin """)
        data = ''
        start = False
        i = 0
        if not expect :
            expect = self.prompt
        while True:
            sleep(1)
            new_data = self.channel.recv(9999*1000).decode('utf-8')
            self.logger.debug(f"""WAIT RESULT : new_data = {new_data}""")
            if new_data :
                i = 0
                data += new_data   
                self.allBuffer += new_data   
                if expect in data or self.prompt in data:   
                    data2 = data.splitlines()   
                    return_data = ''
                    for line in data2 :
                        if expectError != None and str(expectError).lower() in line.lower(): 
                            self.logger.debug(f"expectError found in buffer. expectError={expectError} line={line}")
                            self.logger.debug(f"""wait_result failure details : 
                                command={command}
                                expect={expect}
                                errorMessage={errorMessage}
                                autoError={autoError}
                                line={line}
                            """)
                            if errorMessage :
                                raise Exception(errorMessage)
                            else :
                                raise Exception(f"command failed due to {expectError}")
                        if autoError and 'error' in line.lower() or 'Login incorrect!' in line.lower():
                            self.logger.debug(f"""wait_result failure details : 
                                        command={command}
                                        expect={expect}
                                        errorMessage={errorMessage}
                                        autoError={autoError}
                                        line={line}
                                        """)
                            raise Exception(f"Command Failed to Execute: {line}")
                        if command in line : 
                            start = True
                        elif not command in line and start == True  and not self.prompt in line and line != '':
                            return_data += line +'\n'
                        if line.startswith(self.prompt) and command not in line or expect in line:
                            self.logger.debug(f"""WAIT RESULT : return_data = {return_data} | END""")
                            self.logger.debug(f"""WAIT RESULT : command = {command} | END """)
                            return return_data
            else: 
                i += 1
                if i >= self.TIMEOUT*2 :
                    self.logger.error(f"""Timout in WAIT_RESULT : {command}""")

    
    def get_allcards(self) : 
        self.logger.info("Getting all cards inventory .. ")
        cards = self.cli_execute('show slot *')
        self.logger.debug(f"Getting all cards inventory .. return {cards} ")
        cards = cards.splitlines()
        cards_return = {"all" : {} , "equipped" : {} , "unequipped" : {} }
        for key , line in enumerate(cards) : 
            try :
                if "------------" in line : continue
                if 'Slot' in line or 'Present Type' in line  or'see slot' in line or "Oper" in line : continue
                _card_line = [x for x in line.split(' ') if x != '' ]
                if 'Empty' == _card_line[1] : continue
                self.logger.debug(f"get_allcards : line split .. return {_card_line} ")
                slotting = _card_line[0]
                cardType = _card_line[1]
                cards_return['all'][slotting] = {'card' : cardType , 'slot' : slotting , 'status' : _card_line[-1]}
                if "UEQ" in line :
                    cards_return['unequipped'][slotting] = {'card' : cardType , 'slot' : slotting ,  'status' : _card_line[-1] }
                else :
                    cards_return['equipped'][slotting] = {'card' : cardType , 'slot' : slotting ,  'status' : _card_line[-1] }
            except :
                continue
        self.logger.debug(f"get_allcards : final return {cards_return}")
        return cards_return  
            

    def get_xcs(self) :
        xcs = self.cli_execute('show xc *')
        xcs = xcs.splitlines()
        xcsList = []
        for _ , line in enumerate(xcs) : 
            if "------------" in line : continue
            if "A-End" in line or 'OCH Trail' in line or "Admin Oper" in line or "entries" in line or " "*20 in line : continue
            details = line.split('  ')
            details = [ i for i in details if i != "" ]
            if len(details) == 0 : 
                continue
            try :
                aEnd = details[0]
                zEnd = details[1]
                channel = details[2]
                connectionId = details[3]
                label = details[4]
                width = details[5]
                type = details[6]
                adminState = details[7]
                oper = details[8]
                dir = details[9]
            except :
                continue
            tmp = {'aEnd' : aEnd , 'zEnd' : zEnd , 'channel' : channel , "id" : connectionId ,
                   "label" : label , 'width' : width , "type" : type , "admin" : adminState , 
                   "operation" : oper , 'dir' : dir
                   }
            xcsList.append(tmp)
        return xcsList        
         
    def get_cards(self) :
        cards = self.cli_execute('show card inven *')
        raw_return = cards
        cards = cards.splitlines()
        cardsJson  = []
        for line in cards :
            try :
                if line == '' or "Location  Card" in line or "--"*10 in line : continue 
                card = line.split(' ')
                cardsList = [ i for i in card if i != "" ]
                shelfSlot = cardsList[0]
                shelf = shelfSlot.split('/')[0]
                slot = shelfSlot.split('/')[1]
                family = cardsList[1]
                cardType = cardsList[2]
                pn = cardsList[3]
                sn = cardsList[4]
                cardsJson.append({
                    "shelfSlot" : shelfSlot , 'shelf' : shelf , 'slot' : slot ,'family' : family , "cardType" : cardType , "pn" : pn  , 'sn'  : sn
                })
            except :
                continue
        return cardsJson , raw_return

    def get_userlabel(self) :
        return self.cli_execute('show general userlabel')
    
    def enable_openagent(self) :
        self.cli_execute('config general openagent enabled')

    def disable_openagent(self) :
        self.cli_execute('config general openagent disable')

    def openagent_status(self) :
        result = self.cli_execute('show general openagent').splitlines()
        self.logger.debug(f'openagent status response from cli_execute: {result}')
        for line in result :
            self.logger.debug(f'Checking openAgent line by line: line={line}')
            if ":" in line :
                status = line.split(':')[1]
                self.logger.debug(f'open agent detected status is {status}')
                if "enabled" in status.lower() :
                    status  = True
                    break
                elif 'disabled' in status.lower() :
                    status =  False
                    break
                else :
                    status =  'Unknown'
                    break
        self.logger.info(f'Open Agent Status = {status}')
        return status
        
    def get_odukxc(self) : 
        odukxs = self.cli_execute('show odukxc brief')
        odukxs = odukxs.splitlines()
        odukxsList = []
        for key , line in enumerate(odukxs) : 
            try :
                if "------------" in line : continue
                if "A-End" in line or 'XcRate' in line or 'State' in line: continue
                details = line.split('  ')
                details = [ i for i in details if i != "" ]
                if len(details) == 0 : continue
                aEnd = details[0]
                zEnd = details[1]
                id = details[2]
                rate = details[3]
                dir = details[4]
                prot = details[5]
                name = details[6]
                odukxsList.append({
                    'aEnd' : aEnd , "zEnd" : zEnd  , "id" : id , "rate" : rate , "dir" : dir , "protection" : prot , 
                    "name" : name
                })
            except :
                continue
        return odukxsList
        
    def get_version(self) :
        return self.pssRelease
        
    def close_cliconnection(self) :
        if self.gmre and self.isGmreLogin :
            self.cli_execute('quit' , wait=False)
            sleep(1)
        self.cli_execute('mm' , wait=False)
        sleep(1)
        self.cli_execute('logout' , wait=False)
        self.connected = False
    
    def get_mastershelf(self) :
        masterShelf = self.get_shelfs()[0]['type']    
        return masterShelf

    def clear_buffer(self) :
        try :
            for i in range(3) :
                if self.channel.recv_ready():
                    self.channel.recv(1024)
                    break
                sleep(1)
        except : 
            pass
        

    def get_nefirmware(self) :
        self.logger.info('Getting NE firmware .. ')        
        cli = f"show firmware ne"
        result = self.cli_execute(cli)
        data = []
        result = result.splitlines()
        for line in result :
            try :
                if 'sh/sl' in line or '----------' in line or line == ''  or "NE" in line : continue
                s = line.split(' ')
                s = [ x for x in s if x != '' ]
                # print(s)
                shelfslot = s[0]
                shelf = shelfslot.split('/')[0]
                slot = shelfslot.split('/')[1]
                card = s[1]
                try : 
                    profile= s[2]
                except IndexError :
                    profile= 'N/A'
                data.append({'shelf' : shelf , 'slot' : slot ,  'shelf/slot' : shelfslot , 'card' : card , 'profile' : profile  })
            except :
                continue
        self.logger.info('Getting NE firmware .. completed') 
        return data

    def get_ec_type(self) :
        self.logger.debug('retreiving EC type from all installed cards ...')
        cards = self.get_allcards().get('all')
        for key , value in cards.items() :
            self.logger.debug(f'Searching for EC in {key} detail=> {value}')
            if 'EC' in value.get('card' , '').upper() :
                self.logger.debug(f'''EC card detected in {key} card={value.get('card')}''')
                return value.get('card')
            


    def get_availableFW(self) :
        self.logger.info('Getting available firmware .. ')        
        cli = f"show firmware available"
        result = self.cli_execute(cli)
        self.logger.info(f'get_availableFW : command = {cli}')    
        self.logger.debug(f'{self.nodeName} - {cli} - {result}')
        result = result.splitlines()
        data = {}
        start = False
        current_fw = 'Not Found'
        for line in result :
            try :
                if 'All available firmware profiles' in line :
                    self.logger.debug(f'All Available firmware profiles line detected. splitting line to search for cards. and flag start to True.')
                    card = line.split('for')[1].replace(' ', '').replace('\n' , '')
                    start = True
                    profiles = []
                elif start == True :
                    if line != '' :
                        fw = line.replace(' ', '').replace('\n' , '').replace('*' , '')
                        profiles.append(fw)
                        data[card] = {'profiles' : profiles , 'currentfw' :  current_fw}
                    if "*" in line : 
                        current_fw = line.replace(' ', '').replace('\n' , '').replace('*' , '')
                        data[card] = {'profiles' : profiles , 'currentfw' :  current_fw}
            except : 
                pass
        self.logger.debug(f'Getting available firmware completed. {data}') 
        return data

    def getUsers(self) :
        result = self.cli_execute(f'show admin user *')
        sleep(1)
        # print(f"RESULT >>>> {result}")
        a = result.splitlines()
        users=[]
        for line in a :
            if '----' in line or "LinuxTools" in line : continue
            line = line.split(' ')
            line = [x for x in line if x != '']
            if len(line) >= 3 :
                try :
                    users.append({
                    'username' : line[0],
                    'group' : line[1],
                    'status' : line[2],
                    'linuxtools' : line[3],
                })
                except :
                    pass
        return users

    def getUser(self,username) :
        self.logger.debug(f"Looking for user {username}")
        users = self.getUsers()
        self.logger.debug(f"Full users array = {users}")
        for user in users :
            f = username == user['username']
            self.logger.debug(f"is username={username} equal ne_username={user.get('username')} ? {f}")
            if username == user['username'] :
                return user
        return {}


    def enable_cli_user(self , user, exception_on_failure=True ):
        """
        Enable PSS login user status from disabled to enabled.
        user : cli user : string
        exception_on_failure : bool, default True. Raise exception if user not found.

        return True if user is enabled
        return False if error raised during the process.
        """
        self.logger.debug(f"enable pss cli user {user}")
        cli = f'config admin users edit {user} status enabled'
        result = self.cli_execute(cli)
        if 'unknown username' in result or len(result) > 0 :
            if exception_on_failure :
                raise Exception(f'Username {user} is not found. PSS response is {result}')
            return False
        return True

    def updateUserPrivileges(self,affectedUsername,newRole) :
        self.logger.info(f"Updating user privileges with {newRole} for {affectedUsername}")
        possibleRoles = ['administrator' , 'observer' , 'provisioner' , 'crypto']
        if not newRole.lower() in possibleRoles :
            self.logger.error(f"Role  '{newRole}'@{affectedUsername} is not a valid role. Possible roles are: {possibleRoles}")
            return False
        cli = f'config admin users edit {affectedUsername} group {newRole}'
        self.cli_execute(cli)
        return True

    def disable_cli_user(self , user, exception_on_failure=True ):
        """
        Disable PSS login user status from enabled to disabled.
        user : cli user : string
        exception_on_failure : bool, default True. Raise exception if user not found.

        return True if user is disabled
        return False if error raised during the process.
        """
        self.logger.debug(f"enable pss cli user {user}")
        cli = f'config admin users edit {user} status disabled'
        result = self.cli_execute(cli)
        if 'unknown username' in result or len(result) > 0 :
            if exception_on_failure :
                raise Exception(f'Username {user} is not found. PSS response is {result}')
            return False
        return True

    def get_shelfs(self) :
        self.logger.debug('Getting shelfs .. ')
        shelfsList = []
        self.clear_buffer()
        cli = f"show shelf *"
        shelfs = self.cli_execute(cli).splitlines()
        for line in shelfs :
            if "Description" in line or "Present" in line or '---------' in line : 
                start=True
                continue
            if start :
                line= line.split(' ')
                line = [line for line in line if line != '']
                shelfId = line[0]
                shelfType = line[1]
                shelfsList.append({
                    'shelfId' : shelfId,
                    'type' : shelfType
                })
        return shelfsList


if __name__ == '__main__' : 
    pass

        
# pss = PSS1830(auto_enable_tcp_forward=True)
# pss.port = 322
# pss.set_debug_level('debug')
# jumpserver = pss.nfmtJumpServer('127.0.0.1' , 'root' , 'Nokia@2023')
# pss = PSS1830()
# pss.set_debug_level('debug')
# x= pss.connect('cli' , neip="10.10.40.167" , jumpserver=jumpserver )
# # x = pss.get_allcards()
# # x = pss.get_ec_type()
# s = pss.enable_cli_user('admin')
# print(s)

# s = pss.get_nefirmware()
# print(s)
# pss.get_mastershelf()
# pss.disable_openagent()
# pss.enable_openagent()
# pss.openagent_status()
# pss.get_version()
# pss.get_xcs()
# pss.channels_report()

# pss.cli_execute('show xc *')
# s = pss.close_cliconnection()
# s = pss.cli_execute('show otu *')
# print(s)
# pss.cli_execute('show shelf *' , False)
# pss.cli_execute('show version')
# pss.cli_execute('show soft up st')
# pss.cli_execute('show card inven * ')
# pss.config_database('10.10.10.1' , 'alcatel' , 'alu1233' , 'ftp' , '/' , 'BACKUP')
# pss.config_swserver('10.10.10.2' , 'alcatel' , 'alu1233' , 'ftp' , '/')
