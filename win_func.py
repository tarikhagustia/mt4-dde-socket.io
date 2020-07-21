from ctypes import c_int, c_double, c_char_p, c_void_p, c_ulong, c_char, pointer, cast
from ctypes import windll, byref, create_string_buffer, Structure, sizeof
from ctypes import POINTER, WINFUNCTYPE
from ctypes.wintypes import BOOL, HWND, MSG, DWORD, BYTE, INT, LPCWSTR, UINT, ULONG, LPCSTR

def get_winfunc(libname, funcname, restype=None, argtypes=(), _libcache={}):
    """Retrieve a function from a library/DLL, and set the data types."""
    if libname not in _libcache:
        _libcache[libname] = windll.LoadLibrary(libname)
    func = getattr(_libcache[libname], funcname)
    func.argtypes = argtypes
    func.restype = restype
    return func 

def WinMSGLoop():
    """Run the main windows message loop."""
    LPMSG = POINTER(MSG)
    LRESULT = c_ulong
    GetMessage = get_winfunc("user32", "GetMessageW", BOOL, (LPMSG, HWND, UINT, UINT))
    TranslateMessage = get_winfunc("user32", "TranslateMessage", BOOL, (LPMSG,))
    # restype = LRESULT
    DispatchMessage = get_winfunc("user32", "DispatchMessageW", LRESULT, (LPMSG,))
 
    msg = MSG()
    lpmsg = byref(msg)
    while GetMessage(lpmsg, HWND(), 0, 0) > 0:
        TranslateMessage(lpmsg)
        DispatchMessage(lpmsg)
 