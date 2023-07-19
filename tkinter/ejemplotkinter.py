from difflib import restore
from platform import python_revision
from tkinter import *
from tkinter import messagebox
import sqlite3 as sq3

'''
====================================
          FUNCIONALIDAD
====================================
'''
# MENU
# MENU BBDD

def conectar():
    global con
    global cur
    con = sq3.connect('mi_bbdd.db')
    cur = con.cursor()
    messagebox.showinfo('STATUS','Conectado a la BBDD')

def salir():
    resp = messagebox.askquestion('CONFIRME','¿Desean salir del programa')
    if resp == 'yes':
        con.close() #cierra la conexion
        raiz.destroy() #mata la interfaz

# MENU LIMPIAR

def limpiar():
    legajo.set('')
    alumno.set('')
    email.set('')
    grado.set('')
    calificacion.set('')
    escuela.set('Seleccione')
    localidad.set('')
    provincia.set('')
    legajo_input.config(state='normal')

# MENU AYUDA
#   LICENCIA

def licencia():
    # CREATIVE COMMONS GNU GPL https://www.gnu.org/licenses/gpl-3.0.txt
    gnuglp = '''
    Demo de un sistema CRUD en Python para gestión 
    de alumnos creada en la clase de Big Data de Codo a Codo
    Copyright (C) 2022 - Ale Vedoya
    Email: alejandravedoya@hotmail.com\n=======================================
    This program is free software: you can redistribute it 
    and/or modify it under the terms of the GNU General Public 
    License as published by the Free Software Foundation, 
    either version 3 of the License, or (at your option) any 
    later version.
    This program is distributed in the hope that it will be 
    useful, but WITHOUT ANY WARRANTY; without even the 
    implied warranty of MERCHANTABILITY or FITNESS FOR A 
    PARTICULAR PURPOSE.  See the GNU General Public License 
    for more details.
    You should have received a copy of the GNU General Public 
    License along with this program.  
    If not, see <https://www.gnu.org/licenses/>.'''
    messagebox.showinfo("LICENCIA", gnuglp)

#   ACERCA DE

def acerca():
    messagebox.showinfo("ACERCA DE...", "Creado por Ale Vedoya\npara Codo a Codo 4.0 - Big Data\nMayo, 2022\nEmail: alejandravedoya@hotmail.com")

# FUNCIONES VARIAS

def buscar_escuelas(actualiza):
    con = sq3.connect('mi_bbdd.db')
    cur = con.cursor()

    if actualiza:
        cur.execute('SELECT _id, localidad, provincia FROM escuelas Where nombre = ?', (escuela.get(),))
    else:
        cur.execute('SELECT nombre FROM escuelas')

    resultado = cur.fetchall() 
    retorno = []
    for e in resultado:
        if actualiza:
            provincia.set(e[2])
            localidad.set(e[1])
        esc = e[0]
        retorno.append(esc)
    # print("Resultado: ", resultado)
    print("Retorno: ", retorno) # solo los nombres de las escuelas
    con.close()
    return retorno
    
# FUNCIONES CRUD

#CREATE
def crear():
    id_escuela = int(buscar_escuelas(True)[0])
    datos = id_escuela, legajo.get(), alumno.get(), calificacion.get(), email.get()
    cur.execute("INSERT INTO alumnos (id_escuela, legajo, nombre, nota, grado, email) VALUES (?,?,?,?,?,?)", datos)
    con.commit() # cuando voy a escribir en la bbdd se usa commit()
    messagebox.showinfo("STATUS","Registro agregado!")
    limpiar()

#READ    
def leer():
    query_leer = '''SELECT alumnos.legajo, alumnos.nombre, 
    alumnos.nota, alumnos.email, alumnos.grado, 
    escuelas.nombre, escuelas.localidad, escuelas.provincia 
    FROM alumnos INNER JOIN escuelas
    ON alumnos.id_escuela = escuelas._id 
    WHERE alumnos.legajo ='''
    cur.execute(query_leer + legajo.get())
    resultado = cur.fetchall()
    if resultado == []:
        messagebox.showerror('ERROR', 'No existe ese numero de legajo')
    else:
        # print(resultado)
        for campo in resultado:
            legajo.set(campo[0])
            alumno.set(campo[1])
            calificacion.set(campo[2])
            email.set(campo[3])
            grado.set(campo[4])
            escuela.set(campo[5])
            localidad.set(campo[6])
            provincia.set(campo[7])
            legajo_input.config(state='disabled')  # no se puede editar

#UPDATE
def actualizar():
    id_escuela = int(buscar_escuelas(True)[0])
    datos = id_escuela, alumno.get(), calificacion.get(), email.get(), grado.get()
    cur.execute("UPDATE alumnos SET id_escuela =?, nombre =?, nota =?, email =?, grado =? WHERE legajo=" + legajo.get(), datos)
    con.commit()
    messagebox.showinfo("STATUS", "Regitro actualizado")
    limpiar()

#DELETE
def borrar():
    resp = messagebox.askquestion("ELIMINAR", "¿Desea eleiminar el registro?")
    if resp == "yes":
        cur.execute("DELETE FROM alumnos WHERE legajo =" + legajo.get())
        con.commit()
        messagebox.showinfo("STATUS", "Registro eliminado")
        limpiar()

'''
====================================
         INTERFAZ GRÁFICA
====================================
'''

raiz = Tk()  # crea ventana ppal
raiz.title('GUI - Prueba v1')  # título de la ventana
raiz.geometry('500x600')

# BARRA MENU
barramenu = Menu(raiz)  # crea barra de menú
raiz.config(menu=barramenu)  # agrega el menú a la ventana ppal

bbddmenu = Menu(barramenu, tearoff=0)  # Crea submenú BBDD
bbddmenu.add_command(label='Conectar', command=conectar) # Agrega un botón al submenú BBDD
bbddmenu.add_command(label='Salir', command=salir) # Agrega un botón al submenú BBDD

limpiarmenu = Menu(barramenu, tearoff=0) # tearoff saca la barra de arriba
limpiarmenu.add_command(label='Limpiar campos')

ayudamenu = Menu(barramenu, tearoff=0)
ayudamenu.add_command(label='Licencia', command=licencia)
ayudamenu.add_command(label='Acerca de...', command=acerca)

barramenu.add_cascade(label='BBDD', menu=bbddmenu) # Crea el Botón BBDD y le asigna el submenú
barramenu.add_cascade(label='Limpiar', menu=limpiarmenu)
barramenu.add_cascade(label='Acerca de...', menu=ayudamenu)

# FRAME CAMPOS

fondo = "turquoise4"
color_fuente = "white"
framecampos = Frame(raiz)
framecampos.config(bg=fondo)
framecampos.pack(padx=30, pady=30, ipadx=40, ipady=40) # pack acomoda las cosas en una ventana sin orden específico

# Campos: creo una variable por cada campo

legajo = StringVar()
alumno = StringVar()
email = StringVar()
grado = StringVar()
calificacion = DoubleVar()
escuela = StringVar()
localidad = StringVar()
provincia = StringVar()

'''
entero = IntVar()  # Declara variable de tipo entera
flotante = DoubleVar()  # Declara variable de tipo flotante
cadena = StringVar()  # Declara variable de tipo cadena
booleano = BooleanVar()  # Declara variable de tipo booleana
'''

# siempre es textvariable aunqnue sea un numero
legajo_input = Entry(framecampos, textvariable=legajo, width=40)
legajo_input.grid(row=0, column=1, padx=10, pady=10)

alumno_input = Entry(framecampos, textvariable=alumno, width=40)
alumno_input.grid(row=1, column=1, padx=10, pady=10)

email_input = Entry(framecampos, textvariable=email, width=40)
email_input.grid(row=2, column=1, padx=10, pady=10)

grado_input = Entry(framecampos, textvariable=grado, width=40)
grado_input.grid(row=3, column=1, padx=10, pady=10)

calificacion_input = Entry(framecampos, textvariable=calificacion, width=40)
calificacion_input.grid(row=4, column=1, padx=10, pady=10)

# Obtener la lista de escuelas
escuelas = buscar_escuelas(False)

# OPCION MENU -> si quiero un menu desplegable
escuela_option = OptionMenu(framecampos, escuela,*escuelas)
escuela_option.grid(row=5, column=1, padx=10, pady=10, sticky='w')
escuela_option.config(width=34, bd=0, justify=LEFT)


localidad_input = Entry(framecampos, textvariable=localidad, state='readonly', width=40)
localidad_input.grid(row=6, column=1, padx=10, pady=10)

provincia_input = Entry(framecampos, textvariable=provincia, state='readonly', width=40)
provincia_input.grid(row=7, column=1, padx=10, pady=10)

# LABELS

'''
"STICKY"
     n
  nw   ne
w         e
  sw   se
     s
'''

# Personaliza los colores y 
def config_label(mi_label, fila):
    espaciado_label = {'column': 0, 'padx':10, 'pady':10, 'sticky':'e'}
    color_label = {'bg':fondo, 'fg':color_fuente}
    mi_label.grid(row=fila, **espaciado_label)
    mi_label.config(**color_label)

legajo_label = Label(framecampos, text='Legajo: ')
config_label(legajo_label, 0)
# legajo_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')

alumno_label = Label(framecampos, text='Alumno: ')
config_label(alumno_label, 1)
# alumno_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

email_label = Label(framecampos, text='Email: ')
config_label(email_label, 2)
# email_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')

grado_label = Label(framecampos, text='Grado: ')
config_label(grado_label, 3)
# email_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')

calificacion_label = Label(framecampos, text='Calificación: ')
config_label(calificacion_label, 4)
# calificacion_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')

escuela_label = Label(framecampos, text='Escuela: ')
config_label(escuela_label, 5)
# escuela_label.grid(row=4, column=0, padx=10, pady=10, sticky='e')

localidad_label = Label(framecampos, text='Localidad: ')
config_label(localidad_label, 6)
# localidad_label.grid(row=5, column=0, padx=10, pady=10, sticky='e')

provincia_label = Label(framecampos, text='Provincia: ')
config_label(provincia_label, 7)
# provincia_label.grid(row=6, column=0, padx=10, pady=10, sticky='e')

# FRAME BOTONERA ---> CRUD (Create, Read, Update, Delete)

framebotones = Frame(raiz)
framebotones.pack()

#CREAR
boton_crear = Button(framebotones, text='Crear', command=crear)
boton_crear.grid(row=0, column=0, padx=5, pady=10)

#LEER (buscar x nro de legajo)
boton_leer = Button(framebotones, text='Buscar', command=leer)
boton_leer.grid(row=0, column=1, padx=5, pady=10)

#ACTUALIZAR
boton_actualizar = Button(framebotones, text='Actualizar', command=actualizar)
boton_actualizar.grid(row=0, column=2, padx=5, pady=10)

#BORRAR
boton_borrar = Button(framebotones, text='Eliminar', command=borrar)
boton_borrar.grid(row=0, column=3, padx=5, pady=10)

# FRAME DEL PIE
framecopy = Frame(raiz)
framecopy.pack()

copy_label = Label(
    framecopy, text='(2022) por Ale Vedoya para Codo a Codo - Big Data')
copy_label.grid(row=0, column=0, padx=10, pady=10)


print(buscar_escuelas(False))
raiz.mainloop()  # mantiene la ventana abierta y a la espera = ÚLTIMA LÍNEA DE CÓDIGO!!!!