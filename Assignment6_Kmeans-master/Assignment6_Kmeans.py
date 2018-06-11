import csv
import pylab as plt
import numpy as np
import uuid
from numpy import vstack,array
from scipy.cluster.vq import *
from flask import Flask,render_template,request

app = Flask(__name__,template_folder="static")
# coloumn_names = ["Postal","House","Sector","City","State","Lat","Long","Bracket","Occupancy","District"]
coloumn_names = ["time","latitude","longitude","depth","mag","magType","nst","gap","dmin","rms","id","place","depthError","magError","magNst","locationSource"]
myfile = open("edata.csv","r")
csv_reader = csv.DictReader(myfile, fieldnames=coloumn_names)
next(csv_reader)

@app.route('/')
def index():
  return render_template('index.html')

Coordlist = []
@app.route('/kmeans', methods=['GET', 'POST'])
def main():
        attribute1 = request.form['attribute1']
        attribute2 = request.form['attribute2']
        clusters = request.form['clusters']
        K_clusters = int(clusters)
        mylist = getdata(attribute1,attribute2)
        data = []
        cdist=[]
        data = array(mylist)
        cent, pts = kmeans2(data,K_clusters)

        disCluster = []
        for i in range(len(cent)):
            dc = {}
            x1 = cent[i][0]
            y1 = cent[i][1]
            x1 = float("{0:.3f}".format(x1))
            y1 = float("{0:.3f}".format(y1))
            dc['dist'] = "centroids" + str(i) + "have coordinates" + str(x1) + "," + str(y1) + ""
            disCluster.append(dc)
        #
        #     for j in range(i+1,len(cent)):
        #         dc = {}
        #         x2 = cent[j][0]
        #         y2 = cent[j][1]
        #         x2 = float("{0:.3f}".format(x2))
        #         y2 = float("{0:.3f}".format(y2))
        #         dist = np.sqrt((x1-x2)*2 + (y1-y2)*2)
        #         cdist.append(dist)
        #         dc['dist'] = "Distance between cluster " + str(i) + " and cluster " + str(j) + " is: " + str(dist)

        #         print (disCluster)
        #         print ("Distance between cluster " + str(i) + " and cluster " + str(j) + " is: " + str(dist))
        clr = ('tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:gray', 'tab:olive',
               'tab:cyan', 'tab:yellow', 'tab:maroon', 'tab:black')
        colors = ([(clr)[i] for i in pts])

        color_dict = {"blu": 0, "oran": 0, "green": 0, "red": 0, "purp": 0, "bro": 0, "gray": 0, "olive": 0, "cyan": 0,
                      "yellw": 0, "mar": 0, "black": 0}
        ptsdict = []
        for x in colors:
            if str(x) == "tab:blue":
                color_dict["blu"] += 1
            if str(x) == "tab:orange":
                color_dict["oran"] += 1
            if str(x) == "tab:green":
                color_dict["green"] += 1
            if str(x) == "tab:red":
                color_dict["red"] += 1
            if str(x) == "tab:purple":
                color_dict["purp"] += 1
            if str(x) == "tab:brown":
                color_dict["bro"] += 1
            if str(x) == "tab:gray":
                color_dict["gray"] += 1
            if str(x) == "tab:olive":
                color_dict["olive"] += 1
            if str(x) == "tab:cyan":
                color_dict["cyan"] += 1
            if str(x) == "tab:yellow":
                color_dict["yellw"] += 1
            if str(x) == "tab:maroon":
                color_dict["mar"] += 1
            if str(x) == "tab:black":
                color_dict["black"] += 1
        count = 0
        print(color_dict)
        for i in color_dict:
            if color_dict[i] == 0:
                continue
            string = str(count) + " : " + str(color_dict[i])
            ptsdict.append(string)
            print("No of points in cluster with " + str(i) + " is: " + str(color_dict[i]))
            count += 1
        plt.scatter(data[:,0],data[:,1], c=colors)
        plt.scatter(cent[:,0],cent[:,1], marker='o', s = 400, linewidths=3, c='none')
        plt.scatter(cent[:,0],cent[:,1], marker='x', s = 400, linewidths=3)

        plt.savefig("static/kmeans7.png")

        return render_template('index.html',pdict=ptsdict,disCluster = disCluster)


def getdata(attr1,attr2):
    c = 0
    for row in csv_reader:
        c += 1
        if c == 5000:
            break
        pair = []
        if row[attr1] == "":
            row[attr1] = 0
        if row[attr2] == "":
            row[attr2] = 0
        x = float(row[attr1])
        y = float(row[attr2])
        pair.append(x)
        pair.append(y)
        Coordlist.append(pair)
    return Coordlist


@app.route('/show', methods=['GET', 'POST'])
def show():
  return render_template('show.html')

@app.route('/Bargraph', methods=['GET', 'POST'])
def bargraph():
  return render_template('d3barchart.html')

@app.route('/Piegraph', methods=['GET', 'POST'])
def Piegraph():
  return render_template('d3piechart.html')



if __name__ == "__main__":
    app.run(debug=True,port=6010)