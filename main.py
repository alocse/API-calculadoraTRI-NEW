import sys
import math
import random
import keyboard
import string
import subprocess
import os
import time
import json
import io
import collections
habilidade=[]
nota_bin=[]
pnome_aluno=[]
pnota_aluno=[]
nota=[]
soma=[]
at=[]
pmin=[]
p=[]
par_a=[]
par_b=[]
amin=[]
bmin=[]
aux1a=[]
aux1b=[]
aux2a=[]
aux2b=[]
tot=[]
bi=[]
nome=[]
dic={}
from readchar import readchar
from random import uniform

#definicoes

def cci(a,b,k,c):
    if float(a)*(float(b)-float(k))>708:
            k1=float(c)
    else:
            k1=(1-float(c))/(1+math.exp(float(a)*(float(b)-float(k))))+float(c)
    if k1>=1:
        k1=1
    if k1<=0:
        k1=0
    return k1

#leitura de dados a partir arquivo .json
def execute(nota_json):

    json_nota = json.dumps(nota_json)
    entrada = json.loads(json_nota)

    anc1=entrada[0]['ANCORA_1']
    anc2=entrada[0]['ANCORA_2']
    disc=entrada[0]['DISCIPLINA']
    seri=entrada[0]['SERIE']
    turm=entrada[0]['TURMA']
    alternativas=5

    for i in range(len(turm)):
        pnome_aluno.append(turm[i]['ALUNO'])
        pnota_aluno.append(turm[i]['RESPOSTA'])

    quant_dados=len(turm)-1
    quant_itens=len(pnota_aluno[0])-1
    for j in range(len(turm)):
        bbin=[]
        for i in range(len(pnota_aluno[j])):bbin.append(int(pnota_aluno[j][i]==pnota_aluno[0][i]))
        nota_bin.append(bbin[:])

    nota_bin.remove(nota_bin[0])
    nome=pnome_aluno[1:]
    
    dic['DISCIPLINA']=disc
    dic['SERIE']=seri
    dic['TURMA']={}
    for i in range(quant_dados):dic['TURMA'][nome[i]]=0


    # inicializacao de variaveis
    for i in range(quant_dados):
        nota.append(0)
        habilidade.append(0)

    for i in range(quant_itens):
        pmin.append(0)
        p.append(0)
        par_a.append(0)
        par_b.append(0)
        amin.append(0)
        bmin.append(0)

    #primeira estimativa de nota
    for i in range(quant_itens):
        for j in range(quant_dados):par_b[i]=par_b[i]+(1-nota_bin[j][i])/quant_dados
    for i in range(quant_dados):
        for j in range(quant_itens):habilidade[i]=habilidade[i]+nota_bin[i][j]*par_b[j]/quant_itens

    #calculo dos parametros dos itens
    #colocacao em ordem crescente
    ee={a:b for b,a in zip(nota_bin,habilidade)}
    aux1a=sorted(habilidade)
    for i in aux1a:aux1b.append(ee[i])
    minima=aux1a[0]
    maxima=aux1a[len(aux1a)-1]
    

    #calculo das medias
    passo=10
    if quant_dados>=500:passo=50
    if quant_dados>=2000:passo=100
    if quant_dados>=10000:passo=int(math.sqrt(quant_dados))
    resto=quant_dados%passo
    quant_media=int((quant_dados-resto)/passo)
    for i in range(quant_media):tot.append(0)
    for i in range(quant_media*quant_itens):soma.append(0)
    for i in range(quant_media):
        if i==quant_media-1:
            max=passo+resto
        else:
            max=passo

        for j in range(max):
            tot[i]=tot[i]+float(aux1a[i*passo+j])/max
            for k in range(quant_itens):soma[i*quant_itens+k]=soma[i*quant_itens+k]+int(aux1b[i*passo+j][k])/max

        for j in range(quant_itens):
            if soma[i*quant_itens+j]<1/alternativas:soma[i*quant_itens+j]=1/alternativas

    #otimizacao de parametros
    cc=1/alternativas
    media=0
    desvpad=0
    for i in range(quant_dados):media=media+habilidade[i]/quant_dados
    for i in range(quant_dados):desvpad=desvpad+(habilidade[i]-media)**2
    if desvpad!=0:
        desvpad=math.sqrt(desvpad/(quant_dados-1))
    else:
        desvpad=1

    for y in range(0,1000):         
        cont=0
        bb=y                       
        aa=0.015                   
        for i in range(quant_itens):p[i]=0
        while cont<quant_media:
            cont=cont+1
            soma1=(tot[cont-1]-media)/desvpad*100+500
            for i in range(quant_itens):
                p[i]=p[i]+(soma[(cont-1)*quant_itens+i]-cci(aa,bb,soma1,cc))**2
    
        for i in range(quant_itens):
            if p[i]<pmin[i] or y==0:
                pmin[i]=p[i]
                par_a[i]=aa
                par_b[i]=bb


    #afericao das notas
    for i in range(quant_dados):
        nota1=0
        nota2=0
        for ele in range(500):     
            lutil=-500+4*ele       
            nota[i]=1
            for j in range(quant_itens):
                y=nota_bin[i][j]
                x=cci(par_a[j],par_b[j],lutil,cc)
                nota[i]=nota[i]*((x*y+(1-x)*(1-y)))**(1/quant_itens)

            nota1=nota1+nota[i]
            nota2=nota2+lutil*nota[i]

        habilidade[i]=nota2/nota1
            
#otimizacao dos parametros
    
    cc=1/alternativas
    media=0
    desvpad=0
    for i in range(quant_dados):media=media+habilidade[i]/(quant_dados)
    for i in range(quant_dados):desvpad=desvpad+(habilidade[i]-media)**2
    if desvpad!=0:
        desvpad=math.sqrt(desvpad/(quant_dados-1))
    else:
        desvpad=1
    for y in range(0,1000):     
        cont=0
        bb=y                   
        aa=0.015                         
        for i in range(quant_itens):p[i]=0
        while cont<quant_media:
            cont=cont+1
            soma1=(tot[cont-1]-media)/desvpad*100+500
            for i in range(quant_itens):
                p[i]=p[i]+(soma[(cont-1)*quant_itens+i]-cci(aa,bb,soma1,cc))**2
    
        for i in range(quant_itens):
            if p[i]<pmin[i] or y==0:
                pmin[i]=p[i]
                par_a[i]=aa
                par_b[i]=bb

    #afericao das notas
    for i in range(quant_dados):
        nota1=0
        nota2=0
        for ele in range(500): 
            lutil=-500+4*ele 
            nota[i]=1
            for j in range(quant_itens):
                y=nota_bin[i][j]
                x=cci(par_a[j],par_b[j],lutil,cc)
                nota[i]=nota[i]*((x*y+(1-x)*(1-y)))**(1/quant_itens)

            nota1=nota1+nota[i]
            nota2=nota2+lutil*nota[i]

        habilidade[i]=nota2/nota1
        
    #equalizando as notas e gravando os resultados
    media=0
    desvpad=0
    for i in range(quant_dados):media=media+habilidade[i]/(quant_dados)
    for i in range(quant_dados):desvpad=desvpad+(media-habilidade[i])**2
    if desvpad>1:
        desvpad=math.sqrt(desvpad/(quant_dados-1))
    else:
        desvpad=1
    for i in range(quant_dados):habilidade[i]=(habilidade[i]-media)/desvpad*100+500

    a=1
    b=0
    if anc1!=0 and anc2!=0:
        if par_b[0]!=par_b[1]:
            a=(anc2-anc1)/(par_b[1]-par_b[0])
        if a<=0:
            a=1
        else:
            b=anc1-a*par_b[0]

    if anc1!=0 and anc2==0:
        if par_b[0]!=0:a=anc1/par_b[0]

    for i in range(quant_dados):habilidade[i]=a*habilidade[i]+b

    #fechamento do dicionario dic e criacao do json de saida
    for i in range(quant_dados):dic['TURMA'][nome[i]]=int(10000*habilidade[i])/10000
    return dic

