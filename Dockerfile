FROM "ubuntu"

#Updaten
RUN apt update -y && apt upgrade -y


# Die benötigten Systempakete installieren
RUN apt install -y tesseract-ocr libtesseract-dev python3-dev libgl1-mesa-glx git python3-pip

# pip und python fertig machen 
RUN pip3 install --upgrade pip

RUN alias python='/usr/bin/python3.6'
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1
RUN python --version

# Dateien rüberschieben
RUN mkdir /key-req
RUN mkdir /bilder
ADD ./key-req /key-req

# Python Packages installieren 
RUN pip3 install -r /key-req/requirements.txt

RUN python /key-req/key-req.py -h > /dev/null







