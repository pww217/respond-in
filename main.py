import os, logging, json
from linkedin_api import Linkedin

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s:")
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)

def main():

  user = os.getenv('LKDIN_USER')
  pw = os.getenv('LKDIN_PW')

  # Authenticate using any Linkedin account credentials
  api = Linkedin(user, pw)



  # GET a profile
  details = json.dumps(api.get_conversation_details("urn:li:member:1100009813"), indent=2)
  with open('details.txt', 'w') as f:
    f.write(details)

"""   messages = json.dumps(api.get_conversations(), indent=2)
  with open('messages.txt', 'w') as f:
    f.write(messages)
  
  threads = json.dumps(api.get_conversation("urn:li:fsd_conversation:2-M2QwZTU2OTUtYWE0OS00ODFkLWExMDktY2YxMDU1MDU1OTEyXzAxMg=="), indent=2)
  with open('threads.txt', 'w') as f:
    f.write(threads) """

if __name__ == '__main__':
  main()