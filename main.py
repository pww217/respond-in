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


def get_convo_urns(convos):
    all_urns = []
    for c in convos:
        urn = c["entityUrn"].split(":")[-1]
        all_urns.append(urn)
    return all_urns


def check_recruiter_status(convos):
    events = convos["elements"]["events"]
    rstatus = events[0]["eventContent"][
        "com.linkedin.voyager.messaging.event.MessageEvent"
    ]["customContent"]["com.linkedin.voyager.messaging.event.message.InmailContent"][
        "recruiterInmail"
    ]
    return rstatus


def check_unreads(inbox):
    unreads = []
    for message in inbox["elements"]:
        is_read = message["read"]
        if is_read == False:
            unreads.append(message)
    with open("unreads.txt", "w") as f:
        f.write(json.dumps(unreads, indent=2))
    return unreads


def main():
    # user = os.getenv('LKDIN_USER')
    # pw = os.getenv('LKDIN_PW')

    # # Ideally would improve on the env var method
    # api = Linkedin(user, pw)

    # inbox = api.get_conversations()
    # with open('inbox.txt', 'w') as f:
    #  f.write(json.dumps(inbox, indent=2))

    with open("inbox.txt", "r") as f:
        inbox = json.loads(f.read())

    unreads = check_unreads(inbox)
    pprint(f"Unread messages: {len(unreads)}")

    # convos = api.get_conversations()
    # with open('convos.txt', 'w') as f:
    #   f.write(json.dumps(convos, indent=2))


if __name__ == "__main__":
    main()
