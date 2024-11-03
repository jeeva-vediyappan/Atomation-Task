from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import requests
import time , json , re 

class SRM_LMS():

    Subjects = {
        "Software"  :10249,
        "Java"      :10244,
        "IT"        :10250,
        "DB"        :10246,
        "OS"        :10245,
        "CA"        :10251
        }
    headers = {
        'User-Agent'        : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
        'Accept-Encoding'   : "gzip, deflate, br, zstd",
        'Content-Type'      : "application/x-www-form-urlencoded",
        'sec-ch-ua-platform': "\"Windows\"",
        'sec-ch-ua'         : "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        'sec-ch-ua-mobile'  : "?0",
        'sec-fetch-site'    : "same-site",
        'sec-fetch-mode'    : "cors",
        'sec-fetch-dest'    : "empty",
        'accept-language'   : "en-US,en;q=0.9",
        'priority'          : "u=1, i",
        }

    domain ={
        'srmonline'             :"https://learn.srmonline.in",
        'brightspace_sequences' :"https://b4e4a216-b523-4789-b874-01376c642e90.sequences.api.brightspace.com"
    } 

    requests_body=  {
            "d2l_controlMapPrev": {
                "ID": {
                    "btn_action": "z_a",
                    "cms": "z_b",
                    "hid_haspass": "z_c",
                    "hid_disablerightclick": "z_d",
                    "ctl_3": "z_e",
                    "lbl_time": "z_f",
                    "ctl_5": "z_g",
                    "lbl_user": "z_h",
                    "ctl_7": "z_i",
                    "lbl_timelimit": "z_j",
                    "ctl_9": "z_k",
                    "lbl_attempts": "z_l",
                    "lbl_instructions1": "z_m",
                    "lbl_instructions2": "z_n",
                    "lbl_negative_marking_instructions": "z_o",
                    "hid_lockdownbrowserurl": "z_p",
                    "hid_lockdownbrowserlaunchtimeout": "z_q",
                    "ctl_messagearea": "z_r"
                },
                "SID": {}
            },
            "d2l_controlMap": [
                        {
                            "btn_action": [ ["z_a", "Button", ["DoAction();;return false;"], {}, 0, 0] ],
                            "cms": [
                                    [
                                        [
                                        [], "submission", 1, 1, 0, [0, 0, 0, "Submissions", "", []], "return false;"
                                        ],
                                        [[], "report", 1, 1, 0, [0, 0, 0, "Reports", "", []], "return false;"]
                                    ],
                                    "","qi_code(2)","HandleItemClick",0,"start"
                                    ],
                            "hid_haspass": ["z_c", "Hidden", [1], {}, 0, 1],
                            "hid_disablerightclick": ["z_d", "Hidden", [1], {}, 0, 1],
                            "ctl_3": ["z_e", "Field", [], None, 1, 1],
                            "lbl_time": ["z_f", "Label", [], {}, 0, 1],
                            "ctl_5": ["z_g", "Field", [], None, 1, 1],
                            "lbl_user": ["z_h", "Label", [], {}, 0, 1],
                            "ctl_7": ["z_i", "Field", [], None, 1, 1],
                            "lbl_timelimit": ["z_j", "Label", [], {}, 0, 1],
                            "ctl_9": ["z_k", "Field", [], None, 1, 1],
                            "lbl_attempts": ["z_l", "Label", [], {}, 0, 1],
                            "lbl_instructions1": ["z_m", "Label", [], {}, 0, 1],
                            "lbl_instructions2": ["z_n", "Label", [], {}, 0, 1],
                            "lbl_negative_marking_instructions": ["z_o", "Label", [], {}, 0, 1],
                            "hid_lockdownbrowserurl": ["z_p", "Hidden", [1], {}, 0, 1],
                            "hid_lockdownbrowserlaunchtimeout": ["z_q", "Hidden", [1], {}, 0, 1],
                            "ctl_messagearea": ["z_r", "MessageArea", ["d_content_inner", "d_page_header", 0, [], None], {}, 0, 0]
                        },
                        {}]
        }

    def __init__(self,userName,password):
        self.response = requests.Session()
        self.access_token = None
        self.x_csrf_token = None
        self.userName     = userName
        self.passward     = password
        
        self.login()

    def login(self):
        url =f"{self.domain['srmonline']}/d2l/lp/auth/login/login.d2l"
        payload = {
            'd2l_referrer': '',
            'target': '/d2l/home',
            'loginPath': '/d2l/login',
            'userName': f'{self.userName}@srmist.edu.in',
            'password':  self.passward
        }
        r=self.__request(url,"POST",payload).text

        if "'XSRF.Token','" in r:
            try:
              X = r.find("'XSRF.Token','")
              self.x_csrf_token = r[X+14:X+32+14]
              self.access_token_v()
            except: raise AssertionError(r)
        else:       raise AssertionError(r)

    def access_token_v(self):
        url = f"{self.domain['srmonline']}/d2l/lp/auth/oauth2/token"

        payload = "scope=%2A%3A%2A%3A%2A"

        if self.x_csrf_token != None:
          r =self.__request(url,"POST",payload)
          try:
            self.access_token = r['access_token']
          except:   raise AssertionError(r)
        else:       raise AssertionError("Empty x-csrf-token")


    def Subject_seq(self,subject_name):
        url = f"{self.domain['brightspace_sequences']}/{subject_name}"
        params = {
            'deepEmbedEntities': "1",
            'embedDepth': "1",
            'filterOnDatesAndDepth': "1"
            }
        return(self.__request(url,"GET",params))


    def mcq_qutions(self,SUB):

        def looping(S):
            if "activity" in S["class"]:
                if "MCQ's" in S["properties"]["title"]: 
                    print(S["properties"]["title"])
                    for x in S["links"]:
                        if "class" in x: 
                            if "embed" in x["class"]: qustion_register(x["href"],S["properties"]["title"]) if "quiz_summary.d2l" in x["href"] else None
            else: 
                if "entities" in S:
                    for q in S["entities"]: looping(q)

        def qustion_reg(url,qi):
            d2l_controlMap =self.requests_body["d2l_controlMap"]
            d2l_controlMap[0]["cms"][2] = qi
            data = {
                    "d2l_action": "Custom",
                    "d2l_actionparam": "1",
                    "d2l_hitCode": GenerateHitCode(url),
                    "d2l_rf": "",
                    "d2l_controlMapPrev": str(self.requests_body["d2l_controlMapPrev"]),
                    "hps": "",
                    "drc": "0",
                    "LockDownBrowserUrl": "0",
                    "LockDownBrowserLaunchTimeout": "5000",
                    "d2l_controlMap": str(d2l_controlMap),
                    "d2l_state": str([{
                                "3": ["grid", "pagesize", "htmleditor", "hpg"],
                                "1": ["gridpagenum", "search", "pagenum"],
                                "2": ["lcs"]},[]
                                    ]),
                    "d2l_referrer": self.x_csrf_token,
                    "d2l_multiedit": str({"Controls": []}),
                    "d2l_stateScopes": str({
                                "1": ["gridpagenum", "search", "pagenum"],
                                "2": ["lcs"],
                                "3": ["grid", "pagesize", "htmleditor", "hpg"]
                                        }),
                    "d2l_stateGroups": "",
                    "d2l_statePageId": "271"
                    }
            data_ = {
                    "d2l_action": "Custom",
                    "d2l_actionparam": "1",
                    "d2l_hitCode": GenerateHitCode(url),
                    "d2l_rf": "",
                    "d2l_controlMapPrev": "{\"ID\":{\"btn_action\":\"z_a\",\"cms\":\"z_b\",\"hid_haspass\":\"z_c\",\"hid_disablerightclick\":\"z_d\",\"ctl_3\":\"z_e\",\"lbl_time\":\"z_f\",\"ctl_5\":\"z_g\",\"lbl_user\":\"z_h\",\"ctl_7\":\"z_i\",\"lbl_timelimit\":\"z_j\",\"ctl_9\":\"z_k\",\"lbl_attempts\":\"z_l\",\"lbl_instructions1\":\"z_m\",\"lbl_instructions2\":\"z_n\",\"lbl_negative_marking_instructions\":\"z_o\",\"hid_lockdownbrowserurl\":\"z_p\",\"hid_lockdownbrowserlaunchtimeout\":\"z_q\",\"ctl_messagearea\":\"z_r\"},\"SID\":{}}",
                    "hps": "",
                    "drc": "0",
                    "LockDownBrowserUrl": "0",
                    "LockDownBrowserLaunchTimeout": "5000",
                    "d2l_controlMap": "[{\"btn_action\":[\"z_a\",\"Button\",[\"DoAction();;return false;\"],{},0,0],\"cms\":[\"z_b\",\"ContextMenuStructure\",[[[[],\"submission\",1,1,0,[0,0,0,\"Submissions\",\"\",[]],\"return false;\"],[[],\"report\",1,1,0,[0,0,0,\"Reports\",\"\",[]],\"return false;\"]],\"\",\""+qi+"\",\"HandleItemClick\",0,\"start\"],{},0,1],\"hid_haspass\":[\"z_c\",\"Hidden\",[1],{},0,1],\"hid_disablerightclick\":[\"z_d\",\"Hidden\",[1],{},0,1],\"ctl_3\":[\"z_e\",\"Field\",[],null,1,1],\"lbl_time\":[\"z_f\",\"Label\",[],{},0,1],\"ctl_5\":[\"z_g\",\"Field\",[],null,1,1],\"lbl_user\":[\"z_h\",\"Label\",[],{},0,1],\"ctl_7\":[\"z_i\",\"Field\",[],null,1,1],\"lbl_timelimit\":[\"z_j\",\"Label\",[],{},0,1],\"ctl_9\":[\"z_k\",\"Field\",[],null,1,1],\"lbl_attempts\":[\"z_l\",\"Label\",[],{},0,1],\"lbl_instructions1\":[\"z_m\",\"Label\",[],{},0,1],\"lbl_instructions2\":[\"z_n\",\"Label\",[],{},0,1],\"lbl_negative_marking_instructions\":[\"z_o\",\"Label\",[],{},0,1],\"hid_lockdownbrowserurl\":[\"z_p\",\"Hidden\",[1],{},0,1],\"hid_lockdownbrowserlaunchtimeout\":[\"z_q\",\"Hidden\",[1],{},0,1],\"ctl_messagearea\":[\"z_r\",\"MessageArea\",[\"d_content_inner\",\"d_page_header\",0,[],null],{},0,0]},{}]",
                    "d2l_state": "[{\"3\":[\"grid\",\"pagesize\",\"htmleditor\",\"hpg\"],\"1\":[\"gridpagenum\",\"search\",\"pagenum\"],\"2\":[\"lcs\"]},[]]",
                    "d2l_referrer": self.x_csrf_token,
                    "d2l_multiedit": "{\"Controls\":[]}",
                    "d2l_stateScopes": "{\"1\":[\"gridpagenum\",\"search\",\"pagenum\"],\"2\":[\"lcs\"],\"3\":[\"grid\",\"pagesize\",\"htmleditor\",\"hpg\"]}",
                    "d2l_stateGroups": "",
                    "d2l_statePageId": "271"
                    }

            if self.__request(url,"POST",data_).status_code == 200: return True
            else: False
            
        def qustion_register(url,sub):
            qi  =parse_qs(urlparse(url).query).get('qi',[None])[0]
            ou  =parse_qs(urlparse(url).query).get('ou',[None])[0]
            if qustion_reg(url,qi):
                ai = ai_v(ou,qi)
                if  ai != None: quiz_attempt_page_auto(ou,qi,ai,sub)

        def ai_v(ou,qi):  
            url =f"https://learn.srmonline.in/d2l/lms/quizzing/user/attempt/quiz_start_process_auto.d2l?ou={ou}&isprv=&qi={qi}&dnb=1&cfql=1&fromQB=0&inProgress=1&cft=&d2l_body_type=1"
    
            reqs = self.__request(url,"GET")
            X=reqs.text.find('parent.GoToAttemptQuizAuto( ')
            try: return int(reqs.text[X+28:X+28+7])
            except : return None


        def quiz_attempt_page_auto(ou,qi,ai,sub):
            url_ = "https://learn.srmonline.in/d2l/lms/quizzing/user/attempt/quiz_attempt_page_auto.d2l"

            params = {
                    'ou': ou,
                    'isprv': "",
                    'impcf': "",
                    'pg': "1",
                    'qi': qi,
                    'ai': ai,
                    'dnb': "1",
                    'cfql': "1",
                    'fromQB': "0",
                    'showIncorrectOnly': "0",
                    'cft': "",
                    'd2l_body_type': "1"
                    }

            quiz(self.__request(url_,"GET",params),sub)
        
        def quiz(page,sub):
            soup = BeautifulSoup(page.text,'html.parser')
            y=0 
            question = ""
            options  = []
            answer   = ""
            quiz_f   = []

            for x in soup.findAll('d2l-html-block'):
                y+=1
                if y == 6:  y = 1
                if y == 1:
                    print("Qustion"+" : ",x.get('html'))
                    question = x.get('html')
                else:
                    print("option "+" : ",x.get('html'))
                    options.append(x.get('html'))
                if y==5:
                    quiz_f.append({
                        "question"  :   question,        
                        "options"   :   options,
                        "answer"    :   answer
                        })
                    
                    options=[]
            
            try:
                with open("quize.json", 'r') as json_file:
                    data = json.load(json_file)
            except: data = dict()

            with open("quize.json", 'w') as json_file:
                 data[sub] = quiz_f
                 json.dump(data, json_file, indent=4)


        def Hitcode_seed(r):
            W = r.text.find('D2L.LP.Web.Authentication.Xsrf.Init')
            return re.findall(r'-?\d+',r.text[W+99:])[0]
    
        def GenerateHitCode(url): 
            r =self.__request(url,"GET") 
            hitCodeCount = 0
            hitCodeCount = hitCodeCount + 1
            m_hitCode = str(Hitcode_seed(r)) + str((int(time.time() * 1000) + 100000000) % 100000000) + str(hitCodeCount % 10)
            return m_hitCode   

        looping(self.Subject_seq(SUB))


    def view_task_activity(self,subject_name):

        SUB_CONT = self.Subject_seq(subject_name)
        print("\n"+"SUBJECT NAME : ",SUB_CONT["properties"]["title"]+"\n")

        def looping(src):

            if 'completion' in src["entities"][-1]['class']:
                Total = src["entities"][-1]['properties']['total']
                Completed = src["entities"][-1]['properties']['completed']
                print(f"Remining {Total-Completed}"+"  :  "+src["properties"]["title"])
                if Total-Completed ==0: return None

            if  "Assessment & Assignment" in src["properties"]["title"] or "Discussion Forum" in src["properties"]["title"]: return None

            if "class" in src:
                if "activity"  in src['class']:
                    for link in src['actions']:
                        if "view-activity" in link["name"]:
                            self.__request(link["href"],method="POST")
                            print("             -->Complited")
            else:
                for q in src["entities"]: looping(q)
                            
            

        looping(SUB_CONT)

    def __request(self,url,method,params=None):

        headers = self.headers.copy()
        if self.access_token != None: headers['authorization']= f'Bearer {self.access_token}'
        if self.x_csrf_token != None: headers['x-csrf-token']= self.x_csrf_token

        r = self.response.request(
            method,url,
            data=params if params!=None else None,
            headers=headers
            )

        try:
            if 'The access token is expired' in r.json().values():
                self.access_token_v()
                return self.__request(url,params,method)
            else: return r.json()
        except:   return r




lms = SRM_LMS("jv6108","chemistry@3D")
for x in lms.Subjects.values():
    lms.view_task_activity(x)

