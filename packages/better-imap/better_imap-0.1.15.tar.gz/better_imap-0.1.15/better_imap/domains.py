from enum import StrEnum
from typing import Tuple, Optional
import json
from pathlib import Path

with open(Path(__file__).parent / "known_domains.json") as f:
    KNOWN_DOMAINS = json.load(f)


class EmailEncoding(StrEnum):
    UTF8 = "UTF-8"
    US_ASCII = "US-ASCII"


class EmailDomain(StrEnum):
    RAMBLER = "rambler"
    OUTLOOK = "outlook"
    FIRSTMAIL = "firstmail"
    MAILRU = "mailru"
    GMAIL = "gmail"
    ICLOUD = "icloud"
    CUSTOM = "custom"

    def imap_server_info(self) -> Optional[Tuple[str, EmailEncoding]]:
        """
        Retrieve the IMAP server information for the given email domain.

        Returns:
            A tuple containing the IMAP server address and the required encoding.
            Returns None if the domain does not have predefined IMAP server info.
        """
        imap_info_mapping = {
            EmailDomain.RAMBLER: ("imap.rambler.ru", EmailEncoding.UTF8),
            EmailDomain.OUTLOOK: ("outlook.office365.com", EmailEncoding.UTF8),
            EmailDomain.FIRSTMAIL: ("imap.firstmail.ltd", EmailEncoding.US_ASCII),
            EmailDomain.MAILRU: ("imap.mail.ru", EmailEncoding.UTF8),
            EmailDomain.GMAIL: ("imap.gmail.com", EmailEncoding.UTF8),
            # CUSTOM does not have predefined IMAP info
        }
        return imap_info_mapping.get(self, (None, EmailEncoding.UTF8))


def determine_email_domain(email: str) -> EmailDomain:
    """
    Determine the email domain from the provided email address.

    Args:
        email (str): The email address to evaluate.

    Returns:
        EmailDomain: The corresponding EmailDomain enum member.
    """
    try:
        str_domain = email.split("@")[1].lower()
    except IndexError:
        raise ValueError("Invalid email address format.")

    domain = (
        EmailDomain(KNOWN_DOMAINS[str_domain])
        if str_domain in KNOWN_DOMAINS
        else EmailDomain.CUSTOM
    )

    return domain
