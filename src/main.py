import logging



from src.config.loader import get_settings
from src.auth import get_gmail_service
from datetime import datetime,timedelta
from src.config.senders import SENDERS


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def read_latest_email():
    service=get_gmail_service()

    # get the todays date range
    today=datetime.now()
    start=today.strftime("%Y/%m/%d")
    end=(today+timedelta(days=1)).strftime("%Y/%m/%d")

    # Gmail query for todays emails:
    query=f"after:{start} before:{end}"
    results=service.users().messages().list(
        userId="me",
        q=query,
        maxResults=50
    ).execute()

    messages=results.get("messages",[])
    if not messages:
        logging.info("No message Found")
        return

    for msg in messages:

        full_msg=service.users().messages().get(userId="me",id=msg["id"]).execute()
        headers=full_msg['payload']['headers']
        sender=next((h["value"] for h in headers if h['name'].lower()=='from'),"unknown sender")
        subject=next((h["value"] for h in headers if h['name'].lower()=='subject'),"No subject")
        date=next((h["value"] for h in headers if h['name'].lower()=='date'),"No Date")

        if any(s in sender for s in SENDERS):
            logging.info(f"\nlatest message is \n sender :{sender}\n subject:  {subject} \n date :{date}")



def main():
    settings = get_settings()
    logging.info(f"System initialized with APP_NAME={settings.app_name}")
    logging.basicConfig(level=logging.INFO)
    read_latest_email()

if __name__ == "__main__":
    main()
