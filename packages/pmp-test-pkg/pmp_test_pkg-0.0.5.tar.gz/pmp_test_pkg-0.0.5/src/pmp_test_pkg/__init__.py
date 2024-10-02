import pmplicense as pmp
valid = pmp.check_license('pmp-test-pkg')
if (not valid):
    raise Exception("License check failed")

def hello_world():
    return "[pmp-test-pkg] Hello, world!"
