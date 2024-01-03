def create_shortname(fullname: str):
    fullname = fullname.lower().replace(" ", "-")
    for word in ["club", "uw", "uwaterloo", "waterloo"]:
        fullname = fullname.replace(word, "")
    return fullname