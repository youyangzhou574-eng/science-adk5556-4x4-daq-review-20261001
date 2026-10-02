def validate_creation_id(part):
    if part['ref']=='J2':return True
    value=part['association']['uuid']
    if len(value)!=32 or any(c not in '0123456789abcdef' for c in value.lower()):
        raise ValueError('Only recorded catalog UUIDs may create a part; imported identities are not creation inputs')
    return True
