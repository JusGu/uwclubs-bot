import secrets

def create_shortname(fullname: str):
    lowercase_fullname = fullname.lower()
    cleaned_fullname = ''.join(e if e.isalnum() or e.isspace() else ' ' for e in lowercase_fullname)
    filtered_words = [x for x in cleaned_fullname.split() if x not in ["uw", "uwaterloo", "waterloo", "wlu"]]
    shortname = "-".join(filtered_words)
    return shortname

def create_secret():
    return secrets.token_urlsafe(16)
