from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork
import functools
import datetime
import time
from path import path


class MainWindow(QtGui.QWidget):
    housedata = ""
    stationdata = ""
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()
        self.show()
        self.raise_()

    def setupUi(self):
        #self.setFixedSize(800, 500)
        hbox = QtGui.QHBoxLayout()
        self.setLayout(hbox)
        vbox = QtGui.QVBoxLayout()
        hbox.addLayout(vbox)
        label = self.label = QtGui.QLabel()
        sp = QtGui.QSizePolicy()
        sp.setVerticalStretch(0)
        label.setSizePolicy(sp)

        #left side buttons
        widget=QtGui.QWidget(self)
        QRadioButtonHouse = QtGui.QRadioButton("mark house")
        QRadioButtonStation = QtGui.QRadioButton("mark station")
        qbuttonGroup = QtGui.QButtonGroup(widget)
        qbuttonGroup.addButton(QRadioButtonHouse,1)
        qbuttonGroup.addButton(QRadioButtonStation,2)
        vbox.addWidget(widget)
        vbox.addWidget(QRadioButtonHouse)
        vbox.addWidget(QRadioButtonStation)  
        QRadioButtonHouse.setChecked(True)
        self.connect(qbuttonGroup, QtCore.SIGNAL("buttonClicked(int)"), self.changeMarker)

        saveStationbutton = QtGui.QPushButton('save station')
        vbox.addWidget(saveStationbutton)
        saveStationbutton.clicked.connect(self.file_save_station)
        saveHouseButton = QtGui.QPushButton('save house')  
        vbox.addWidget(saveHouseButton)
        saveHouseButton.clicked.connect(self.file_save_house)
        functionButton1 =  QtGui.QPushButton('FN1')
        vbox.addWidget(functionButton1)
        functionButton1.clicked.connect(self.Func1)
        functionButton2 =  QtGui.QPushButton('FN2')
        vbox.addWidget(functionButton2)
        functionButton2.clicked.connect(self.Func2)
        functionButton3 =  QtGui.QPushButton('FN3')
        vbox.addWidget(functionButton3)
        functionButton3.clicked.connect(self.Func3)
        plotRouteButton =  QtGui.QPushButton('plot route')
        vbox.addWidget(plotRouteButton)
        plotRouteButton.clicked.connect(self.plotRoute)
        clearRouteButton =  QtGui.QPushButton('clear route')
        vbox.addWidget(clearRouteButton)
        clearRouteButton.clicked.connect(self.clearRoute)
        loadFileButton =  QtGui.QPushButton('load file')
        vbox.addWidget(loadFileButton)
        loadFileButton.clicked.connect(self.loadFile)
        
        #right side view
        view = self.view = QtWebKit.QWebView()
        
        cache = QtNetwork.QNetworkDiskCache()
        cache.setCacheDirectory("cache")
        view.page().networkAccessManager().setCache(cache)
        view.page().networkAccessManager()
        
        view.page().mainFrame().addToJavaScriptWindowObject("MainWindow", self)
        view.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        view.load(QtCore.QUrl('map.html'))
        view.loadFinished.connect(self.onLoadFinished)
        view.linkClicked.connect(QtGui.QDesktopServices.openUrl)
        
        hbox.addWidget(view)

    def changeMarker(self,id):
        frame = self.view.page().mainFrame()
        if (id == 1):#house
            frame.evaluateJavaScript("changeFeature('house')")
        if(id == 2):#station
            frame.evaluateJavaScript("changeFeature('station')")
        print id 
        

    def onLoadFinished(self):
        pass
    
    def Func1(self):
        pass    

    def Func2(self):
        pass 

    def Func3(self):
        pass

    def plotRoute(self):
        frame = self.view.page().mainFrame()
        frame.evaluateJavaScript("drawRoute()")
        pass

    def clearRoute(self):
        frame = self.view.page().mainFrame()
        frame.evaluateJavaScript("clearRoute()")
        pass

    @QtCore.pyqtSlot(float, float)
    def onMapMove(self, lat, lng):
        self.label.setText('Lng: {:.5f}, Lat: {:.5f}'.format(lng, lat))


    def file_save_station(self):
        frame = self.view.page().mainFrame()
        housedata = frame.evaluateJavaScript("exportToTxt('station')").toString()
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File','map_'+str(int(time.time()))+'_station'+'.txt',selectedFilter='*.txt')
        file = open(name,'w')
        file.write(housedata)
        file.close()

    def file_save_house(self):
        frame = self.view.page().mainFrame()
        housedata = frame.evaluateJavaScript("exportToTxt('house')").toString()
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File','map_'+str(int(time.time()))+'_house'+'.txt',selectedFilter='*.txt')
        file = open(name,'w')
        file.write(housedata)
        file.close()

    def loadFile(self):
        filename = QtGui.QFileDialog.getOpenFileName()
        s = path(filename).bytes()
        s = str(s)
        lines = s.splitlines()
        script = "loadData(%s)"%lines
        print script
        frame = self.view.page().mainFrame()
        frame.evaluateJavaScript(script)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    w = MainWindow()
    app.exec_()