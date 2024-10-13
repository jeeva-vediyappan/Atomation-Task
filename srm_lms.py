import requests

class SRM_LMS():

    Subjects = {
        "Software"  :10249,
        "Java"      :10244,
        "IT"        :10250,
        "Database"  :10246,
        "OS"        :10245,
        "CA"        :10251
        }
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
        'Accept-Encoding': "gzip, deflate, br, zstd",
        'Content-Type': "application/x-www-form-urlencoded",
        'sec-ch-ua-platform': "\"Windows\"",
        'sec-ch-ua': "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
        'sec-ch-ua-mobile': "?0",
        'sec-fetch-site': "same-site",
        'sec-fetch-mode': "cors",
        'sec-fetch-dest': "empty",
        'accept-language': "en-US,en;q=0.9",
        'priority': "u=1, i",
        }

    def __init__(self):
        self.response = requests.Session()
        self.access_token_v()

    def sequences(self,subject_name):
        url = f"https://b4e4a216-b523-4789-b874-01376c642e90.sequences.api.brightspace.com/{subject_name}"
        params = {
            'deepEmbedEntities': "1",
            'embedDepth': "1",
            'filterOnDatesAndDepth': "1"
            }
        return(self.__request(url,params))

    def activity(self,subject_name,activity_id):
        url = f"https://b4e4a216-b523-4789-b874-01376c642e90.sequences.api.brightspace.com/{subject_name}/activity/{activity_id}"
        params = {
            'deepEmbedEntities': "1",
            'embedDepth': "1",
            'filterOnDatesAndDepth': "1"
            }
        return(self.__request(url,params))

    def access_token_v(self):
        url = "https://learn.srmonline.in/d2l/lp/auth/oauth2/token"

        payload = "scope=%2A%3A%2A%3A%2A"
        headers = self.headers.copy()
        headers['x-csrf-token']= "UNDER DEVELOPING"
        cookies = {
          "d2lSessionVal":"UNDER DEVELOPING",
          "d2lSecureSessionVal":'UNDER DEVELOPING'
        }
        r =self.response.request("POST",url, data=payload, headers=headers,cookies=cookies)
        try:
          self.access_token = r.json()['access_token']
        except: print(r.text)


    def task_view(self,subject_name,activity_code):
        url =f"https://b4e4a216-b523-4789-b874-01376c642e90.sequences.api.brightspace.com/{subject_name}/activity/{activity_code}/view"
        params = {
            'hasStateChanged': 0,
            'hasBeenViewed': 0,
            'filterOnDatesAndDepth': "1",
            'previousCompletion':"Incomplete"
            }
        return(self.__request(url,params,"POST"))

    def task(self,subject_name):

        SUB_CONT = self.sequences(subject_name)

        def looping(SUB_CONTENT):
          if "sequence"  in SUB_CONTENT['class'] or "sequenced-activity" in SUB_CONTENT['class']:
            for _A in SUB_CONTENT["entities"]:
                if task_verif(SUB_CONTENT):   pass
                elif task_view_activity(_A):  looping(_A)
                else: print("Finished : ",SUB_CONTENT['properties']['title'])


        def task_view_activity(src):
            if "activity"  in src['class']:
                for link in src['actions']:
                    if "view-activity" in link["name"]:
                      self.__request(link["href"],method="POST")
                      return False
                    else: return False
            else: return True


        def task_verif(src):
            try:
              if 'completion' in src["entities"][-1]['class']:
                  if  src["entities"][-1]['properties']['completed'] == src["entities"][-1]['properties']['total']: return True
                  else: return False
              else: return False
            except: raise Exception(src)


        looping(SUB_CONT)

    def __request(self,url,params=None,method="GET"):

        headers = self.headers.copy()
        headers['authorization']= f'Bearer {self.access_token}'

        try:
          r = self.response.request(method,url, params=params, headers=headers)

          if 'The access token is expired' in r.json().values():
              self.access_token_v()
              return self.__request(url,params,method)
          else:
             return r.json()

        except Exception as e: print(e,r.text)




lms = SRM_LMS()

for subject in lms.Subjects.values():
     lms.task(subject)
