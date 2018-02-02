import cv2
import sys

#Setando o XML de classificacao
def set_classifier(cascPath):
    cascPath = cascPath
    faceCascade = cv2.CascadeClassifier(cascPath)
    return faceCascade

def count_item(classifier):
    count_item = 0
    for x in classifier:
        count_item += 1

        if count_item >= 2:
            msg = 'Apenas uma face deve estar posicionada'                   
            return msg
            
def put_msg(msg,frame):
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (0,0,255)
    cv2.putText(frame,msg,(30,30), font, 1,(255,255,255),2)

def set_nose_point(x,y,w,h,frame):
    #Marca ponto no nariz
    face_x = (x+(w/2))
    face_y = (y+(h/2))
    #Exibe ponto do nariz
    cv2.circle(frame,(face_x,face_y), 8, (0,255,0),-1)

def reset_average(self,error):
    if error >= 20:
        self.error_face = 0
        self.average_x = 0
        self.average_y = 0
        self.count_face = 0
        self.calc_average = True
        self.flag_save = False

def set_direction(x,y,ax,ay,stop):

    if(stop == True):
        print "STOP"
    else:
        if y < ay-precision_v: print "Top Moviment"
            #else: self.status_test(False)
        elif y > ay+precision_v: print "Bottom Moviment"
            #else: self.status_test(False)
        elif x < ax-precision_h: print "Left Moviment"
            #else: self.status_test(False)
        elif x > ax+precision_h: print "Right Moviment"
            #else: self.status_test(False)


#Variaveis de controle e configuracao
calc_average = True
count_face = 0
average_x = 0
average_y = 0
precision_h = 20
precision_v = 15
sp=0

#Comeca a pegar a imagem da WebCam
video_capture = cv2.VideoCapture(0)


while True:
    #Captura e faz a leitura de cada frame em tempo real
    ret, frame = video_capture.read()
    #Espelha a imagem
    frame = cv2.flip(frame,180) 
    #Filtra a imagem em escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Seta o classificador do rosto
    faceCascade = set_classifier('haarcascade_frontalface_default.xml')

    #Seta as configuracoes do classificador do ROSTO
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=8,
        minSize=(120, 120),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    #Seta o classificador do sorriso
    smileCascade = set_classifier('haarcascade_smile.xml')

    #Desenha um retangulo no rosto encontrado
    for (x, y, w, h) in faces:
        interesting_area = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #Seta ponto no nariz
        set_nose_point(x,y,w,h,frame)
        #Conta os rostos
        msg = count_item(faces)
        #Escreve msg
        put_msg(msg,frame)
        #Define Region of Intereting do SORRISO
        roi_smile = frame[y:y+h, x:x+w]
        #Seta as configuracoes do classificador do SORRISO
        smile = smileCascade.detectMultiScale(
        roi_smile,
        scaleFactor=2.7,
        minNeighbors=20,
        minSize=(10, 10),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        #Cria retangulo do SORRISO
        for (sp,sq,sr,ss) in smile:
            cv2.rectangle(roi_smile,(sp,sq),(sp+sr,sq+ss), (0,0,255),1)

        #Verificar a parada com o sorriso
        if sp in smile:
            stop = True
        else:
            stop = False    
        #Calibrando Local do Retangulo de Referencia
        if calc_average:

            count_face += 1
            average_x += (x+(w/2))
            average_y += (y+(h/2))
            progress = (count_face/60.0) * 100


            if count_face==20:
                average_x /= count_face
                average_y /= count_face

                calc_average = False
        else:

            face_x = (x+(w/2))
            face_y = (y+(h/2))
            flag_save = True


            #Cria quadrado em volta do nariz
            cv2.rectangle(frame, (average_x-precision_h,average_y-precision_v),
                                     (average_x+precision_h,average_y+precision_v), (255,255,255))

            #Verifica a direcao do movimento do rosto
            set_direction(face_x,face_y,average_x,average_y,stop)

        
    #Exibe o frame da imagem
    cv2.imshow('Video', frame)

    #Sair do programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

