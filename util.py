import re, os

def ensure_dirs(dirpath):
    # dirpath should be a string representing a path to a directory;
    # it should NOT include a filename as part of the path
    components = re.split(r'/', dirpath)
    if len(components) == 0:
        return
    partialpath = components[0]
    if partialpath == "":
        return
    if not os.path.exists(partialpath):
        os.mkdir(partialpath)
    for component in components[1:]:
        partialpath = os.path.join(partialpath, component)
        if not os.path.exists(partialpath):
            os.mkdir(partialpath)
