#AUTHOR : PRAJAKTA KHANDVE
#last modified : 24th Sept 11:02 am
import os
import math

nodes=[]
explored=[]
path={}
PTer=[]
PDest=[]
nodes=[]
explored=[]
path={}
heuristic=[]

def is32pos(num):
    if num > 0:
        return True
    else:
        return False

def Get_Input_File():
    global PW,PH,PN,PX,PY,PZ,PInstr
    i=0
    j=0
    Pfi=open("input.txt",'r')
    Pline = Pfi.readline()
    Pcnt=1
    Plinemat=[]
    while Pline:
        Plinemat.append(Pline.strip())
        Pline = Pfi.readline()
        Pcnt+=1
    PInstr=Plinemat[0].split()[0]
    PW,PH = int(Plinemat[1].split()[0]),int(Plinemat[1].split()[1]) 
    if(not(is32pos(PW) and is32pos(PH))):
       return False
    PX,PY = int(Plinemat[2].split()[0]),int(Plinemat[2].split()[1]) 
    if(not((PX>=0 and PX <= (PW-1)) and (PY>=0 and PY <= (PH-1)))):
        return False
    PZ = int(Plinemat[3].split()[0])
    PN = int(Plinemat[4].split()[0])
    if(not((PZ>=0) and (PN>0))):
        return False
    for i in range(0,PN):
         D1=int(Plinemat[5+i].split()[0])
         D2=int(Plinemat[5+i].split()[1])
         PDest.append([D1,D2])
    for i in range(0,PW):
        PTerR=[]
        for j in range(0,PH):
            Z=int(Plinemat[5+PN+j].split()[i])
            PTerR.append(Z)        
        PTer.append(PTerR)
    Pfi.close()
    return True

def Create_Node(w,h,z,cost,heuristic):
    node={(w,h):[z,cost,heuristic]}
    return(node)

def Initialize_Node():
    snode=Create_Node(PX,PY,PTer[PX][PY],0,0)
    return(snode)

def Node_Unvisited(w,h):
    for x in nodes:
        if(x.keys()==[(w,h)]): 
            return(False)
    return(True)

def Node_UnExplored(w,h):    
    for e in explored:
        if(e.keys()==[(w,h)]): 
            return(False)
    return(True)

def Priority_Q_Index(node):
    index=0
    for i in nodes:
        if(i.values()[0][1]<=node.values()[0][1]):
            index=index+1
    return(index)

def Get_Heuristic(w,h,Dx,Dy):
    return(int(math.sqrt((Dx-w)**2 + (Dy-h)**2))*10)


def A_Star(node,Dx,Dy):
    w= node.keys()[0][0]
    h= node.keys()[0][1]
    z= node[node.keys()[0]]
    children=[]
    PW1=PW-1
    PH1=PH-1
    if(w-1>=0 and abs(PTer[w-1][h]-z[0])<=PZ and Node_Unvisited(w-1,h) and Node_UnExplored(w-1,h)):
         hn= Get_Heuristic(w-1,h,Dx,Dy)
         gn= abs(PTer[w-1][h]-z[0])+10+z[2]
         fn = max(hn+gn,z[1]) 
         temp_node=Create_Node(w-1,h,PTer[w-1][h],fn,gn)
         nodes.insert(Priority_Q_Index(temp_node),temp_node)
         children.append([w-1,h])
    if(w+1 <= PW1 and abs(PTer[w+1][h]-z[0])<=PZ and Node_Unvisited(w+1,h) and Node_UnExplored(w+1,h)):
          hn=Get_Heuristic(w+1,h,Dx,Dy)
          gn= abs(PTer[w+1][h]-z[0])+10+z[2]
          fn = max(hn+gn,z[1])
          temp_node=Create_Node(w+1,h,PTer[w+1][h],fn,gn)
          nodes.insert(Priority_Q_Index(temp_node),temp_node)
          children.append([w+1,h])
    if(h-1>=0 and abs(PTer[w][h-1]-z[0])<=PZ and Node_Unvisited(w,h-1) and Node_UnExplored(w,h-1)): 
         hn=Get_Heuristic(w,h-1,Dx,Dy)
         gn=abs(PTer[w][h-1]-z[0])+10+z[2]
         fn = max(hn+gn,z[1])
         temp_node = Create_Node(w,h-1,PTer[w][h-1],fn,gn)
         nodes.insert(Priority_Q_Index(temp_node),temp_node)
         children.append([w,h-1])
    if(h+1 <=PH1 and abs(PTer[w][h+1]-z[0])<=PZ and Node_Unvisited(w,h+1) and Node_UnExplored(w,h+1)): 
          hn=Get_Heuristic(w,h+1,Dx,Dy)
          gn=abs(PTer[w][h+1]-z[0])+10+z[2]
          fn = max(hn+gn,z[1])
          temp_node=Create_Node(w,h+1,PTer[w][h+1],fn,gn)
          nodes.insert(Priority_Q_Index(temp_node),temp_node)
          children.append([w,h+1])
    if(w-1>=0 and h-1 >=0 and abs(PTer[w-1][h-1]-z[0])<=PZ and Node_Unvisited(w-1,h-1) and Node_UnExplored(w-1,h-1)):
         hn=Get_Heuristic(w-1,h-1,Dx,Dy)
         gn=abs(PTer[w-1][h-1]-z[0])+14+z[2]
         fn = max(hn+gn,z[1])
         temp_node=Create_Node(w-1,h-1,PTer[w-1][h-1],fn,gn)
         nodes.insert(Priority_Q_Index(temp_node),temp_node)
         children.append([w-1,h-1])
    if(w-1>=0 and h+1 <= PH1 and abs(PTer[w-1][h+1]-z[0])<=PZ and Node_Unvisited(w-1,h+1) and Node_UnExplored(w-1,h+1)): 
          hn=Get_Heuristic(w-1,h+1,Dx,Dy)
          gn=abs(PTer[w-1][h+1]-z[0])+14+z[2]
          fn = max(hn+gn,z[1])
          temp_node=Create_Node(w-1,h+1,PTer[w-1][h+1],fn,gn)
          nodes.insert(Priority_Q_Index(temp_node),temp_node)
          children.append([w-1,h+1])
    if(w+1 <= PW1 and h+1 <=PH1 and abs(PTer[w+1][h+1]-z[0])<=PZ and Node_Unvisited(w+1,h+1) and Node_UnExplored(w+1,h+1)): 
          hn=Get_Heuristic(w+1,h+1,Dx,Dy)
          gn=abs(PTer[w+1][h+1]-z[0])+14+z[2]
          fn = max(hn+gn,z[1])
          temp_node=Create_Node(w+1,h+1,PTer[w+1][h+1],fn,gn)
          nodes.insert(Priority_Q_Index(temp_node),temp_node)
          children.append([w+1,h+1])
    if(w+1 <= PW1 and h-1>=0 and abs(PTer[w+1][h-1]-z[0])<=PZ and Node_Unvisited(w+1,h-1) and Node_UnExplored(w+1,h-1)):
          hn=Get_Heuristic(w+1,h-1,Dx,Dy)
          gn=abs(PTer[w+1][h-1]-z[0])+14+z[2]
          fn = max(hn+gn,z[1])
          temp_node=Create_Node(w+1,h-1,PTer[w+1][h-1],fn,gn)
          nodes.insert(Priority_Q_Index(temp_node),temp_node)
          children.append([w+1,h-1])
    path[(w,h)]=children

def UCS(node):
    w= node.keys()[0][0]
    h= node.keys()[0][1]
    z= node[node.keys()[0]]
    children=[]
    PW1=PW-1
    PH1=PH-1
    if(w-1>=0 and abs(PTer[w-1][h]-z[0])<=PZ and Node_Unvisited(w-1,h) and Node_UnExplored(w-1,h)):
         temp_node=Create_Node(w-1,h,PTer[w-1][h],10+z[1],0)
         nodes.insert(Priority_Q_Index(temp_node),temp_node)
         children.append([w-1,h])
    if(w+1 <= PW1 and abs(PTer[w+1][h]-z[0])<=PZ and Node_Unvisited(w+1,h) and Node_UnExplored(w+1,h)):
          temp_node = Create_Node(w+1,h,PTer[w+1][h],10+z[1],0)
          nodes.insert(Priority_Q_Index(temp_node),temp_node)
          children.append([w+1,h])
    if(h-1>=0 and abs(PTer[w][h-1]-z[0])<=PZ and Node_Unvisited(w,h-1) and Node_UnExplored(w,h-1)): 
         temp_node = Create_Node(w,h-1,PTer[w][h-1],10+z[1],0)
         nodes.insert(Priority_Q_Index(temp_node),temp_node)
         children.append([w,h-1])
    if(h+1 <=PH1 and abs(PTer[w][h+1]-z[0])<=PZ and Node_Unvisited(w,h+1) and Node_UnExplored(w,h+1)): 
          temp_node=Create_Node(w,h+1,PTer[w][h+1],10+z[1],0)
          nodes.insert(Priority_Q_Index(temp_node),temp_node)
          children.append([w,h+1])
    if(w-1>=0 and h-1 >=0 and abs(PTer[w-1][h-1]-z[0])<=PZ and Node_Unvisited(w-1,h-1) and Node_UnExplored(w-1,h-1)): 
         temp_node=Create_Node(w-1,h-1,PTer[w-1][h-1],14+z[1],0)
         nodes.insert(Priority_Q_Index(temp_node),temp_node)
         children.append([w-1,h-1])
    if(w-1>=0 and h+1 <= PH1 and abs(PTer[w-1][h+1]-z[0])<=PZ and Node_Unvisited(w-1,h+1) and Node_UnExplored(w-1,h+1)): 
          temp_node=Create_Node(w-1,h+1,PTer[w-1][h+1],14+z[1],0)
          nodes.insert(Priority_Q_Index(temp_node),temp_node)
          children.append([w-1,h+1])
    if(w+1 <= PW1 and h+1 <=PH1 and abs(PTer[w+1][h+1]-z[0])<=PZ and Node_Unvisited(w+1,h+1) and Node_UnExplored(w+1,h+1)): 
          temp_node=Create_Node(w+1,h+1,PTer[w+1][h+1],14+z[1],0)
          nodes.insert(Priority_Q_Index(temp_node),temp_node)
          children.append([w+1,h+1])
    if(w+1 <= PW1 and h-1>=0 and abs(PTer[w+1][h-1]-z[0])<=PZ and Node_Unvisited(w+1,h-1) and Node_UnExplored(w+1,h-1)):
          temp_node=Create_Node(w+1,h-1,PTer[w+1][h-1],14+z[1],0)
          nodes.insert(Priority_Q_Index(temp_node),temp_node)
          children.append([w+1,h-1])
    path[(w,h)]=children

def BFSQF(node):
     w= node.keys()[0][0]
     h= node.keys()[0][1]
     z= node[node.keys()[0]]
     cost=0
     children=[]
     PW1=PW-1
     PH1=PH-1
     if(w-1>=0 and abs(PTer[w-1][h]-z[0])<=PZ and Node_Unvisited(w-1,h) and Node_UnExplored(w-1,h)):
         nodes.append(Create_Node(w-1,h,PTer[w-1][h],cost,0))
         children.append([w-1,h])
     if(w+1 <= PW1 and abs(PTer[w+1][h]-z[0])<=PZ and Node_Unvisited(w+1,h) and Node_UnExplored(w+1,h)):
          nodes.append(Create_Node(w+1,h,PTer[w+1][h],cost,0))
          children.append([w+1,h])
     if(h-1>=0 and abs(PTer[w][h-1]-z[0])<=PZ and Node_Unvisited(w,h-1) and Node_UnExplored(w,h-1)): 
         nodes.append(Create_Node(w,h-1,PTer[w][h-1],cost,0))
         children.append([w,h-1])
     if(h+1 <=PH1 and abs(PTer[w][h+1]-z[0])<=PZ and Node_Unvisited(w,h+1) and Node_UnExplored(w,h+1)): 
          nodes.append(Create_Node(w,h+1,PTer[w][h+1],cost,0))
          children.append([w,h+1])
     if(w-1>=0 and h-1 >=0 and abs(PTer[w-1][h-1]-z[0])<=PZ and Node_Unvisited(w-1,h-1) and Node_UnExplored(w-1,h-1)):
         nodes.append(Create_Node(w-1,h-1,PTer[w-1][h-1],cost,0))
         children.append([w-1,h-1])
     if(w-1>=0 and h+1 <= PH1 and abs(PTer[w-1][h+1]-z[0])<=PZ and Node_Unvisited(w-1,h+1) and Node_UnExplored(w-1,h+1)): 
          nodes.append(Create_Node(w-1,h+1,PTer[w-1][h+1],cost,0))
          children.append([w-1,h+1])
     if(w+1 <= PW1 and h+1 <=PH1 and abs(PTer[w+1][h+1]-z[0])<=PZ and Node_Unvisited(w+1,h+1) and Node_UnExplored(w+1,h+1)): 
          nodes.append(Create_Node(w+1,h+1,PTer[w+1][h+1],cost,0))
          children.append([w+1,h+1])
     if(w+1 <= PW1 and h-1>=0 and abs(PTer[w+1][h-1]-z[0])<=PZ and Node_Unvisited(w+1,h-1) and Node_UnExplored(w+1,h-1)):
          nodes.append(Create_Node(w+1,h-1,PTer[w+1][h-1],cost,0))
          children.append([w+1,h-1])
     path[(w,h)]=children

def Destinations():
    for x in PDest:
        if(not((x[0]>=0 and x[0]<=PW-1) and (x[1]>=0 and x[1]<=PH-1))): 
            Write_To_File(None)
            continue
        for i in range(len(nodes)):
            nodes.pop()
        for i in range(len(explored)):
            explored.pop() 
        path.clear() #clear
        Msg = Search(x)
    return(True)

def Get_Parent(dx,dy):
    d=[dx,dy]
    for i in path.items():
        if d in i[1]:
            return (i[0][0],i[0][1])

def Write_To_File(op):
        if(op is not None): 
            cnt=0
            Str=''
            for i in op:
                if(cnt==len(op)-1):
                    msg = "{}{},{}"
                    Str = msg.format(Str,str(i[0]),str(i[1]))
                else:
                    msg = "{}{},{}{}"
                    Str = msg.format(Str,str(i[0]),str(i[1]),' ')
                cnt=cnt+1
            output.write(Str+'\n')
        else:
            output.write('FAIL\n')
        return(True)
            
def Write_Path(Dx,Dy):
    Ix =Dx
    Iy=Dy
    op=[]
    while((Ix,Iy) <> (PX,PY)):
        op.append([Ix,Iy])
        Ix,Iy = Get_Parent(Ix,Iy)
    op.append([Ix,Iy])
    op.reverse()
    Write_To_File(op)
    return True

def Search(x):
    source = Initialize_Node()
    Dx,Dy=x[0],x[1]
    nodes.append(source)
    while(True):
        if (len(nodes)==0):
            Write_To_File(None)
            return(False)
        elif (nodes[0].keys()==[(Dx,Dy)]):
            Write_Path(Dx,Dy)
            return(True)
        else:
            explored.append(nodes[0])
            if(PInstr=='BFS'):
                BFSQF(nodes.pop(0))
            elif(PInstr=='UCS'):
                UCS(nodes.pop(0))
            elif(PInstr=='A*'):
                A_Star(nodes.pop(0),Dx,Dy)
            else:
                return(False)
            
def main():
    global output
    if os.path.exists("output.txt"):
        os.remove("output.txt")
    output = open("output.txt","w+")
    try:
        if(Get_Input_File()):
             Destinations()                
        else:
            Write_To_File(None)
    except:
        Write_To_File(None)
    output.close()

if __name__== "__main__":
    main()

