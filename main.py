import os, logging, json
from linkedin_api import Linkedin

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s:")
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)

api_logger = logging.getLogger('linkedin_api')
api_logger.setLevel(logging.DEBUG)

def main():

  user = os.getenv('LKDIN_USER')
  pw = os.getenv('LKDIN_PW')

  # Authenticate using any Linkedin account credentials
  api = Linkedin(user, pw)

  convos = json.dumps(api.get_conversations(), indent=2)
  with open('convos.txt', 'w') as f:
    f.write(convos)

  one_convo = json.dumps(api.get_conversation(conversation_urn_id="2-M2QwZTU2OTUtYWE0OS00ODFkLWExMDktY2YxMDU1MDU1OTEyXzAxMg=="), indent=2)
  with open('one_convo.txt', 'w') as f:
    f.write(one_convo)

  profile = json.dumps(api.get_profile(public_id="irina-chernous-905483268", urn_id=None), indent=2)
  with open('profile.txt', 'w') as f:
    f.write(profile)

  chat = json.dumps(api.get_conversation_details("ACoAAEGQ0VUB1QS0cJ-Xt-Us4VA8U7vuWjJ11Vc"), indent=2)
  with open('chat.txt', 'w') as f:
    f.write(chat)

if __name__ == '__main__':
  main()


  """
  ...
    "metadata": {
    "unreadCount": 0
  }

  "elements": [
    {
      "read": true,
      "totalEventCount": 4
    }
  """