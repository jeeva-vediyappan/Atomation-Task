import requests, json

class Networks:
    # Domain
    DOM_srmonline = "https://learn.srmonline.in"
    DOM_brightspace = "https://b4e4a216-b523-4789-b874-01376c642e90.sequences.api.brightspace.com"
    # Path
    PATH_login = "/d2l/lp/auth/login/login.d2l"
    PATH_Oathen = "/d2l/lp/auth/oauth2/token"

    # Declard Variables
    x_csrf_token = None
    access_token = None

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
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

        })

    def isAccesstokenValid(self,userName,passward)->bool:
        pass

    def set_accesstoken(self,userName,passward)->bool:

        r1 = self.session.request(
            "POST",
            self.DOM_srmonline + self.PATH_login,
            data={
              'd2l_referrer': '',
              'target': '/d2l/home',
              'loginPath': '/d2l/login',
              'userName': f'{userName}@srmist.edu.in',
              'password':  passward})

        if "'XSRF.Token','" in r1.text:
            try:
              X = r1.text.find("'XSRF.Token','")
              self.x_csrf_token = r1.text[X+14:X+32+14]
              self.session.headers.update({'x-csrf-token': self.x_csrf_token})
            except: raise AssertionError(f"XSRF.Token failed to extract: {r1.text}")
        else: raise AssertionError(f"XSRF.Token not found in HTML Page: {r1.text}")

        if self.x_csrf_token != None:
          r2 =self.session.request(
              "POST",
              self.DOM_srmonline+self.PATH_Oathen,
              data="scope=%2A%3A%2A%3A%2A")
          try:
              self.access_token = r2.json().get('access_token')
              self.session.headers.update({'authorization': f'Bearer {self.access_token}'})
              if self.access_token is None:
                raise AssertionError(f"Access token not found in JSON: {r2.text}")
          except json.JSONDecodeError as e:
            raise AssertionError(f"JSONDecodeError: {e}, Response Text: {r2.text}")
        else: raise AssertionError("Empty x-csrf-token")


    def GET(self,url,parameter=None):
        return self.session.request("GET",url,data=parameter if parameter != None else None)

    def POST(self,url,parameter):
        return self.session.request("POST",url,data=parameter if parameter != None else None)

    def PUT(self):
        pass

    def DELETE(self):
        pass

class Color:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"