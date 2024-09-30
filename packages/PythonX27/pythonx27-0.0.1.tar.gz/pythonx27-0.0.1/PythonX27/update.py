try: 
    import pip 
except (ImportError, ModuleNotFoundError): 
    import PythonX27.installpip 
    PythonX27.installpip.main()
    import pip 

def autoUpdate() -> None:
    pip.main(['install', 'PythonX'])