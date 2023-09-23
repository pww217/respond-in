import os, logging, json, time
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


def get_unread(inbox):
    """
    Filters out already-read or sponsored messages.
    Returns a list of unread messages.
    """
    unread = []
    for message in inbox:
        is_read = message["read"]
        if is_read == False:
            try:
                _ = message["sponsoredConversationMetadata"]
            except:
                unread.append(message)
    return unread


def get_recruiter_message(message):
    urn = message["entityUrn"].split(":")[-1]
    event = message["events"][0]
    content = event["eventContent"]["com.linkedin.voyager.messaging.event.MessageEvent"]
    is_recruiter = filter_for_recruiters(content)
    
    if is_recruiter:
        map = {"urn": urn, "content": content}
        return map
    else:
        map = {"urn": urn, "content": None}
        return map


def filter_for_recruiters(content):
    is_recruiter = False
    try:
        if (
            content["customContent"][
                "com.linkedin.voyager.messaging.event.message.InmailContent"
            ]["inmailProductType"]
            == "RECRUITER"
        ):
            is_recruiter = True
    except KeyError:
        pass
    return is_recruiter


def parse_message(message): 
    subject = message.get("subject")
    text = message["attributedBody"]["text"].strip("\n")
    print(f"Subject: {subject}\n\n{text}\n-----------------------------------")


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

    unread = get_unread(inbox)

    with open("unread.txt", "w") as f:
        f.write(json.dumps(unread, indent=2))

    recruiter_messages = []
    for item in unread:
        message = get_recruiter_message(item)
        if message == None:
            pass
        else:
            recruiter_messages.append(message)
    # print(json.dumps(recruiter_messages, indent=2))
    
    with open("recruiter-messages.txt", "w") as f:
        f.write(json.dumps(recruiter_messages, indent=2))

    pprint(f"Messages needing response: {len(unread)}")

if __name__ == "__main__":
    main()
