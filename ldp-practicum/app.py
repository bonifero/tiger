"""ЛП-Практикум: exact LP/IP desktop workbench."""
import sys
import queue
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from model import Problem, number
from formats import load, save, settings
from presets import PRESETS
from simplex import solve

BG='#f3f5f9';INK='#17243b';NAVY='#12233c';BLUE='#315fea';FONT='Segoe UI'

class ScrollArea(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent,bg='white')
        self.canvas=tk.Canvas(self,bg='white',highlightthickness=0)
        self.inner=tk.Frame(self.canvas,bg='white')
        self.canvas.create_window(0,0,anchor='nw',window=self.inner)
        self.canvas.grid(row=0,column=0,sticky='nsew')
        h=ttk.Scrollbar(self,orient='horizontal',command=self.canvas.xview);h.grid(row=1,column=0,sticky='ew')
        self.canvas.configure(yscrollcommand=self._vertical,xscrollcommand=h.set)
        self.v=ttk.Scrollbar(self,orient='vertical',command=self.canvas.yview);self.v.grid(row=0,column=1,sticky='ns')
        self.inner.bind('<Configure>',lambda e:self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.rowconfigure(0,weight=1);self.columnconfigure(0,weight=1)
    def _vertical(self,a,b):self.v.set(a,b)

class App(tk.Tk):
    def __init__(self):
        super().__init__();self.title('ЛП · Практикум');self.geometry('1280x850');self.minsize(1050,720);self.configure(bg=BG)
        style=ttk.Style(self);style.theme_use('clam');style.configure('.',font=(FONT,11));style.configure('TButton',padding=(12,9))
        style.configure('Accent.TButton',background=BLUE,foreground='white');style.map('Accent.TButton',background=[('active','#254bc5')])
        self.dirty=False;self.running=False;self.events=[];self.current_problem=None
        self.scale=tk.IntVar(value=100);self.decimal=tk.BooleanVar(value=False);self.integer=tk.BooleanVar(value=False);self.integer_goal=tk.BooleanVar(value=False)
        self.stop_flag=threading.Event();self.gate=threading.Event();self.auto=threading.Event()
        side=tk.Frame(self,bg=NAVY,width=220);side.pack(side='left',fill='y');side.pack_propagate(False)
        tk.Label(side,text='ЛП',font=(FONT,32,'bold'),bg=NAVY,fg='white').pack(anchor='w',padx=25,pady=(35,0))
        tk.Label(side,text='П Р А К Т И К У М',font=(FONT,10),bg=NAVY,fg='#aabbd2').pack(anchor='w',padx=25,pady=(0,35))
        self.nav=tk.StringVar(value='01   Исходные данные')
        for title,index in [('01   Исходные данные',0),('02   Модель',1),('03   Решение',2),('04   Результат',3)]:
            tk.Button(side,text=title,anchor='w',bg=NAVY,fg='white',bd=0,padx=24,pady=15,command=lambda i=index:self.tabs.select(i)).pack(fill='x')
        tk.Label(side,text='ЛАБОРАТОРНАЯ 2\nСимплекс · Отсечения',bg=NAVY,fg='#aabbd2',justify='left').pack(side='bottom',anchor='w',padx=24,pady=30)
        main=tk.Frame(self,bg=BG);main.pack(fill='both',expand=True,padx=25,pady=22)
        top=tk.Frame(main,bg=BG);top.pack(fill='x')
        tk.Label(top,text='Линейное программирование',font=(FONT,23,'bold'),fg=INK,bg=BG).pack(side='left')
        ttk.Combobox(top,textvariable=self.scale,values=[50,75,100,125,150],width=5,state='readonly').pack(side='right')
        tk.Label(top,text='Масштаб, %',bg=BG,fg=INK).pack(side='right',padx=8)
        self.tabs=ttk.Notebook(main);self.tabs.pack(fill='both',expand=True,pady=18)
        self.editor=tk.Frame(self.tabs,bg='white');self.model_view=tk.Text(self.tabs,wrap='word',font=(FONT,12),padx=20,pady=20)
        self.work=tk.Frame(self.tabs,bg='white');self.result=tk.Text(self.tabs,wrap='word',font=(FONT,13),padx=20,pady=20)
        for widget,title in [(self.editor,'Исходные данные'),(self.model_view,'Модель'),(self.work,'Решение'),(self.result,'Результат')]:self.tabs.add(widget,text=title)
        tools=tk.Frame(self.editor,bg='white');tools.pack(fill='x',padx=14,pady=14)
        self.preset=ttk.Combobox(tools,values=[p.name for p in PRESETS],state='readonly',width=36);self.preset.current(0);self.preset.pack(side='left')
        ttk.Button(tools,text='Выбрать',command=self.choose).pack(side='left',padx=5)
        ttk.Button(tools,text='Открыть',command=self.open_file).pack(side='left',padx=5)
        ttk.Button(tools,text='Сохранить',command=self.save_file).pack(side='left')
        dims=tk.Frame(self.editor,bg='white');dims.pack(fill='x',padx=14)
        self.n=tk.IntVar(value=3);self.m=tk.IntVar(value=2);self.sense=tk.StringVar(value='min')
        for title,var in [('Переменных',self.n),('Ограничений',self.m)]:
            ttk.Label(dims,text=title).pack(side='left',padx=5);ttk.Spinbox(dims,from_=1,to=100,textvariable=var,width=4).pack(side='left')
        ttk.Combobox(dims,textvariable=self.sense,values=['min','max'],state='readonly',width=5).pack(side='left',padx=8)
        ttk.Button(dims,text='Новая таблица',command=self.new_table).pack(side='left')
        ttk.Button(dims,text='Добавить ограничение',command=self.branch).pack(side='left',padx=6)
        self.gridarea=ScrollArea(self.editor);self.gridarea.pack(fill='both',expand=True,padx=14,pady=12)
        bottom=tk.Frame(self.editor,bg='white');bottom.pack(fill='x',padx=14,pady=12)
        ttk.Checkbutton(bottom,text='Целочисленно · отсечения',variable=self.integer).pack(side='left')
        ttk.Checkbutton(bottom,text='F также целая',variable=self.integer_goal).pack(side='left',padx=8)
        ttk.Button(bottom,text='Проверить модель',command=self.show_model).pack(side='right')
        buttons=tk.Frame(self.work,bg='white');buttons.pack(fill='x',padx=14,pady=12)
        ttk.Button(buttons,text='Следующий шаг',command=self.step).pack(side='left')
        ttk.Button(buttons,text='Решить полностью',style='Accent.TButton',command=self.run_all).pack(side='left',padx=8)
        ttk.Button(buttons,text='Остановить',command=self.stop).pack(side='left')
        ttk.Checkbutton(buttons,text='Десятичный вид',variable=self.decimal,command=self.refresh_table).pack(side='right')
        self.summary=tk.StringVar(value='Готово к решению');ttk.Label(self.work,textvariable=self.summary,font=(FONT,12,'bold')).pack(fill='x',padx=14,pady=8)
        self.pages=ttk.Notebook(self.work);self.pages.pack(fill='both',expand=True,padx=14,pady=10)
        self.table=ScrollArea(self.pages);self.journal=tk.Text(self.pages,font=(FONT,11),wrap='word')
        self.pages.add(self.table,text='Рабочая таблица');self.pages.add(self.journal,text='Журнал')
        self.source_view=tk.Text(self.pages,font=(FONT,11),wrap='word',padx=15,pady=15);self.pages.add(self.source_view,text='Исходные данные')
        self.history=ttk.Combobox(self.work,state='readonly');self.history.pack(fill='x',padx=14,pady=8);self.history.bind('<<ComboboxSelected>>',lambda e:self.refresh_table())
        self.scale.trace_add('write',lambda *args:self.rescale())
        self.protocol('WM_DELETE_WINDOW',self.close)
        self.set_problem(PRESETS[0]);self.poll_id=self.after(40,self.poll)

    def confirm(self):return not (self.dirty or self.running) or messagebox.askyesno('Заменить задачу?','Текущие несохранённые изменения и ход решения будут сброшены.')
    def set_problem(self,p):
        self.stop();self.problem=p;self.n.set(len(p.c));self.m.set(len(p.b));self.sense.set(p.sense)
        self.events=[];self.history['values']=[];self.current_problem=None
        for area in (self.table.inner,self.gridarea.inner):
            for child in area.winfo_children():child.destroy()
        font=(FONT,max(8,int(11*self.scale.get()/100)))
        self.cells=[]
        for j,title in enumerate([*p.names,'Знак','Правая часть']):ttk.Label(self.gridarea.inner,text=title,padding=7).grid(row=0,column=j+1)
        for i,row in enumerate([*p.A,p.c]):
            ttk.Label(self.gridarea.inner,text=f'Ограничение {i+1}' if i<len(p.b) else 'F',padding=6).grid(row=i+1,column=0)
            values=[*row,p.signs[i],p.b[i]] if i<len(p.b) else list(row)
            entries=[]
            for j,value in enumerate(values):
                var=tk.StringVar(value=str(value));var.trace_add('write',self.mark_dirty)
                widget=ttk.Combobox(self.gridarea.inner,textvariable=var,values=['<=','=','>=','<','>'],width=6,state='readonly') if j==len(p.c) else ttk.Entry(self.gridarea.inner,textvariable=var,width=12,font=font)
                widget.grid(row=i+1,column=j+1,padx=2,pady=3);entries.append(var)
            self.cells.append(entries)
        self.dirty=False;self.summary.set('Готово к решению');self.text(self.result,'Решение ещё не запускалось.');self.text(self.model_view,'Нажмите «Проверить модель».');self.text(self.journal,'')
    def mark_dirty(self,*args):self.dirty=True
    def read_problem(self):
        n=len(self.problem.c);m=len(self.problem.b)
        return Problem([v.get() for v in self.cells[m]],[[v.get() for v in row[:n]] for row in self.cells[:m]],[r[n+1].get() for r in self.cells[:m]],[r[n].get() for r in self.cells[:m]],self.sense.get(),self.problem.name,self.problem.names)
    def choose(self):
        if self.confirm():self.set_problem(PRESETS[self.preset.current()]);self.tabs.select(0)
    def new_table(self):
        try:
            n=self.n.get();m=self.m.get()
            if not 1<=n<=100 or not 1<=m<=200:raise ValueError('Допустимо 1–100 переменных и 1–200 ограничений.')
            p=Problem([0]*n,[[0]*n for _ in range(m)],[0]*m,['<=']*m,self.sense.get())
            if self.confirm():self.set_problem(p)
        except Exception as e:messagebox.showerror('Ошибка ввода',str(e))
    def branch(self):
        try:
            p=self.read_problem()
            if not self.confirm():return
            p=Problem(p.c,(*p.A,(0,)*len(p.c)),(*p.b,0),(*p.signs,'<='),p.sense,p.name+' · подзадача',p.names)
            self.set_problem(p);self.dirty=True;self.tabs.select(0)
        except Exception as e:messagebox.showerror('Ошибка',str(e))
    def open_file(self):
        path=filedialog.askopenfilename(filetypes=[('Задачи','*.json *.ini'),('Все файлы','*.*')])
        if not path:return
        try:
            p=load(path);ip,goal=settings(path)
            if self.confirm():self.set_problem(p);self.integer.set(ip);self.integer_goal.set(goal);self.tabs.select(0)
        except Exception as e:messagebox.showerror('Ошибка файла',str(e))
    def save_file(self):
        try:
            p=self.read_problem();path=filedialog.asksaveasfilename(defaultextension='.json',filetypes=[('JSON','*.json'),('Старый INI','*.ini')])
            if path:save(path,p,self.integer.get(),self.integer_goal.get());self.dirty=False
        except Exception as e:messagebox.showerror('Ошибка сохранения',str(e))
    def show_model(self):
        try:
            p=self.read_problem();lines=[p.name,'',f'{p.sense} F = '+self.expression(p.c,p.names),'']
            lines.extend(f'{self.expression(r,p.names)} {s} {b}' for r,s,b in zip(p.A,p.signs,p.b));lines+=['','Все переменные ≥ 0.','Целочисленные переменные.' if self.integer.get() else 'Непрерывные переменные.']
            self.text(self.model_view,'\n'.join(lines));self.tabs.select(1)
        except Exception as e:messagebox.showerror('Ошибка модели',str(e))
    @staticmethod
    def expression(row,names):return ' + '.join(f'({v})·{n}' for v,n in zip(row,names) if v) or '0'
    @staticmethod
    def text(widget,value):widget.configure(state='normal');widget.delete('1.0','end');widget.insert('end',value);widget.configure(state='disabled')
    def start(self,automatic):
        try:p=self.read_problem()
        except Exception as e:messagebox.showerror('Ошибка ввода',str(e));return False
        self.stop();self.current_problem=p;self.events=[];self.history['values']=[];self.text(self.journal,'')
        self.text(self.source_view,p.name+'\n\n'+p.sense+' F = '+self.expression(p.c,p.names)+'\n\n'+'\n'.join(self.expression(r,p.names)+' '+s+' '+str(b) for r,s,b in zip(p.A,p.signs,p.b)))
        self.messages=queue.Queue(maxsize=4);messages=self.messages;stop=threading.Event();gate=threading.Event();auto=threading.Event()
        self.stop_flag=stop;self.gate=gate;self.auto=auto;self.running=True
        self.tabs.tab(0,state='disabled')
        if automatic:auto.set()
        gate.set();integer=self.integer.get();goal=self.integer_goal.get()
        def send(value):
            while not stop.is_set():
                try:messages.put(value,timeout=.1);return
                except queue.Full:pass
        def worker():
            try:
                gen=solve(p,integer,goal)
                while not stop.is_set():
                    if not auto.is_set():
                        if not gate.wait(.1):continue
                        gate.clear()
                    try:event=next(gen)
                    except StopIteration:break
                    send(event)
            except Exception as e:send(str(e))
            finally:send(None)
        threading.Thread(target=worker,daemon=True).start();self.tabs.select(2);return True
    def step(self):
        if not self.running:self.start(False)
        else:self.auto.clear();self.gate.set()
    def run_all(self):
        if not self.running:self.start(True)
        else:self.auto.set();self.gate.set()
    def stop(self):
        self.stop_flag.set();self.gate.set()
        if hasattr(self,'messages'):del self.messages
        if self.running:self.summary.set('Остановлено пользователем · результат не доказан')
        self.running=False
        self.tabs.tab(0,state='normal')
    def poll(self):
        if hasattr(self,'messages'):
            try:
                item=self.messages.get_nowait()
                if item is None:self.running=False;self.tabs.tab(0,state='normal')
                elif isinstance(item,str):self.running=False;self.tabs.tab(0,state='normal');self.summary.set('Ошибка вычисления');messagebox.showerror('Ошибка вычисления',item)
                else:
                    self.events.append(item)
                    if len(self.events)>300:self.events.pop(0)
                    self.history['values']=[f'{i+1}. {e.title}' for i,e in enumerate(self.events)];self.history.current(len(self.events)-1)
                    self.summary.set(f'{item.title}  ·  итерация {item.iteration}  ·  отсечений {item.cuts}  ·  F = {self.fmt(item.objective)}')
                    self.journal.configure(state='normal');self.journal.insert('end',self.summary.get()+'\n');self.journal.configure(state='disabled');self.journal.see('end');self.refresh_table()
                    if item.status!='running':
                        self.running=False
                        self.tabs.tab(0,state='normal')
                        statuses={'optimal':'Оптимальное решение','infeasible':'Нет допустимого решения','unbounded':'Целевая функция не ограничена','limit':'Вычисления остановлены по лимиту','undetermined':'LP-релаксация не ограничена; целочисленный статус не установлен'}
                        lines=[statuses.get(item.status,item.status)]
                        if item.status=='optimal':lines += ['',*[f'{n} = {self.fmt(v)}' for n,v in zip(self.current_problem.names,item.x)],'',f'F = {self.fmt(item.objective)}','', 'План проверен по исходным ограничениям.']
                        else:lines+=['','Оптимальный план не выдан.']
                        self.text(self.result,'\n'.join(lines))
            except queue.Empty:pass
        self.poll_id=self.after(40,self.poll)
    def destroy(self):
        self.stop()
        if hasattr(self,'poll_id'):
            self.after_cancel(self.poll_id)
        super().destroy()
    def fmt(self,v):return '—' if v is None else (f'{float(v):.8g}' if self.decimal.get() else str(v))
    def refresh_table(self):
        for child in self.table.inner.winfo_children():child.destroy()
        if not self.events:return
        idx=self.history.current();e=self.events[max(0,idx)];font=(FONT,max(8,int(11*self.scale.get()/100)))
        if not e.rows:return
        for j,name in enumerate(['Базис',*e.names,'b']):tk.Label(self.table.inner,text=name,bg='#edf5ff',font=font,padx=10,pady=9).grid(row=0,column=j,sticky='nsew',padx=1,pady=1)
        for i,row in enumerate(e.rows):
            title=e.names[e.basis[i]] if i<len(e.basis) else 'Оценки'
            for j,value in enumerate([title,*map(self.fmt,row)]):
                bg='#d8e5ff' if e.pivot and (i,j-1)==e.pivot else ('#f5f7fb' if j==0 else 'white')
                tk.Label(self.table.inner,text=value,bg=bg,fg=INK,font=font,padx=9,pady=7).grid(row=i+1,column=j,sticky='nsew',padx=1,pady=1)
    def rescale(self):
        font=(FONT,max(8,int(11*self.scale.get()/100)))
        for w in self.gridarea.inner.winfo_children():
            if isinstance(w,ttk.Entry):w.configure(font=font)
        self.refresh_table()
    def close(self):
        if self.confirm():self.stop();self.destroy()

if __name__=='__main__':
    app=App()
    if '--smoke-test' in sys.argv:
        app.update();app.start(True)
        def finish():app.stop();app.destroy()
        app.after(600,finish)
    app.mainloop()
