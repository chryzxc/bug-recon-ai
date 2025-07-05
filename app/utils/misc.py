def without_https(raw):
    return raw.replace("https://","") if raw.startswith("https://") else raw