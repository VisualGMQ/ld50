import gvar


def Log(msg):
    if gvar.DebugMode:
        print(msg)
