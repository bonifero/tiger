"""Snapshot the content view of this Python process's Tk window, not the desktop."""
import ctypes as C
import ctypes.util

class Point(C.Structure):
    _fields_ = [('x', C.c_double), ('y', C.c_double)]
class Size(C.Structure):
    _fields_ = [('width', C.c_double), ('height', C.c_double)]
class Rect(C.Structure):
    _fields_ = [('origin', Point), ('size', Size)]

objc=C.CDLL(ctypes.util.find_library('objc'))
objc.objc_getClass.argtypes=[C.c_char_p]; objc.objc_getClass.restype=C.c_void_p
objc.sel_registerName.argtypes=[C.c_char_p]; objc.sel_registerName.restype=C.c_void_p
send_addr=C.cast(objc.objc_msgSend,C.c_void_p).value

def msg(obj,sel,result=C.c_void_p,args=(),values=()):
    fn=C.CFUNCTYPE(result,C.c_void_p,C.c_void_p,*args)(send_addr)
    return fn(obj,objc.sel_registerName(sel.encode()),*values)

def snapshot(path,title='Рюкзак · Практикум'):
    app=msg(objc.objc_getClass(b'NSApplication'),'sharedApplication')
    windows=msg(app,'windows')
    count=msg(windows,'count',C.c_ulong)
    window=None
    for i in range(count):
        candidate=msg(windows,'objectAtIndex:',args=(C.c_ulong,),values=(i,))
        txt=msg(msg(candidate,'title'),'UTF8String',C.c_char_p)
        if txt and txt.decode()==title:
            window=candidate;break
    if not window:raise RuntimeError('Tk native window not found')
    view=msg(window,'contentView')
    bounds=msg(view,'bounds',Rect)
    bitmap=msg(view,'bitmapImageRepForCachingDisplayInRect:',args=(Rect,),values=(bounds,))
    msg(view,'cacheDisplayInRect:toBitmapImageRep:',None,(Rect,C.c_void_p),(bounds,bitmap))
    props=msg(objc.objc_getClass(b'NSDictionary'),'dictionary')
    data=msg(bitmap,'representationUsingType:properties:',args=(C.c_ulong,C.c_void_p),values=(4,props))
    name=msg(objc.objc_getClass(b'NSString'),'stringWithUTF8String:',args=(C.c_char_p,),values=(str(path).encode(),))
    ok=msg(data,'writeToFile:atomically:',C.c_bool,(C.c_void_p,C.c_bool),(name,True))
    if not ok:raise RuntimeError('Native snapshot write failed')
