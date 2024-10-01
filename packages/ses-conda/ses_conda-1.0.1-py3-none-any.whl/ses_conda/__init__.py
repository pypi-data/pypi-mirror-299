#author: 街角的猫_wjz
#copyright(c) SESISEC Tech Inc. All rights reserved.

import time
import json

class body:
    def __init__(self,idx,disp="x",name="default"):
        self.type="body"
        self.idx=idx
        self.disp=disp
        self.name=name
        self.fri=0 #function resistance instance
        self.frv=0 #function resistance value
        self.fv=0 #function value
    def export(self):
        return {"idx": a.idx,
               "disp": a.disp,
               "name": a.name,
               "fri": a.fri,
               "frv": a.frv,
               "fv": a.fv}

class operation:
    class b2:
        def __init__(self,src,tgt,t=time.time()):
            self.src=src
            self.tgt=tgt
            self.t=t
            self.alias="b2"
    class ch:
        def __init__(self,src,tgt,t=time.time()):
            self.src=src
            self.tgt=tgt
            self.t=t
            self.alias="ch"
    class lc:
        def __init__(self,src,tgt,t=time.time()):
            self.src=src
            self.tgt=tgt
            self.t=t
            self.alias="lc"
    class sl:
        def __init__(self,src,tgt,t=time.time()):
            self.src=src
            self.tgt=tgt
            self.t=t
            self.alias="sl"
    class rd: ##stands for `return(double)`
        def __init__(self,src,tgt,t=time.time()):
            self.src=src
            self.tgt=tgt
            self.t=t
            self.alias="rd"
class function:
    def __init__(self,src,tgt,fi=0,fi_st=0,fi_ts=0):
        self.type="function"
        self.src=src #source
        self.tgt=tgt #target
        self.fi=fi #function instance
        self.fi_st=fi_st #source to target
        self.fi_ts=fi_ts #target to source
        self.fi_t=0 #backend extension for function total instance
        self.history=[]
    def export(self):
        hist=[]
        for i in a.history:
            hist.append({"alias": i.alias,
                         "src": i.src.idx,
                         "tgt": i.tgt.idx,
                         "t": i.t})
        return {"src": a.src.idx,
                "tgt": a.tgt.idx,
                "fi": a.fi,
                "fi_st": a.fi_st,
                "fi_ts": a.fi_ts,
                "fi_t": a.fi_t,
                "history": hist}

class database:
    def __init__(self,scope="default"):
        self.scope=scope
        self.dat={"scope": self.scope,
                  "bodies": [],
                  "functions": [],
                  }
    def add(self,a):
        if a.type=="body":
            self.dat["bodies"].append({"idx": a.idx,
                                       "disp": a.disp,
                                       "name": a.name,
                                       "fri": a.fri,
                                       "frv": a.frv,
                                       "fv": a.fv})
        elif a.type=="function":
            hist=[]
            for i in a.history:
                hist.append({"alias": i.alias,
                             "src": i.src.idx,
                             "tgt": i.tgt.idx,
                             "t": i.t})
            self.dat["functions"].append({
                "src": a.src.idx,
                "tgt": a.tgt.idx,
                "fi": a.fi,
                "fi_st": a.fi_st,
                "fi_ts": a.fi_ts,
                "fi_t": a.fi_t,
                "history": hist})
        else:
            raise TypeError("Inappropriate object for database.add(). Supports"+\
                            " \"body\" and \"function\" only.")
    def load(self,a):
        if type(a)!=dict:
            raise TypeError("Inappropriate object for database.load(). Support"+\
                            "s \"dict\" only.")
            return
        self.dat=a
    def import_(self,a):
        if type(a)!=dict:
            raise TypeError("Inappropriate object for database.import_(). Suppo"+\
                            "rts \"dict\" only.")
            return
        try:
            v=a["fi"]
            self.dat["functions"].append(a)
        except:
            self.dat["bodies"].append(a)

class fx:
    def function_(src,tgt,fi=0,fi_st=0,fi_ts=0):
        return function(src,tgt,fi,fi_st,fi_ts)
    class operate:
        def b2(src,tgt,t=time.time()):
            return operation.b2(src,tgt,t)
        def ch(src,tgt,t=time.time()):
            return operation.ch(src,tgt,t)
        def sl(src,tgt,t=time.time()):
            return operation.sl(src,tgt,t)
        def lc(src,tgt,t=time.time()):
            return operation.lc(src,tgt,t)
        def rd(src,tgt,t=time.time()):
            return operation.b2(src,tgt,t)

class conversion:
    def save_to_json(dict_data,file_name):
        if type(a)!=dict:
            raise TypeError
            return
        dict_str=json.dumps(dict_data,indent=4,ensure_ascii=False)
        with open(file_name,"w") as f:
            r=f.write(dict_str)
            f.close()
            return r
    def load_from_json(file_name):
        with open(file_name,"r") as f:
            return json.dumps(f.read())

if __name__=="__main__":
    print("""This is a module, not a program.
It cannot be run directly.
Try importing it in another Python program.
Example: from ses_conda import *""")
#test some data
"""
a=body(5)
b=body(30)
c=function(a,b)
d=operation.b2(a,b)
c.history.append(d)
e=database("jc")
e.add(c)
print(e.dat)
"""
    
        
