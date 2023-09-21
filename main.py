import os, logging, json
from linkedin_api import Linkedin
from pprint import pprint

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s:")
sh = logging.StreamHandler()
sh.setFormatter(formatter)
logger.addHandler(sh)

api_logger = logging.getLogger("linkedin_api")
api_logger.setLevel(logging.DEBUG)

"""
is_sponsored = content["com.linkedin.voyager.messaging.event.message.SponsoredMessageContent"]
message = content["attributedBody"]["text"]
"""


def get_needs_response(inbox):
    """
    Sorts out already-read, sponsored, or other non-recruiter messages.
    Returns a list of unread messages from recruiters only
    """
    needs_response = []
    for message in inbox:
        is_read = message["read"]
        if is_read == False:
            try:
                for e in message["events"]:
                    content = e["eventContent"]["com.linkedin.voyager.messaging.event.MessageEvent"]
                    try:
                        if (
                            content["customContent"][
                                "com.linkedin.voyager.messaging.event.message.InmailContent"
                            ]["inmailProductType"]
                            == "RECRUITER"
                        ):
                            is_recruiter = True
                            needs_response.append(content)
                    except KeyError:
                        is_recruiter = False
            except KeyError:
                continue
    return needs_response

def parse_message(message):
    custom_content = message["customContent"]
    subject = message["subject"]
    text = message["attributedBody"]["text"].strip("\n")
    print(f"Subject: {subject}\nText:\n{text}\n")

def main():
    # user = os.getenv('LKDIN_USER')
    # pw = os.getenv('LKDIN_PW')

    # # Ideally would improve on the env var method
    # api = Linkedin(user, pw)

    # inbox = api.get_conversations()
    # with open('inbox.txt', 'w') as f:
    #  f.write(json.dumps(inbox, indent=2))

    with open("inbox.txt", "r") as f:
        inbox = json.loads(f.read())["elements"]

    needs_response = get_needs_response(inbox)
    pprint(f"Messages needing response: {len(needs_response)}")

    with open("needs_response.txt", "w") as f:
        f.write(json.dumps(needs_response, indent=2))

    for message in needs_response:
        parse_message(message)
       


if __name__ == "__main__":
    main()
