"""Bounded Win32 UI probe of the supplied Delphi EXE; no memory patching."""
from pathlib import Path
import ctypes as C
from ctypes import wintypes as W
import hashlib, itertools, json, os, subprocess, sys, time, traceback
from PIL import ImageGrab

ROOT = Path(__file__).resolve().parents[2]
EXE = ROOT / 'source/Лаб_3/Загрузка_рюкзака.exe'
OUT = ROOT / 'qa/lab3-parity-2026-11-23/runtime-original'
OUT.mkdir(parents=True, exist_ok=True)
U=C.WinDLL('user32', use_last_error=True)
U.SetProcessDPIAware()
CALLBACK=C.WINFUNCTYPE(W.BOOL,W.HWND,W.LPARAM)
U.EnumWindows.argtypes=[CALLBACK,W.LPARAM]
U.EnumChildWindows.argtypes=[W.HWND,CALLBACK,W.LPARAM]
U.GetWindowThreadProcessId.argtypes=[W.HWND,C.POINTER(W.DWORD)]
U.GetWindowRect.argtypes=[W.HWND,C.POINTER(W.RECT)]
U.GetClientRect.argtypes=[W.HWND,C.POINTER(W.RECT)]
U.ClientToScreen.argtypes=[W.HWND,C.POINTER(W.POINT)]
U.GetWindowTextW.argtypes=[W.HWND,W.LPWSTR,C.c_int]
U.GetClassNameW.argtypes=[W.HWND,W.LPWSTR,C.c_int]
U.SendMessageW.argtypes=[W.HWND,W.UINT,W.WPARAM,W.LPARAM];U.SendMessageW.restype=W.LPARAM
U.PostMessageW.argtypes=[W.HWND,W.UINT,W.WPARAM,W.LPARAM]
U.SetForegroundWindow.argtypes=[W.HWND]
U.SetWindowPos.argtypes=[W.HWND,W.HWND,C.c_int,C.c_int,C.c_int,C.c_int,W.UINT]
U.IsWindowVisible.argtypes=[W.HWND]
U.IsWindowEnabled.argtypes=[W.HWND]

def enum(parent=None):
    result=[]
    cb=CALLBACK(lambda hwnd,_: result.append(int(hwnd)) or True)
    U.EnumChildWindows(parent,cb,0) if parent else U.EnumWindows(cb,0)
    return result

def text(hwnd):
    b=C.create_unicode_buffer(4096);U.GetWindowTextW(hwnd,b,len(b))
    value=b.value
    try:
        decoded=value.encode('cp1252').decode('cp1251')
        if any('\u0400'<=c<='\u04ff' for c in decoded):return decoded
    except UnicodeError:pass
    return value

def cls(hwnd):
    b=C.create_unicode_buffer(256);U.GetClassNameW(hwnd,b,len(b));return b.value

def rect(hwnd):
    r=W.RECT();U.GetWindowRect(hwnd,C.byref(r));return [r.left,r.top,r.right,r.bottom]

def info(hwnd):
    return dict(hwnd=hwnd,cls=cls(hwnd),text=text(hwnd),rect=rect(hwnd),visible=bool(U.IsWindowVisible(hwnd)),enabled=bool(U.IsWindowEnabled(hwnd)))

def owned(pid):
    result=[]
    for h in enum():
        p=W.DWORD();U.GetWindowThreadProcessId(h,C.byref(p))
        if p.value==pid:result.append(h)
    return result

def wait(predicate, seconds=5):
    end=time.monotonic()+seconds
    while time.monotonic()<end:
        value=predicate()
        if value:return value
        time.sleep(.04)
    raise RuntimeError('Timed out waiting for UI state')

class Probe:
    def __init__(self):
        self.events=[];self.actions=0
        self.proc=subprocess.Popen([str(EXE)],cwd=EXE.parent)
        self.main=wait(lambda:next((h for h in owned(self.proc.pid) if cls(h)=='TForm1'),None))
        U.SetWindowPos(self.main,None,5,5,825,700,0x40)
        U.SetForegroundWindow(self.main);time.sleep(.2)
        # Match HWNDs against the decoded DFM's exact initial positions.
        origin=W.POINT(0,0);U.ClientToScreen(self.main,C.byref(origin))
        anchors={'n':('TEdit',432,24),'b':('TEdit',224,120),'accept_n':('TButton',552,16),
                 'accept_data':('TButton',368,104),'next':('TButton',384,104),
                 'check_candidates':('TButton',16,600),'check_summary':('TButton',480,600),
                 'check_plan':('TButton',624,600),'values':('TStringGrid',144,192),
                 'weights':('TStringGrid',24,192),'candidates':('TStringGrid',16,432),
                 'summary':('TStringGrid',480,424),'restore':('TStringGrid',624,424)}
        self.controls={}
        for name,(klass,x,y) in anchors.items():
            matching=[h for h in enum(self.main) if cls(h)==klass]
            self.controls[name]=min(matching,key=lambda h:abs(rect(h)[0]-origin.x-x)+abs(rect(h)[1]-origin.y-y))
        assert len(set(self.controls.values()))==len(self.controls),self.controls
    def snapshot(self,name):
        time.sleep(.1)
        windows=[dict(info(h),children=[info(c) for c in enum(h)]) for h in owned(self.proc.pid) if U.IsWindowVisible(h)]
        self.events.append(dict(event=name,windows=windows,controls={k:info(h) for k,h in self.controls.items()}))
        (OUT/'observations.json').write_text(json.dumps(self.events,ensure_ascii=False,indent=2),encoding='utf-8')
        ImageGrab.grab(all_screens=True).crop(tuple(rect(self.main))).save(OUT/f'{name}.png')
        print(name,[(k,text(h)) for k,h in self.controls.items() if U.IsWindowVisible(h) and 'TButton'==cls(h)],flush=True)
    def click(self,name):
        h=self.controls[name];assert U.IsWindowVisible(h),(name,'hidden')
        U.PostMessageW(h,0xF5,0,0);self.actions+=1;time.sleep(.16)
    def dialogs(self,label):
        for i in range(4):
            dialogs=[h for h in owned(self.proc.pid) if h!=self.main and U.IsWindowVisible(h)]
            if not dialogs:return
            self.snapshot(f'{label}-dialog-{i}')
            for h in dialogs:
                buttons=[c for c in enum(h) if cls(c) in ('TButton','Button') and U.IsWindowVisible(c)]
                if buttons:U.PostMessageW(buttons[0],0xF5,0,0)
                else:U.PostMessageW(h,0x10,0,0)
            time.sleep(.15)
    def edit(self,name,value):
        b=C.create_unicode_buffer(str(value));U.SendMessageW(self.controls[name],0xC,0,C.addressof(b));self.actions+=1
    def cell(self,name,row,col,value,width=64):
        h=self.controls[name]
        # DFM/default dimensions: columns64px (+1 gridline), rows24px (+1).
        x=2+col*(width+1)+12;y=2+row*25+10
        U.PostMessageW(h,0x201,1,(y<<16)|x);U.PostMessageW(h,0x202,0,(y<<16)|x)
        U.PostMessageW(h,0x100,0x71,0);U.PostMessageW(h,0x101,0x71,0)
        editor=wait(lambda:next((e for e in enum(h) if cls(e)=='TInplaceEdit' and U.IsWindowVisible(e)),None),2)
        b=C.create_unicode_buffer(str(value));U.SendMessageW(editor,0xC,0,C.addressof(b))
        # VCL records edit text on the normal edit-change/focus transition.
        U.PostMessageW(editor,0x100,0xD,0);U.PostMessageW(editor,0x101,0xD,0)
        self.actions+=1;time.sleep(.025)
    def close(self):
        U.PostMessageW(self.main,0x10,0,0)
        try:self.proc.wait(3)
        except subprocess.TimeoutExpired:self.proc.kill();self.proc.wait(3)
        (OUT/'cleanup.json').write_text(json.dumps(dict(pid=self.proc.pid,returncode=self.proc.returncode,actions=self.actions)))

def exhaustive(values,weights,capacity,start,used):
    return max(sum(values[j][x] for j,x in zip(range(start,len(weights)),plan))
               for plan in itertools.product(*(range(len(r)) for r in values[start:]))
               if used+sum(w*x for w,x in zip(weights[start:],plan))<=capacity)

def main():
    assert hashlib.sha256(EXE.read_bytes()).hexdigest()=='6c7440765517e2f484f539491fffb19a66e6e644f57104c61a0c3f09000cf220'
    p=Probe()
    try:
        p.snapshot('00-initial')
        p.edit('n',4);p.click('accept_n');p.dialogs('01-accept-n');p.snapshot('01-condition-empty')
        p.click('accept_data');p.dialogs('02-invalid-condition');p.snapshot('02-condition-error')
        p.edit('b',4)
        values=[[0,10,17,25,36],[0,11,16,25,35],[0,10,18,24,34],[0,9,19,26,35]]
        weights=[1]*4
        for j,row in enumerate(values):
            p.cell('weights',j+1,0,1)
            for x,value in enumerate(row):p.cell('values',j+1,x+1,value)
        p.snapshot('03-condition-filled');p.click('accept_data');p.dialogs('04-condition-accepted');p.snapshot('04-ready')
        for j in reversed(range(4)):
            p.click('next');p.snapshot(f'05-stage-{j+1}-empty')
            states=range(5) if j else [0]
            summaries=[]
            for y in states:
                row=[]
                for x,own in enumerate(values[j]):
                    if y+x<=4:
                        value=own+exhaustive(values,weights,4,j+1,y+x)
                        p.cell('candidates',y+1,x+1,value);row.append((value,x))
                best=max(v for v,x in row);choice=min(x for v,x in row if v==best);summaries.append((y,best,choice))
            p.snapshot(f'06-stage-{j+1}-candidates');p.click('check_candidates');p.dialogs(f'07-stage-{j+1}-candidates');p.snapshot(f'07-stage-{j+1}-summary-empty')
            for y,best,choice in summaries:
                p.cell('summary',y+1,0,best);p.cell('summary',y+1,1,choice)
            p.snapshot(f'08-stage-{j+1}-summary-filled');p.click('check_summary');p.dialogs(f'09-stage-{j+1}-summary');p.snapshot(f'09-stage-{j+1}-accepted')
        p.snapshot('10-restore')
        for j,(y,x) in enumerate(zip([0,0,1,2],[0,1,1,2])):
            p.cell('restore',1,j,y,width=50);p.cell('restore',2,j,x,width=50)
        p.snapshot('11-restore-filled');p.click('check_plan');p.dialogs('12-plan-accepted');p.snapshot('12-result')
    except Exception:
        p.snapshot('failure')
        (OUT/'failure.txt').write_text(traceback.format_exc(),encoding='utf-8')
        raise
    finally:p.close()

if __name__=='__main__':main()
