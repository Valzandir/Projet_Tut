import os
from datetime import datetime
import zipfile,rarfile
import csv
import re,time

os.chdir('C:\')

# Enlever caractères spéciaux et émojis du texte
def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        u"\u2764"
        u"\u3010"
        u"\u2192"
        u"\u300c"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

# mettre la date dans le bon format
def convert_date(timestamp):
    d = datetime.utcfromtimestamp(timestamp)
    formated_date = d.strftime('%d %b %Y')
    return formated_date


disk_drives = []
MM_Ext_1 = ['.rar']
MM_Ext_2 = ['.zip']

num = int(input("Combien de partitions avez vous ? (rentrez 1,2,3..) "))
for i in range(0,num):
    drive = input("entrez le nom de la partition "+str(i+1)+" (C,D ou autre): ")
    if len(drive) == 1:
        drive = drive.upper() + ":/"  
    else:    
        drive = drive.upper()
    disk_drives.append(drive)
file_paths_1 =[]
file_paths_2 =[]
print("----------------------------")
ch = 1

# detection des fichiers multimedia
if ch == 1:
    All_MM_files = []
    # r=>root, d=>directory, f=>fichier
    print("Veuillez patienter......\n")
    time.sleep(2)
    print("Récupération des données....")
    for dd in disk_drives:
        for r, d, f in os.walk(dd):
            for item in f:
                try:
                    
                    file_path = os.path.join(r, item)
                    
                    fileName,fileExtension = os.path.splitext(file_path)
                    fileExtension = fileExtension.lower()
                    if fileExtension in MM_Ext_1:
                        
                        file_paths_1.append(file_path)
                        

                    if fileExtension in MM_Ext_2:
                        
                        file_paths_2.append(file_path)
                        
                except:
                    continue
                    
    total_contents_rar = []
    filepath2 = []
    for i in file_paths_1 :
        file_name = i
        with rarfile.RarFile(file_name, 'r') as rf:
            files = rf.namelist()
            total_contents_rar.append(files)
            filepath2.append(file_name)

    filepath = []
    total_contents_zip = []
    for i in file_paths_2 :
        try :
            file_name = i
            with ZipFile(file_name, 'r') as zip:
                files = zip.namelist()
                total_contents_zip.append(files)
                filepath.append(file_name)

        except :
            continue
    
    MM_Ext = ['.mpg','.mpeg','.avi','.wmv','.mov','.rm','.ram','.swf','.flv','.oga','.mpu','.aac',',mpga',
        '.ogg','.webm','.mp4','.m4p','.ts','.mkv','.m4v','.amv','.mtv','.mpg4','.mpeg4','.mpgv','.vpg',
        '.ogm','.mcv','.mv4','.m4v','.qt','.mp4v','.mp2','.mpe','.mpv','.avchd','.aif','.cda','.mid',
        '.midi','.mp3','.mpa','.wav','.wma','.wpl','.vgm','.mka','.m4r','.vlc','.ac3','.m4a','.aac',
        '.aax','.alac','.aiff','.msv','.vob','.ogv','.gif','.mts','.m2v','.svi','.3gp','.flac']


    jk =-1
    file1 = []
    rarfile1 =[]
    for i in total_contents_rar :
        for j in i :
            fileName,fileExtension = os.path.splitext(j)
            fileExtension = fileExtension.lower()        
            if fileExtension in MM_Ext:
                file1.append(jk)
                rarfile1.append(j)

                

    jk =-1
    file = []
    zipfile1 =[]
    for i in total_contents_zip :
        jk = jk+1
        for j in i :
            fileName,fileExtension = os.path.splitext(j)
            fileExtension = fileExtension.lower()

            if fileExtension in MM_Ext:

                file.append(jk)
                zipfile1.append(j)
                
    size1 = []
    k=-1
    for i in file1 :
        k = k+1
        zp= rarfile.RarFile(filepath2[i-1])

        spamInfo = zp.getinfo(rarfile1[k])   
        size1.append((spamInfo.file_size)/1024)

        zp.close()


    size2 = []
    k=-1
    for i in file :
        k = k+1
        zp= zipfile.ZipFile(filepath[i])

        spamInfo = zp.getinfo(zipfile1[k])   
        size2.append((spamInfo.file_size)/1024)

        zp.close()
    
    from datetime import datetime

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    a ="Heure de création du fichier log ="+str( current_time)
    op = 'Nombre total de fichier :'+str(len(zipfile1)+len(rarfile1))

    k = -1
    b = ('taille en KO\t\t\t Nom du fichier')
    c =""
    k = -1
    for i in zipfile1 :
        k=k+1

        c = c +str(round(size1[k-1],3))+'\t\t\t'+str(i)+'\n'
    k=-1
    d =""
    for i in rarfile1 :
        k=k+1
        d = d +str(round(size1[k-1],3))+'\t\t\t'+str(i)+'\n'

    total = a+'\n'+op+'\n'+b+"\n"+c+d

    print(total)
    time.sleep(20)
    print("----------------------")
    f = open("log.txt", "w")
    f.write(total)
    f.close()

