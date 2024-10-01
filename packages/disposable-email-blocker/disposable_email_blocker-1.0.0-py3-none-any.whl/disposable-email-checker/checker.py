from blocked_email_domains import DISPOSABLE_EMAIL_DOMAINS

def is_disposable_email(email: str) -> bool:
    domain = email.split('@')[1]
    return domain in DISPOSABLE_EMAIL_DOMAINS
