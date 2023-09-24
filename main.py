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
                # Dump any sponsored conversations
                _ = message["sponsoredConversationMetadata"]
            except:
                # Append non-sponsored and unread messages
                unread.append(message)
    return unread

def get_sender_name(message):
    pass

def get_recruiter_message(message):
    """
    Parses out key information such as Urns and actual message content
    If a recruiter, returns a map of the message content and conversation urn.
    """
    urn = message["entityUrn"].split(":")[-1]
    event = message["events"][0]
    content = event["eventContent"]["com.linkedin.voyager.messaging.event.MessageEvent"]
    is_recruiter = filter_for_recruiters(content)

    if is_recruiter:
        map = {"urn": urn, "content": content, "fname": fname, "lname": lname}
        return map
    else:
        return None


def filter_for_recruiters(content):
    """
    Searches for a recruiter InMail message tag to filter out recruiters
    """
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


def respond_and_mark_read(api, template, message):
    """
    The bread and butter, will actually reply to the message and mark it read.
    """
    urn = message["urn"]
    content = message["content"]
    api.send_message(template, conversation_urn_id=urn)
    api.mark_conversation_as_seen(urn)
    logger.info(f"Finished transaction for {urn}")


def parse_message(message):
    """
    Pulls out a subject and text of a message
    Returns None for subject if none is present.
    """
    subject = message.get("subject")
    text = message["attributedBody"]["text"].strip("\n")
    print(f"Subject: {subject}\n\n{text}\n-----------------------------------")


def main():
    user = os.getenv("LKDIN_USER")
    pw = os.getenv("LKDIN_PW")

    # Ideally would improve on the env var method
    api = Linkedin(user, pw)

    inbox = api.get_conversations()["elements"]
    with open("inbox.txt", "w") as f:
        f.write(json.dumps(inbox, indent=2))

    # with open("inbox.txt", "r") as f:
    #     inbox = json.loads(f.read())["elements"]

    unread = get_unread(inbox)

    # with open("unread.txt", "w") as f:
    #     f.write(json.dumps(unread, indent=2))

    recruiter_messages = []
    for item in unread:
        message = get_recruiter_message(item)
        if message == None:
            pass
        else:
            recruiter_messages.append(message)

    pprint(f"Messages needing response: {len(recruiter_messages)}")

    with open("recruiter-messages.txt", "w") as f:
        f.write(json.dumps(recruiter_messages, indent=2))

    with open("template.txt") as f:
        template = f.read()
    for item in recruiter_messages:
        respond_and_mark_read(api, template, item)


if __name__ == "__main__":
    main()
