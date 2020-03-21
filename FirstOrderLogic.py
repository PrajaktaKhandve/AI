#Author: Prajakta Khandve
#Date: 26th November 2019

import re
import operator
import os
import difflib
import random
import time

st = time.time()

final_res = []
Pred=[]
Arg=[]
HF=[]
VARIABLE=[]


def Get_Input():
    Pfi=open("input.txt",'r')
    Pline = Pfi.readline()
    Plinemat=[]
    while Pline:
        Plinemat.append(Pline.strip())
        Pline = Pfi.readline()
    nq = int(Plinemat[0])
    Queries = []
    for x in range(nq):
        Queries.append(Plinemat[1+x])
    nkb = int(Plinemat[nq+1])
    for x in range(nkb):
        ImplyKey=0
        if('=>' in Plinemat[2+nq+x]):
            HornForm  = Horn_Transform(Plinemat[2+nq+x],ImplyKey)
            s = HornForm[0]
            HF.append(HornForm)
        else:
            HornForm  = [Plinemat[2+nq+x],ImplyKey]
            s = HornForm[0]
            HF.append(HornForm)
    Queries1(Queries)


def Queries1(Q):
    for q in Q:
        Clause = Clauses()
        #KB = KB1()
        final_res.append(Refutation(Clause,q))
    Write_File()

def Clauses():
    Clause=[]
    for x in HF:
        Clause.append(Extract_Horn_Form_Pred(x[0]))
    return(Clause)


def Refutation(Clause,q):
    Q = Extract_Args(Negation(q))
    Clause.append([Q])
    #print 'SC',Clause
    l1=0
    cnt=0
    while(True):
        flag = True
        new = []
        cnt = cnt+1
        #print len(Clause)
        #print Clause
        #print '\n\n'
        #print 'Iteration',cnt
        for v in VARIABLE:
            VARIABLE.pop()
        for i in range(0,len(Clause)):
            x = Clause[i]
            for j in range(l1,len(Clause)):
                y = Clause[j]
                if(x!=y):
                    res = PL_RESOLVE(x,y)
                    if(res==None):# when x and y cannot resolve do nothing continue with next pairs
                        continue
                    #else:
                    #    print res
                    if(res == []):
                        #print 'Time:',(time.time()-st)
                        return('TRUE')
                    if(res not in new):
                            new.append(res)
        l1 = len(Clause)
        for n in new:
            if(Compare_2_Clauses(n,Clause)):#it returns true which means good to add
                Clause.append(n)
                flag = False
        if(flag == True):#if flag is True which means we have added nothing new to the KB
            #print 'FALSE'
            return('FALSE')
        #print 'Time:',(time.time()-st)
        if((time.time()-st)>100):
            return('FALSE')
        


def check_all_consts(r):
    for i in range(1,len(r)):
        if(constant(r[i])):
            continue
        else:
            return(False)
    return(True)
            
                  
def Write_File():
    if os.path.exists("output.txt"):
        os.remove("output.txt")
    output = open("output.txt","w+")
    for x in final_res:
        output.write(x+'\n')


def Compare_2_Clauses(n,Clause):#returns True if no similar sentence n not in Clause
    for c in Clause:
         if(len(c) == len(n)):
             if(Check_Similarity(c,n)):
                 #print 'c',c
                 #print 'n',n
                 #exit()
                 return(False)#if u find similar return False
    return(True)#if we do not find anything same return True and get it added


def Check_Similarity(c,n):#if both are similar return True
    for x in c:
        #print 'x',x
        for y in n:
            #print 'y',y
            if(x[0] in y and check_cond(x,y)):
                #print 'found x',x
                #print 'found y',y
                flag = True
                break
            else:
                #print 'did not find x',x
                flag = False
        if(flag == False):
            return(False)
    return(True)
                
def check_cond(x,y):
    for i in range(1,len(y)):
        if((variable(x[i]) and variable(y[i])) or(constant(x[i]) and constant(y[i]) and x[i]==y[i])):
            continue
        else:
            return(False)#return False if not similar
    return(True)


def PL_RESOLVE(x1,x2):
    refute=[]
    k1=[]
    k2=[]
    for x in x1:
        k1.append(x[:])#copying every element to new list
    for x in x2:
        k2.append(x[:])#copying every element to new list
    Standardize_Var(k1)
    Standardize_Var(k2)
    refute = Find_Pred_2_Resolve(k1,k2)#refute will change
    if(refute == None):#if Ci and Cj doesn't resolve do nothing
        return(refute)
    else:
        refute = removeDuplicates(refute)#remove duplicates after unification
    return(refute)

def Find_Pred_2_Resolve(k1,k2):
    for r in k1:
        for x in k2:
            if(x!=r and Check_Neg(r,x)):
                s = k1+k2
                refute = Unify_Func(r,x,s)#unify both and unify refute and remove both from refute if they are complete
                if(refute != None):
                    refute = Remove_Negations(r,x,refute)
                return(refute)
            else:
                continue
    return(None)
    

def Check_Neg(r,x):#to check if they can be unified
    n=Negation(r[0])
    if(x[0]!=n):
        return(False)
    else:
        for i in range(1,len(r)):
            if(constant(x[i]) and constant(r[i]) and x[i]!=r[i]):
                return(False)
    return(True)
        

def Remove_Negations(r,x,refute):
    refute.remove(r)
    refute.remove(x)
    return(refute)


def removeDuplicates(listofElements):
    uniqueList = []
    for elem in listofElements:
        if elem not in uniqueList:
            uniqueList.append(elem)
    return uniqueList
 

def Standardize_Var(r):#Only standardize variables
    Unify={}
    for x in r:
        for i in range(1,len(x)):
            if(variable(x[i]) and (x[i] in Unify)):
                x[i] = Unify[x[i]]
            elif(variable(x[i]) and (x[i] not in Unify)):
                var = Create_New_Var()
                Unify[x[i]] = var#we create a new variable
                x[i] = Unify[x[i]]
            else:
                continue
    return(r)
         

def Unify_Func(r,k,refute):
    Unify={}
    for i in range(1,len(r)):
        if(variable(k[i]) and constant(r[i])):
            var = k[i]
            const = r[i]
            Unify[var]=const
        elif(constant(k[i]) and variable(r[i])):
            var = r[i]
            const = k[i]
            Unify[var]=const
        elif(variable(k[i]) and variable(r[i])):
            var = r[i]
            const = k[i]
            Unify[var]=const
        elif(constant(k[i]) and constant(r[i]) and k[i]!=r[i]):
            return(None)
        elif(constant(k[i]) and constant(r[i]) and k[i]==r[i]):
            continue
        for x in refute:
            for i in range(1,len(x)):
                if(x[i] in Unify):
                    x[i]=Unify[x[i]]
                    if(x[i] in VARIABLE):
                        VARIABLE.remove(x[i])
    return(refute) 
        

def Create_New_Var():
    r = random.randint(1,30)
    var = 'nvar'+str(r)
    if(var not in VARIABLE):
        VARIABLE.append(var)
    return(var)


def variable(j):
    #print 'in var',j
    if(ord(j[0])>=97 and ord(j[0])<=122):
        return(True)
    else:
        return(False)     


def constant(j):
    #print 'in cn',j
    if(ord(j[0])>=65 and ord(j[0])<=90):
        return(True)
    else:
        return(False)

        

def Divide_Horn_Form(r):
    Args=[]
    x=r.split('|')
    for i in x:
        Args.append(Extract_Args(i))
    return(Args)
    

def Negation(q):
    if('~' in q):
        q=q.replace('~','')
    else:
        q = '~'+q
    return(q)
        

def Extract_Pred(p):
    Args=[]
    if('=>' in p):
        x,y = p.split('=>')
        x = x.split('&')
        x.append(y)
        for i in x:
            Args.append(Extract_Args(i))
    else:
        Args.append(Extract_Args(p))
    return(Args)

def Extract_Horn_Form_Pred(p):
    Args=[]
    x = p.split('|')
    for i in x:
            Args.append(Extract_Args(i))        
    return(Args)
    

def Extract_Args(p):
    r=[]
    pred = p.split('(')
    r.append(pred[0].strip())
    if(',' in pred[1]):
        pred = pred[1].split(')')[0]
        pred = pred.split(',')
        for q in pred:
            r.append(q.strip())
    else:
        r.append(pred[1].split(')')[0].strip())
    return(r)
    

def Horn_Transform(p,key):
    x,y = p.split('=>')
    l = x.split('&')
    k=[]
    for i in l:
        i=i.strip()
        if('~' in i):
            i=i.replace('~','')
        elif('~' not in i):
            i='~'+i
        k.append(i)
    k.append(y)
    s='|'.join(k)
    return([s,key])
    

def main():
    Get_Input()
    
    Write_File()
    
if __name__== "__main__":
    main()

