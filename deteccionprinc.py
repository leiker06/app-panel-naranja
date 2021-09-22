import cv2
import pytesseract
import webbrowser as wb
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import mysql.connector
from deteccion import Deteccion as D

app = Flask (__name__)

#MySQL Conection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '3lPrinc3.'
app.config['MYSQL_DB'] = 'application'
mysql = MySQL(app)

#Settings
app.secret_key = 'mysecretkey'

var_onu1046= "UN-1046"
var_onu1053= "UN-1053"
var_onu1061= "UN-1061"
var_onu1075= "UN-1075"
var_onu1832= "UN-1832"

var_onu1046_mod=var_onu1046[0:7]
var_onu1053_mod=var_onu1053[0:7]
var_onu1061_mod=var_onu1061[0:7]
var_onu1832_mod=var_onu1832[0:7]
var_onu1075_mod=var_onu1075[0:7]


lector_datos=[]

cuadro=100
anchocam,altocam=680,350

cap=cv2.VideoCapture(0)
cap.set(3,anchocam)
cap.set(4,altocam)


def text(image):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    gris=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    texto = pytesseract.image_to_string(gris,config='--psm 4')
    print(texto)
    texto1=texto.find("U")
    #print(texto1)
    texto2=texto1+7;
    #print(texto2)
    texto3 = texto[texto1:texto2]
    #print(texto3)
    if texto3 == var_onu1075_mod:
        #print("UN-1075: BUTANO - Guia de emergencia 115")
        wb.open_new(r'C:\Users\User\Documents\Tesis\documentos\Guias de Emergencia 2020\Guía 115.pdf')
        varsalida1=1075   #variable de salida para web numero ONU
        varsalida2=115    #variable de salida para web guia de emergencia
        varsalida3='Butano - Guia de Emergencia 115'

    if texto3 == var_onu1832_mod:
        print("UN-1832: Ácido sulfúrico, agotado - Guia de emergencia 137")
        wb.open_new(r'C:\Users\User\Documents\Tesis\documentos\Guias de Emergencia 2020\Guía 137.pdf')
        varsalida1=1832   #variable de salida para web numero ONU
        varsalida2=137    #variable de salida para web guia de emergencia
        varsalida3='Ácido Sulfúrico, agotado - Guia de Emergencia 137'
        
    if texto3 == var_onu1061_mod:
        print("UN-1061: Metilamina,anhidra - Guia de Emergencia 118")
        wb.open_new(r'C:\Users\User\Documents\Tesis\documentos\Guias de Emergencia 2020\Guía 137.pdf')
        varsalida1=1061   #variable de salida para web numero ONU
        varsalida2=118    #variable de salida para web guia de emergencia
        varsalida3='Metilamina,anhidra - Guia de Emergencia 118' 
    
    if texto3 == var_onu1053_mod:
        print("UN-1053: Sulfuro de Hidrogeno - Guia de Emergencia 117")
        wb.open_new(r'C:\Users\User\Documents\Tesis\documentos\Guias de Emergencia 2020\Guía 137.pdf')
        varsalida1=1053   #variable de salida para web numero ONU
        varsalida2=117    #variable de salida para web guia de emergencia
        varsalida3='Sulfuro de Hidrogeno - Guia de Emergencia 117'  
        
    if texto3 == var_onu1046_mod:
        print("UN-1053: Helio, comprimido - Guia de Emergencia 120")
        wb.open_new(r'C:\Users\User\Documents\Tesis\documentos\Guias de Emergencia 2020\Guía 137.pdf')
        varsalida1=1046   #variable de salida para web numero ONU
        varsalida2=120    #variable de salida para web guia de emergencia
        varsalida3='Helio comprimido - Guia de Emergencia 120'  
        
    return varsalida1,varsalida2,varsalida3

     
while True:
    ret,frame=cap.read()
    if ret ==False:break
    cv2.putText(frame,'Ubique el panel naranja',(150,80),cv2.FONT_HERSHEY_SIMPLEX,0.71,(255,255,0),2)
    cv2.rectangle(frame,(cuadro,cuadro),(anchocam - cuadro, altocam - cuadro),(0,0,0),2)
    x1,y1=cuadro,cuadro
    ancho,alto=(anchocam - cuadro)-x1,(altocam - cuadro) -y1
    x2,y2=x1 +ancho,y1+alto
    doc=frame[y1:y2,x1:x2]
    cv2.imwrite("image.jpg",doc)
    cv2.imshow("Lector Inteligente",frame)
    t=cv2.waitKey(1)
    if t==27:
        break
    
text(doc)
cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()

texto = D(text)  
         
class Listatextos :
    textos = []
    
    def agregartextos(self, t):
        self.textos.append(t)
    
    def mostrartextos(self):
        for t in self.textos:
           print(t)
    
lista = Listatextos()
lista.agregartextos(texto)
lista.mostrartextos()


@app.route('/')
def Index():    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM panelnaranja')
    data= cur.fetchall()    
    return render_template('index.html', codigo = data)

@app.route('/add_codigo', methods= ['POST'])
def add_codigo(): 
    numberonu,numberemergency,guideemergency = text(doc)
    print (numberonu)
    print (numberemergency) 
    print (guideemergency)   
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO panelnaranja (numberonu,numberemergency,guideemergency) VALUES(%s, %s, %s)", (numberonu,numberemergency,guideemergency))
    #sentencia = "INSERT INTO panelnaranja (numberonu,numberemergency,guideemergency) VALUES ('{0},{0},{0}')".format(numberonu,numberemergency,guideemergency)
    #cur.execute(sentencia)
    mysql.connection.commit()  
    flash('Text ONU add successfully')  
    return redirect(url_for('Index'))   

@app.route('/edit/<id>')
def get_codigo(id): 
    cur = mysql.connection.cursor()
    sentencia = "SELECT * FROM panelnaranja WHERE id = {0}".format(id)
    cur.execute(sentencia)    
    data= cur.fetchall()    
    return render_template('edit-codigo.html', codig = data[0])

@app.route('/update/<id>', methods= ['POST'])
def update_codigo(id):
    if request.method == 'POST':        
        numberonu = request.form['numberonu']
        numberemergency = request.form['numberemergency']
        guideemergency = request.form['guideemergency']
        cur = mysql.connection.cursor()
        #sentencia = "UPDATE codigo SET name = {0} WHERE id = {0}".format(id)
        #cur.execute(sentencia)
        cur.execute( """
                    UPDATE panelnaranja
                    SET numberonu = %s,
                        numberemergency = %s,
                        guideemergency = %s
                    WHERE id = %s            
                    """, (numberonu,numberemergency,guideemergency, id))  
        flash('Contact Update Successfully')
        mysql.connection.commit()  
        return redirect(url_for('Index'))
    
@app.route('/ver/<id>')
def ver_codigo(id):
    cur = mysql.connection.cursor()
    sentencia = "SELECT * FROM panelnaranja WHERE id = {0}".format(id)
    cur.execute(sentencia)    
    data= cur.fetchall()    
    for link in data:
        print(link[2])             
        if link[2] == '115':            
            return render_template('ver-codigo115.html', ver = data[0]) 
        if link[2] == '137':            
            return render_template('ver-codigo137.html', ver = data[0])
        if link[2] == '118':            
            return render_template('ver-codigo118.html', ver = data[0])
        if link[2] == '117':            
            return render_template('ver-codigo117.html', ver = data[0])
        if link[2] == '120':            
            return render_template('ver-codigo120.html', ver = data[0])  


@app.route('/delete/<string:id>')
def delete_codigo(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM panelnaranja WHERE id= {0}'.format(id))
    mysql.connection.commit()    
    flash('Text ONU removed successfully') 
    return redirect(url_for('Index'))
    

if __name__ == '__main__':    
    app.run(port = 3000, debug= True)



