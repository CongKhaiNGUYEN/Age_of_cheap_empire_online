
from genericpath import exists
import os
import threading

from vrai_reseau3 import variable


def handle_recv():
    input_pipe = "/home/kali/Desktop/resobetat/reseau_2/vrai_reseau3/CTOPYTHON"
    # os.mkfifo(input_pipe)
    while (True):

        fifo = os.open(input_pipe, os.O_RDONLY)
        str = os.read(fifo, 500)
        str = str.decode('utf-8')
        print("voici la valeur de stri", str)
        variable.stri = str
    # fifo.close()


def handle_send(param):
    path = "/home/kali/Desktop/resobetat/reseau_2/vrai_reseau3/PYTHONTOC"
    #os.mkfifo(path)

    fifo=open(path,'w')
    string=param
    string = string
    print("voici la chaine envoyé",string)
    fifo.write(string)
    #print('sent to c')

    #fifo.close()



