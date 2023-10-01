import json
from linkedin_api import Linkedin


def get_unread(inbox):
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


def get_sender_info(message):
    participants = message["participants"][0]
    profile = participants["com.linkedin.voyager.messaging.MessagingMember"][
        "miniProfile"
    ]
    fname = profile["firstName"]
    lname = profile["lastName"]
    occupation = profile["occupation"]
    #     print(
    #         f"Name; {fname} {lname}\n\
    # Title: {occupation}\n"
    #     )
    return fname, lname, occupation


def get_recruiter_message(message):
    """
    Parses out key information such as Urns and actual message content
    If a recruiter, returns a map of the message content and conversation urn.
    """
    urn = message["entityUrn"].split(":")[-1]
    event = message["events"][0]
    fname, lname, occupation = get_sender_info(message)
    content = event["eventContent"]["com.linkedin.voyager.messaging.event.MessageEvent"]
    is_recruiter = filter_for_recruiters(content)

    if is_recruiter:
        map = {
            "urn": urn,
            "fname": fname,
            "lname": lname,
            "occupation": occupation,
            "content": content,
        }
        return map
    else:
        return None


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


def respond_and_mark_read(api, template, message):
    urn = message["urn"]
    # content = message["content"]
    fname = message["fname"]
    lname = message["lname"]
    personalized = template.format(fname=fname)
    # print(f"{personalized}\n---------\n")
    api.send_message(personalized, conversation_urn_id=urn)
    api.mark_conversation_as_seen(urn)
    print(f"Finished transaction for message from {fname} {lname}")


# def parse_message(message):
#     subject = message.get("subject")
#     text = message["attributedBody"]["text"].strip("\n")
#     print(f"Subject: {subject}\n\n{text}\n-----------------------------------")


def main():
    with open("creds.json") as f:
        creds = json.loads(f.read())
    user = creds["LKDIN_USER"]
    pw = creds["LKDIN_PW"]
    api = Linkedin(user, pw)

    with open("template.txt") as f:
        template = f.read()

    inbox = api.get_conversations()["elements"]
    with open("inbox.txt", "w") as f:
        f.write(json.dumps(inbox, indent=2))

    unread = get_unread(inbox)

    recruiter_messages = []
    for item in unread:
        message = get_recruiter_message(item)
        if message == None:
            pass
        else:
            recruiter_messages.append(message)

    print(f"Messages needing response: {len(recruiter_messages)}\n")

    for item in recruiter_messages:
        respond_and_mark_read(api, template, item)


if __name__ == "__main__":
    main()
