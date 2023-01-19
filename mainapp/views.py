
from django.shortcuts import render, redirect, HttpResponse
from gtts import gTTS
import string
import random
import os
import shutil



import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel, QWidget, QMenuBar, QFileDialog, QAction
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from matplotlib.figure import Figure

import pandas as pd
import networkx as nx

import collections

def Go():

    class Window(QMainWindow):

        def __init__(self, parent=None):
            super(Window, self).__init__(parent)
            # --- This is for the UI properties
            title = "Final1 Database"
            top = 400
            left = 400
            width = 840
            height = 500

            self.setWindowTitle(title)
            self.setGeometry(top, left, width, height)

            #-------------This is for Menu Bar --------------------

            Database_action = QAction("Get Data", self)
            Database_action.triggered.connect(self.getFile)

            self.menuBar = self.menuBar()

            DatabaseMenu = self.menuBar.addMenu('Database')
            DatabaseMenu.addAction(Database_action)

            #----------------------------------------------------------

            viewMenu = self.menuBar.addMenu('View')
            viewMenu.addAction('Show Tab Bar')
            viewMenu.addAction('Show All Tabs')
            viewMenu.addSeparator()
            viewMenu.addAction('List Intersections')
            viewMenu.addAction('List Streets')
            viewMenu.addAction('Enter Full Screen')
        
            #-------------------------------------------------------
            self.label = QLabel('Plot Options:',self)
            self.label.setGeometry(20,0,680,50)

            self.checkbox1= QCheckBox("Show Intersection",self)
            self.checkbox1.setGeometry(200,0,680,50)
            self.checkbox1.stateChanged.connect(self.show_intersections)

            self.checkbox2= QCheckBox("Show Roads",self)
            self.checkbox2.setGeometry(400,0,680,50)
            self.checkbox2.stateChanged.connect(self.show_roads)

            self.checkbox3= QCheckBox("Show Street Names",self)
            self.checkbox3.setGeometry(600,0,680,50)
            self.checkbox3.stateChanged.connect(self.node)

            self.figure = plt.figure(figsize=(100,100),dpi=80)

            self.canvas = FigureCanvas(self.figure)


            self.button1 = QPushButton('Export to PDF', self)
            self.button1.clicked.connect(self.savePDF)

            self.button2 = QPushButton('Export to PNG', self)
            self.button2.clicked.connect(self.savePNG)

            self.opa=0
            self.list = [1,2,3]
            self.fname = ['file1.xlsx']


            
            layout = QVBoxLayout()

            layout1= QHBoxLayout()
            layout1.setContentsMargins(0,0,0,0)
            layout1.setSpacing(20)

            layout2 = QHBoxLayout()

            layout1.addWidget(self.label)
            layout1.addWidget(self.checkbox1)
            layout1.addWidget(self.checkbox2)
            layout1.addWidget(self.checkbox3)

            layout.addLayout(layout1)

            toolbar = NavigationToolbar(self.canvas, self)
            layout.addWidget(toolbar)

            layout.addWidget(self.canvas)

            layout2.addWidget(self.button1)
            layout2.addWidget(self.button2)

            layout.addLayout(layout2)
            widget = QWidget()
            widget.setLayout(layout)
            self.setCentralWidget(widget)

            self.ax = self.figure.add_subplot(111)

        def getFile(self):

            self.fname = QFileDialog.getOpenFileName(self, "Open File","","Excel Files(*.xlsx);;CSV files (*.csv);;Python Files(*.py);;All Files (*)")

        def savePDF(self):
        
            filePath = QFileDialog.getSaveFileName(self, "Save Image", "","PDF(*.pdf);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
            self.figure.savefig(filePath[0])

        def savePNG(self):
            filePath = QFileDialog.getSaveFileName(self, "Save Image", "","PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
            self.figure.savefig(filePath[0])

            
        def inter(self):
            df = pd.read_excel(self.fname[0],'Intersections')
            dInsFeatures = pd.read_excel(self.fname[0],'InstalledFeatures')

            
            plt.margins(0.2)
            plt.tight_layout()

            intersectionIDlist = dInsFeatures['intersectionID'].tolist()
            FeaureIDlist = dInsFeatures['FeatureID'].tolist()
            gredlist = [item for item, count in collections.Counter(intersectionIDlist).items() if count > 1]
            self.gredlist = gredlist

            greenlist=[]
            redlist = []
            for i in range(len(FeaureIDlist)):
                if intersectionIDlist[i] in gredlist:
                    continue
                if FeaureIDlist[i]==2:
                    greenlist.append(intersectionIDlist[i] )
                if FeaureIDlist[i]==1:
                    redlist.append(intersectionIDlist[i] )

            self.redlist = redlist
            self.greenlist = greenlist
            self.dfID = df['ID']

            self.IDlist = df['ID'].tolist()
            Xlist = df['X'].tolist() 
            Ylist = df['Y'].tolist() 


            IntersectionsDict = dict(zip(self.IDlist,zip(Xlist,Ylist)))

            gredX=[]
            gredY=[]

            for element in gredlist:
                x = IntersectionsDict[element][0]
                gredX.append(x)
                y = IntersectionsDict[element][1]
                gredY.append(y)

            redX = []
            redY = []

            for element in redlist:
                x = IntersectionsDict[element][0]
                redX.append(x)
                y = IntersectionsDict[element][1]
                redY.append(y)

            greenX = []
            greenY = []
        
            for element in greenlist:
                x = IntersectionsDict[element][0]
                greenX.append(x)
                y = IntersectionsDict[element][1]
                greenY.append(y)

            self.gredplot = self.ax.scatter(gredX, gredY, s = 45, visible=True,color='green',alpha=1,marker="x")
            self.gredplot2 = self.ax.scatter(gredX, gredY, s = 25, visible=True,color='red',alpha=1,marker="x")
            self.redplot = self.ax.scatter(redX, redY, s = 10, linewidth = 3, visible=True,color='red',alpha=1)
            self.greenplot = self.ax.scatter(greenX, greenY, s = 25, visible=True,color='green', marker="x")
            # self.greenplot2 = self.ax.scatter(greenX, greenY, s = 25, visible=True,color='green', marker="o")
            self.canvas.draw()

        def show_intersections(self):
            if self.checkbox1.isChecked():
                self.inter()

                
            else:

                self.gredplot.set(alpha=0)
                self.gredplot2.set(alpha=0)
                self.redplot.set(alpha=0)
                self.greenplot.set(alpha=0)
                
                self.canvas.draw()
        def show_roads(self):
            if self.checkbox2.isChecked():
                self.roadsfunc(0.2)
            else:
            
                self.roadsfunc(0.001,)

        def roadsfunc(self,opa=0.3):
        
            G = nx.Graph()

            df = pd.read_excel(self.fname[0],'Intersections')
            dRoads = pd.read_excel(self.fname[0],'Roads')
            
            options = {'node_color': 'green','node_size': 1,'width': 1,'arrowstyle': '-|>','arrowsize': 20,  }

            roadX = dRoads['startNodeID'].tolist()
            roadY = dRoads['endNodeID'].tolist()
            roadlist = list(zip(roadX,roadY))

            G.add_edges_from(roadlist)

            locX = df['X'].tolist()
            locY = df['Y'].tolist()

            locationXY = list(zip(locX,locY))
            pos = {int(i):location for i, location in enumerate(locationXY)}

            for i in range(len(locationXY)):
                G.add_node(i+1,pos=locationXY[i])

            pos = nx.get_node_attributes(G,'pos')
            self.nx3=nx.draw(G,pos,**options,ax=self.ax,alpha=opa)
            self.ax.set_axis_on()
            self.ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
            self.canvas.draw()
    
        
        def node(self):
            def makenodes(opa=1):
        
                G = nx.Graph()
                df = pd.read_excel(self.fname[0],'Intersections')
                nodelist = df['ID'].tolist()
                nodelistX = df['X'].tolist()
                nodelistY = df['Y'].tolist()

                options = {'node_color': 'green','node_size': 1,'width': 1,'arrowstyle': '-|>','arrowsize': 20,  }
                    
                for i in range(len(nodelist)):
                    G.add_node(i+1,pos=(nodelistX[i],nodelistY[i]))
            
                G.add_edge(1,2)

                droads = pd.read_excel(self.fname[0],'Roads')
                startNodelist = droads['startNodeID'].tolist()
                endNodeIDlist = droads['endNodeID'].tolist()
                streetnamelist = droads['name'].tolist()

                dictionary = dict(zip(zip(startNodelist, endNodeIDlist),streetnamelist))

                pos = nx.get_node_attributes(G,'pos')
                nx.draw(G,pos,**options,ax=self.ax,alpha=opa)
                nx.draw_networkx_edge_labels(G, pos,dictionary, label_pos=0.5,font_size= 6,alpha=opa)

                self.ax.set_axis_on()
                self.ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
                self.canvas.draw()
                
            if self.checkbox3.isChecked():
                makenodes(1)
                self.show_intersections()
            
            else:
                makenodes(0)
                self.show_intersections()
            # if self.checkbox2.isChecked():
            #     self.roadsfunc(1)
            # else:
            #     self.roadsfunc(0)


    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()

#------------------------------------------------------------------------------------------


def index_page(request):
    print("hi")

    
    if request.method == "POST":
        # Go()


        letters = string.ascii_lowercase

        file_name = f"{''.join(random.choice(letters) for i in range(10))}.mp3"

        text = request.POST['text']
        tdl = request.POST['tdl']
        lang = request.POST['lang']

        tts = gTTS(text, lang=lang, tld=tdl)
        tts.save(file_name)

        dir = os.getcwd()
        full_dir = os.path.join(dir, file_name)
    
        print(dir)
        print(full_dir)

        dest = shutil.move(full_dir, os.path.join(
            dir, "mainapp/static/sound_file"))

        data = {"loc" :file_name}


        return render(request,'download.html',data)

    return render(request, 'index.html')
