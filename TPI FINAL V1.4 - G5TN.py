import sys
import os
from types import NoneType
from colorama import init, Fore, Back, Style
init()

#-- Definicion de clases 
class Particion:
  def __init__(self, idParticion, dirInicio, tamaPart, proc, idProceso, fragmentacion):
      self.idParticion = idParticion
      self.dirInicio = dirInicio
      self.tamaPart = tamaPart
      self.proc = proc
      self.idProceso = idProceso
      self.fragmentacion=fragmentacion
  def __repr__(self):
        return repr((self.idParticion, self.dirInicio, self.tamaPart, self.proc, self.idProceso, self.fragmentacion))
    
class Proceso:
    def __init__(self, idProceso, tamProceso, estado, TA, TI):
      self.idProceso = idProceso
      self.tamProceso = tamProceso
      self.estado = estado
      self.TA = TA
      self.TI = TI
    def __repr__(self):
        return repr((self.idProceso, self.tamProceso, self.estado, self.TA, self.TI))

class Cpu:
    def __init__(self, idProceso, estado, TI, procesosTerminados):
      self.idProceso = idProceso
      self.estado = estado
      self.TI = TI
      self.procesosTerminados=procesosTerminados

    # Algoritmo SRTF
    def addProceso(self):
      #carga proceso a memoria
      pos=-1
      p=0 #particion en memoria
      if self.estado==0: #0 es libre y 1 es ocupado
        minTI= sys.maxsize
        for k in particiones:
          if k.proc!=None and k.proc.TI < minTI:
            minTI=k.proc.TI
            pos=p
          elif k.proc!=None and k.proc.TI == minTI: 
            #caso que tengan mismo TI tenemos en cuenta el TA
            if k.proc.TA < particiones[pos].proc.TA:
              pos=p
          p=p+1
        if particiones[pos].proc != None:
          #carga proceso a CPU
          self.idProceso=particiones[pos].idProceso
          #Formato de salida por pantalla de ejecucion en CPU para ingreso
          vistaProceso= ' EJECUCION: Se coloca en CPU el proceso '+ str(self.idProceso)
          print(format('+','-<56')+'+')
          print('|'+'\033[1m' + format(vistaProceso, '<55') + '\033[0m'+'|')
          print(format('+','-<56')+'+\n')
          self.TI=particiones[pos].proc.TI
          self.estado=1
                
    def dropProceso(self):
      self.TI=self.TI-1
      if self.TI<=0:
        # sacamos el proceso de la lista de procesos
        for j in colaDeTrabajo:
          if j.idProceso == self.idProceso:
            colaDeTrabajo.remove(j)
            self.procesosTerminados=self.procesosTerminados +1
        # sacamos el proceso de la particion
        for i in particiones:
          if i.idProceso == self.idProceso:
            i.fragmentacion=0
            i.proc=None
            i.idProceso=0
        # ponemos la cpu en valores iniciales de nuevo
        self.estado=0
        self.idProceso=0
        self.TI=0
      elif self.TI > 0: 
        # Si el proceso en la cpu no termino, observamos si hay otro proceso que tiene un TI menor
        p=0
        for n in particiones: 
          # recorremos las particiones
          if n.proc!= None and n.proc.TI < self.TI:
            #Muestro el proceso que abandona la cpu
            vistaProceso= ' EJECUCION: Se retira del CPU el proceso '+ str(self.idProceso)
            print(format('+','-<56')+'+')
            print('|'+'\033[1m' + format(vistaProceso, '<55') + '\033[0m'+'|')
            print(format('+','-<56')+'+\n')
            #si existe un proceso en una particion, se compara el TI del proceso de cada particion con el TI del proceso que esta en la cpu
            #Si existe algun proceso en una particion con TI menor, se lo mueve a la cpu
            self.idProceso=particiones[p].idProceso
            #Formato de salida por pantalla de ejecucion en CPU para ingreso
            vistaProceso= ' EJECUCION: Se coloca en CPU el proceso '+ str(self.idProceso)
            print(format('+','-<56')+'+')
            print('|'+'\033[1m' + format(vistaProceso, '<55') + '\033[0m'+'|')
            print(format('+','-<56')+'+\n')
            self.TI=particiones[p].proc.TI
          p=p+1
        
        
#-- Definicion de funciones
def showProcesos(lista):
  m=0
  print(format('+','-<37')+'+')
  print('|'+format('TABLA DE PROCESOS','^36')+'|')
  print(format('+','-<37')+'+')
  print('|   PID   |   PT   |   TA   |   TI   |')
  print(format('+','-<37')+'+')
  init(autoreset=True) #Para que el texto de abajo no cambie de color
  print('|',Fore.CYAN + '   OS   |  100   |  NULL  |  NULL ','|')
  while m < cont:
    print('|'+ format(str(procesos[m].idProceso),'^9') +'|'+ format(str(procesos[m].tamProceso),'^8') +'|'+  format(str(procesos[m].TA), '^8') +'|'+  format(str(procesos[m].TI), '^8') +'|')
    m=m+1
  print(format('+','-<37')+'+\n')  
    
  
def showParticiones(lista):
  m=2
  print(format('+','-<56')+'+')
  print('|'+format('TABLA DE PARTICIONES', '^55')+'|')
  print(format('+','-<56')+'+')
  print('| ID PART |   TP   |  PID  |  PT  |  FRGI  | Dir Inicio |')
  print(format('+','-<56')+'+')
  init(autoreset=True) #Para que el texto de abajo no cambie de color
  print('|'+ Fore.CYAN + '    0    |  100   |  OS   | 100  |  NULL  |     0      '+ Fore.WHITE+'|')
  #Set recorrido en orden de ID particion 
  while m >= 0:
      if particiones[m].proc != None:
        showTamProc = particiones[m].proc.tamProceso
      else:
        showTamProc = 0
      print('|   ',particiones[m].idParticion,'   |'+format(str(particiones[m].tamaPart), '^8') +'|'+format(str(particiones[m].idProceso), '^7')+'|'+format(str(showTamProc), '^6')+'|'+format(str(particiones[m].fragmentacion), '^8')+'|'+format(str(particiones[m].dirInicio), '^12')+'|')
      m=m-1
  print(format('+','-<56')+'+\n')
  
  if colaLS:
    print(Style.BRIGHT + Fore.WHITE + ' Cola de Listos-Suspendidos: ', colaLS, '\n')
  else:
    print(Style.BRIGHT + Fore.WHITE + ' Cola de Listos-Suspendidos: no hay procesos suspendidos \n')
  init(autoreset=True)
  

def showTime(tiempo):
  vistaTiempo = 'TIEMPO = '+ str(tiempo) 
  print(format('+','-<79')+'+')
  print('|',format(vistaTiempo, '^76'),'|' )
  print(format('+','-<79')+'+\n')

# Gestion de cola listo-suspendido
def gestionCLS(colaDeTrabajo, colaLS):
  for i in colaDeTrabajo:
    if i not in colaLS: 
      if i.estado == 0 and tiempo > i.TA:
        colaLS.append(i)
    else:
      if i.estado == 1:
        colaLS.remove(i)
      
      
def crearProceso(idProceso):
  if idProceso==1:
    proc= Proceso(idProceso, tamProceso, 0, TA, TI)
    procesos.append(proc)
  elif idProceso==2:
    proc= Proceso(idProceso, tamProceso, 0, TA, TI)
    procesos.append(proc)
  elif idProceso==3:
    proc= Proceso(idProceso, tamProceso, 0, TA, TI)
    procesos.append(proc)
  elif idProceso==4:
    proc= Proceso(idProceso, tamProceso, 0, TA, TI)
    procesos.append(proc)
  elif idProceso==5:
    proc= Proceso(idProceso, tamProceso, 0, TA, TI)
    procesos.append(proc)
  elif idProceso==6:
    proc= Proceso(idProceso, tamProceso, 0, TA, TI)
    procesos.append(proc)
  elif idProceso==7:
    proc= Proceso(idProceso, tamProceso, 0, TA, TI)
    procesos.append(proc)
  elif idProceso==8:
    proc= Proceso(idProceso, tamProceso, 0, TA, TI)
    procesos.append(proc)
  elif idProceso==9:
    proc= Proceso(idProceso, tamProceso, 0, TA, TI)
    procesos.append(proc)
  elif idProceso==10:
    proc= Proceso(idProceso, tamProceso, 0, TA, TI)
    procesos.append(proc)

def calcTiempo (lista):
  sumaDeTiempo=0
  for i in lista:
    sumaDeTiempo= sumaDeTiempo + i.TI + i.TA
  return sumaDeTiempo


#-- BLOQUE PRINCIPAL --

# Definicion de VARIABLES
N=10 #numero maximo de procesos
band=1
idProceso=0
cont = 0 #cantidad de procesos
procesos = []
colaLS = []

#-- Bloque de ejecucion
while band != 0: 
  idProceso=idProceso+1
  b=False
  os.system('cls')
  print(format('+','-<79')+'+')
  print('|'+ format('Simulador de Procesos GRUPO 5', '^78') +'|')
  print('|'+ format('Ingrese los procesos para poder iniciarlo', '^78') +'|')
  print(format('+','-<79')+'+')
  init(autoreset=True)
  print('|' + Fore.RED + format(' Limitaciones:','<78') + Fore.WHITE+'|')
  print('|' + Fore.RED + format('       --El tamaño maximo de los procesos es de 250K','<78') + Fore.WHITE+'|')
  print('|' + Fore.RED + format('       --Solo se admiten hasta 10 procesos','<78') + Fore.WHITE+'|')
  print(format('+','-<79')+'+')
  while b==False:
    tamProceso=int(input( 'Ingrese el tamaño del proceso: '))
    if tamProceso>250:
      print(Back.WHITE + Fore.RED +'\n ERROR, el tamaño debe ser menor a 250k\n')
      os.system('pause')    
    else:
      b=True   
  TA=int(input('Ingrese el tiempo de arribo del proceso: '))   
  TI=int(input('Ingrese el tiempo de irrupcion del proceso: '))
  crearProceso(idProceso)
  cont=cont+1
  if cont < N:
    band=int(input('Desea agregar otro proceso? SI: 1 | NO: 0  '))
    os.system('cls')
    if band == 0:
      break
  else:
    print('\n ERROR, se alcanzo la maxima cantidad de procesos\n')
    band=0

showProcesos(procesos)
os.system('pause')
os.system('cls')

#-- Cola de procesos
colaDeTrabajo=sorted(procesos, key=lambda proc: proc.TA)

#--Asignacion en Memoria
frag=0 
tiempo = 0 
tiempotot= calcTiempo(procesos) 
#contiene el total de instantes o tiempos necesarios para que se ejecuten todos los procesos
particiones=[Particion(3,470,60,None,0,0),Particion(2,350,120,None,0,0), Particion(1,100,250,None,0,0)]
cpu=Cpu(0,0,0,0) #valores iniciales de la CPU

while tiempo < tiempotot:
  if cpu.estado==1:
    showTime(tiempo)
    cpu.dropProceso()
  if cpu.procesosTerminados == len(procesos): break 
  #-- Si la variable procesosTerminados = a la longitud lista de procesos ingresados, 
  #-- entonces se trataron todos los procesos, y termina el while
	
  # Gestor de COLA DE TRABAJO
  for i in colaDeTrabajo:
    if i.TA <= tiempo and i.estado==0:
      minfrag= sys.maxsize # --asigna valor maximo a la variable
      pos= -1
      p=0 # indicar la posicion de la particion
      for j in particiones:
        frag = j.tamaPart - i.tamProceso
        if frag >=0 and frag < minfrag and j.proc is None:
          # Best Fit donde mejor se acomode el proceso
          minfrag=frag
          pos=p
        # para dos procesos con mismo TA pero TI menor
        if frag >=0 and frag < minfrag and j.proc != None: 
          if j.proc.TI > i.TI:
            band=1
            minfrag=frag
            pos=p
        p=p+1
      if pos>=0:
        if band==1:
          particiones[pos].proc.estado=0
          band=0
        particiones[pos].proc=i
        particiones[pos].proc.estado=1
        # Visibilidad de Tiempo actual y proceso cargado en MP
        os.system('cls')
        showTime(tiempo)
        print(format('+','-<79')+'+')
        vistaProceso = '| EJECUCION: el proceso '+str(i.idProceso)+' de '+str(i.tamProceso)+'K, se coloca en la particion '+str(particiones[pos].idParticion)+' de tamaño '+str(particiones[pos].tamaPart)+'K.'
        print('\033[1m' + format(vistaProceso, '<79') + '\033[0m'+ '|')
        print(format('+','-<79')+'+\n')
        os.system('pause')
        os.system('cls')
        particiones[pos].idProceso=i.idProceso
        particiones[pos].fragmentacion=minfrag
        showTime(tiempo)
  
  gestionCLS(colaDeTrabajo, colaLS)
  colaLS=sorted(colaLS, key=lambda colaDeTrabajo: colaDeTrabajo.TI)
  
  if cpu.estado==0: 
    # si la cpu esta vacia agregamos un proceso
    cpu.addProceso()
    
  if cpu.idProceso==0: 
    # si el PID es igual a 0 la cpu no tiene ningun proceso, no se muestra nada, no hay acciones
    print(' ')
    # Increento el instante de tiempo
    tiempo=tiempo+1
    os.system('pause')
    os.system('cls')
  else:
    showParticiones(particiones)
    # incluimos la visibilidad de TI actual y restante 
    print(format('+','-<56')+'+')
    format(vistaProceso, '<55')
    print('|'+format('EJECUCION DE CPU' , '^55')+'|')
    print(format('+','-<56')+'+')
    print('|'+'\033[1m'+format('  --Se esta ejecutando el proceso:'+ str(cpu.idProceso), '<55')+'\033[0m'+'|')
    print('|'+'\033[1m'+format('  --Tiempo de Irrupcion actual:'+ str(cpu.TI), '<55')+'\033[0m'+'|')
    print('|'+'\033[1m'+format('  --Tiempo de Irrupcion restante:'+ str(cpu.TI-1), '<55')+'\033[0m'+'|')
    print(format('+','-<56')+'+\n')
    
    # Actualizo el TI restante del proceso cargado en Array de procesos 
    procesos[cpu.idProceso-1].TI= cpu.TI-1
    
    #TEST !!!drop at last release!!! 
    
    
    showProcesos(procesos)
    # espera a enter para continuar
    os.system('pause')
    os.system('cls')
    tiempo=tiempo+1
  
  
# saco ultimo proceso
cpu.dropProceso() 

# ultima ejecucion
os.system('cls')
init(autoreset=True) 
vistaTiempo = 'TIEMPO = '+ str(tiempo) 
print(Fore.GREEN + format('+','-<79')+'+')
print(Fore.GREEN + '|',format(vistaTiempo, '^76'),Fore.GREEN + '|' )
print(Fore.GREEN + format('+','-<79')+'+')
print(Fore.GREEN + '|',format('La Tabla de Particiones de memoria se encuentra vacía', '^76'),Fore.GREEN + '|' )
print(Fore.GREEN + '|',format('Todos los procesos fueron ejecutados exitosamente', '^76'),Fore.GREEN + '|' )
print(Fore.GREEN + format('+','-<79')+'+\n')
showParticiones(particiones)
showProcesos(procesos)
os.system('pause')
