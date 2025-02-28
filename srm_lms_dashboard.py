from Network import *

class LMS():
    # Objecs
    LMS = Networks() # networks

    # Subject Codes
    ANDROIED_APPLICATION_DEVELOPMENT =10255
    CAREER_ADVANCEMENT =10259
    DATA_ANALYSING_USING_R =10258
    OPTIMIZATION_TECHNIQUES =10254
    CUMPUTER_NETWORKS =10253
    PYTHON_PROGRAMING =10252

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.LMS.set_accesstoken(self.username,self.password)

    def Activity(self,Subject=None):
      r1 = self.LMS.GET(f"{self.LMS.DOM_brightspace}/{Subject}",
            {
            'deepEmbedEntities': "1",
            'embedDepth': "1",
            'filterOnDatesAndDepth': "1"
            })
      if r1.status_code != 200 : return f"requst faild with status code: {str(r1.status_code)}: {str(r1.text)}"

      Weekly_Activities = r1.json()

      return self.View_Activity(self.LMS,Weekly_Activities)

    class View_Activity():
        def __init__(self,LMS,Activities):
          self.LMS = LMS
          self.ACTIVITIES = Activities

        def CompleteAllWeeks(self):
          for weeks in self.ACTIVITIES["entities"] if "entities" in self.ACTIVITIES else AssertionError(f'improper sequance: {self.ACTIVITIES}'):
            print(f'\n{Color.MAGENTA}Assesment: {weeks["properties"]["title"] if "title" in weeks["properties"] else "Not for you"}{Color.RESET}')
            if self.isCompleted(weeks,False):

              for i,week in enumerate(weeks["entities"] if "entities" in weeks else None):
                skiped_list = ["Assessment & Assignment",None]

                if ((week["properties"]["title"] if "title" in week["properties"] else None) not in skiped_list) and self.isCompleted(week):

                  for assesments in week["entities"] if "entities" in week else None:
                    print(f'  ->isCompleted: {SRM_Activities.LMS.POST(self.get_view_activity_url(assesments),None).status_code==200}') if self.get_view_activity_url(assesments) != None else None

        def isCompleted(self,activity,title=True) ->bool:
          if "entities" not in activity: return False
          completed = activity["entities"][-1:][0]["properties"]["completed"] if "completed" in activity["entities"][-1:][0]["properties"] else 0
          total = activity["entities"][-1:][0]["properties"]["total"] if "total" in activity["entities"][-1:][0]["properties"] else 0

          title = ((activity["properties"]["title"]+":") if "title" in activity["properties"] else activity["properties"]) if title != False else Color.YELLOW
          print(f'{title} {Color.RED}{completed}/{total} remining is: {total-completed}{Color.RESET}')
          return  0 != int(total-completed)

        def get_view_activity_url(self,json_data):
            if "actions" in json_data:
                for action in json_data["actions"]:
                    if action.get("name") == "view-activity":
                        return action.get("href")  # Return the first match
            if "entities" in json_data:  # Recursively check entities
                for entity in json_data["entities"]:
                    url = self.get_view_activity_url(entity)
                    if url:
                        return url
            return None

