#!/usr/bin/env python
# RUN: python plot_2D.py -n 12 --LHC 13 --ch 1 --type 1
import os, sys, time,math, unittest
import subprocess
import numpy as np
import ROOT
from ROOT import TLatex,TPad,TList,TH1,TH1F,TH2F,TH1D,TH2D,TFile,TTree,TCanvas,TLegend,SetOwnership,gDirectory,TObject,gStyle,gROOT,TLorentzVector,TGraph,TMultiGraph,TColor,TAttMarker,TLine,TDatime,TGaxis,TF1,THStack,TAxis,TStyle,TPaveText,TAttFill,TF2,gPad,TGaxis
from array import array
pow = ROOT.TMath.Power
import bisect
from optparse import OptionParser
parser = OptionParser()

parser.add_option("-n", type="int", dest="num", help="Number of clusters")
parser.add_option("--LHC", type="int", dest="lhc", help="pp CM energy in TeV")
parser.add_option("--ch", type="int", dest="ch", help="channel: 1 = WWbb ; 1 = aabb")
parser.add_option("--type", type="int", dest="ty", help="type: 1 = by benchmark ; 2 = by point")
(options, args) = parser.parse_args()

number = options.num
CM =options.lhc 
chan = options.ch
type= options.ty

if (chan==1) : outfolder = "llnnbb"
elif (chan==2) : outfolder = "aabb"
elif (chan==3) : outfolder = "tatabb"
elif (chan==4) : outfolder = "bbbb"
# mkdir
os.system('mkdir '+outfolder)


print "Employ %s clusters" % number
print "pp @ %s TeV" % CM
print "in the channel %s " % chan
###############################
if(type==1) : nclu =12
elif(type==2) : nclu =1507
###############################
# to round numbers
from math import log10, floor
def round_sig(x, sig=6, small_value=1.0e-9):
    return round(x, sig - int(floor(log10(max(abs(x), abs(small_value))))) - 1)
###############################
defaultStyle = TStyle("defaultStyle","Default Style")
defaultStyle.SetOptStat(0)
defaultStyle.SetPadBorderMode(1)
#defaultStyle.SetPadBorderSize(1)
defaultStyle.SetPadColor(0)
defaultStyle.SetPadTopMargin(0.1)
defaultStyle.SetPadBottomMargin(0.14)
defaultStyle.SetPadLeftMargin(0.12)
defaultStyle.SetPadRightMargin(2)
#/////// canvas /////////
defaultStyle.SetCanvasBorderMode(0)
defaultStyle.SetCanvasColor(0)
#/////// frame //////////
defaultStyle.SetFrameBorderMode(0)
defaultStyle.SetFrameBorderSize(1)
defaultStyle.SetFrameFillColor(0) 
defaultStyle.SetFrameLineColor(1)
#/////// various ////////
defaultStyle.SetTitleFillColor(0)
#defaultStyle.SetTitleX(0.2)
defaultStyle.SetTitleSize(0.06, "XYZ")    
defaultStyle.SetLabelColor(1, "XYZ")
defaultStyle.SetLabelSize(0.04, "XYZ")    
# For the axis:
#defaultStyle.SetStripDecimals(kTRUE)
defaultStyle.SetTickLength(0.03, "XYZ")
defaultStyle.SetLabelFont(62) 
defaultStyle.SetNdivisions(11, "XZ")
defaultStyle.SetNdivisions(12, "Y")
defaultStyle.cd()
###############################
warning = "CMS preliminary"
if (chan==1) :
    #    if(type==1) : warning = "WW(ll)bb = warning, limits on benchmarks!"
    #elif(type==2) : warning = "the worst limits on benchmarks applied to all points!"
    channel ="#sigma(pp #rightarrow HH #rightarrow ll#nu#nu b#bar{b})"
    lumi="L = X.x fb^{-1} (13 TeV)"
elif (chan==2) :
    #    if(type==1) : warning = "the worst limit of v1 extrapolated to all points"
    #elif(type==2) : warning = "the worst limits on benchmarks applied to all points!"
    channel ="#sigma(pp #rightarrow HH #rightarrow #gamma#gamma b#bar{b})"
    lumi="L = X.x fb^{-1} (13 TeV)"
elif (chan==3) :
    lumi="L = 2.6 fb^{-1} (13 TeV)"
    channel ="#sigma(pp #rightarrow HH #rightarrow #tau#tau b#bar{b})"
elif (chan==4) :
    #    if(type==1) : warning = "limits on SM extrapolated to all!"
    #elif(type==2) : warning = "the worst limits on benchmarks applied to all points!"
    channel ="#sigma(pp #rightarrow HH #rightarrow b#bar{b} b#bar{b})"
    lumi="L = X.x fb^{-1} (13 TeV)"
###############################
# markers
if(type==2) : leg = TLegend(0.52,0.65,0.96,0.9)
elif (type==1) : leg = TLegend(0.48,0.68,0.92,0.91)
#
if(type==1) : 
  if (chan==4 or chan==3) : leg.SetHeader("Obs. 95% CL upper limits (pb)")
  else : leg.SetHeader("Obs. 95% CL upper limits (fb)")
if(type ==2) : leg.SetHeader("Cluster")
leg.SetNColumns(4)
#leg.SetFillColor(0);
leg.SetFillStyle(0);
leg.SetBorderSize(0);
leg.SetTextSize(0.03);
# allowed/excluded
if(type==2) :  leg2 = TLegend(0.15,0.73,0.47,0.83)
elif(type==1) :  leg2 = TLegend(0.17,0.71,0.46,0.91)
leg2.SetNColumns(2)
leg2.SetFillStyle(0);
leg2.SetBorderSize(0);
leg2.SetTextSize(0.03);
# theory
if(type==2) : leg3 = TLegend(0.15,0.68,0.45,0.78)
elif(type==1) : leg3 = TLegend(0.15,0.65,0.46,0.85)
leg3.SetFillStyle(0);
leg3.SetBorderSize(0);
leg3.SetTextSize(0.03);
###############################
## 
if (chan==1) : BR = 0.0122886 # llnnbb
elif (chan==2) :BR = 0.0026 # aabb
elif (chan==3) :BR = 0.073 #2*(0.58)*(0.06272) # tatabb
elif (chan==4) :BR = (0.58)**2 # 4b
##
###############################
## read one cross section
proc = subprocess.Popen("python 5Dfunction.py --LHC 13 --kl 1 --kt 1 --c2 0 --cg 0 --c2g 0" ,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
#print proc.communicate()[0]
out = proc.stdout.read()
print float(out)*BR
##############################
## read the limits
##############################
if(type==1) :
  if (chan==1) : filne = "../../Resources/Limits/run2/nonRes-in-benchmarks/limits_WWbb_2015.txt"
  elif (chan==2) : filne = "../../Resources/Limits/run2/nonRes-in-benchmarks/limits_aabb_2015.txt"
  elif (chan==3) : filne = "../../Resources/Limits/run2/nonRes-in-benchmarks/limits_tatabb_2015.txt"
  elif (chan==4) : filne = "../../Resources/Limits/run2/nonRes-in-benchmarks/limits_bbbb_2015.txt"
elif(type==2) :
  if (chan==1) : filne = "../../Resources/Limits/run2/nonRes-in-1507-points/limits_WWbb_2015.txt"
  elif (chan==2) : filne = "../../Resources/Limits/run2/nonRes-in-1507-points/limits_aabb_2015.txt"
  elif (chan==3) : filne = "../../Resources/Limits/run2/nonRes-in-1507-points/limits_tatabb_2015.txt"
  elif (chan==4) : filne = "../../Resources/Limits/run2/nonRes-in-1507-points/limits_bbbb_2015.txt"
f = open(filne, 'r+')
lines = f.readlines() # get all lines as a list (array)
head = []
#limits = np.zeros((nclu,8))
limitsObs = np.zeros((nclu))
limitsExp = np.zeros((nclu))
counter =0
print "Reading = "+filne
print "nLimits = "+str(nclu)
# Iterate over each line, printing each line and then move to the next
for line in lines:
    #print line
    tokens = line.split()
    #print str(tokens[0])+ " limit is: " + str(tokens[2])
    #print len(tokens)
    limitsObs[counter] = float(tokens[1])
    limitsExp[counter] = float(tokens[2])
    #for lim in range(0,7) : limits[counter][lim] = float(tokens[lim])
    counter+=1
f.close()
#for ii in range(0,nclu) : print str(ii)+ " limit up to HH is: " + str((limitsExp[ii]/BR))+" (fb), and up to the final state  "+ str(round_sig(limitsExp[ii], 3))+"(fb)"
###################################
## make the 5D functions in root
##################################
number=CM
A7tev = [2.20968, 9.82091, 0.332842, 0.120743, 1.13516, -8.76709, -1.54253, 3.09385, 1.64789, -5.14831, -0.790689, 2.12522, 0.385807, -0.952469, -0.618337]
A8tev = [2.17938, 9.88152, 0.31969, 0.115609, 1.16772, -8.69692, -1.49906, 3.02278, 1.59905, -5.09201, -0.761032, 2.06131, 0.369, -0.922398, -0.604222]
A13tev = [2.09078, 10.1517, 0.282307, 0.101205, 1.33191, -8.51168, -1.37309, 2.82636, 1.45767, -4.91761, -0.675197, 1.86189, 0.321422, -0.836276, -0.568156]
A14tev = [2.07992, 10.2036, 0.277868, 0.0995436, 1.36558, -8.492, -1.35778, 2.80127, 1.44117, -4.89626, -0.664721, 1.83596, 0.315808, -0.826019, -0.564388]
A100tev = [2.17938, 9.88152, 0.31969, 0.115609, 1.16772, -8.69692, -1.49906, 3.02278, 1.59905, -5.09201, -0.761032, 2.06131, 0.369, -0.922398, -0.604222]
if number == 7 : A = A7tev 
elif number == 8 : A = A8tev
elif number == 13 : A = A13tev
elif number == 14 : A = A14tev
elif number == 100 : A = A100tev
else : print ("invalid LHC energy")
########################
# errors in normalization, NNLL
# https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHXSWGHH#Current_recommendations_for_di_H
# mh 125 GeV 

if number == 7 : 
    xs = 7.718
    scalep= 4.0
    scalem = -5.7
    PDF = 3.4
    alphas = 2.8
elif number == 8 : 
    xs = 11.18
    scalep= 4.1 
    scalem = -5.7
    PDF = 3.1
    alphas = 2.6
elif number == 13 : 
    xs = 33.45
    scalep= 4.3 
    scalem = -6.0
    PDF = 2.1
    alphas = 2.3
elif number == 14 : 
    xs = 45.05
    scalep= 4.4 
    scalem = -6.0
    PDF = 2.1
    alphas = 2.2
elif number ==100 : 
    xs = 1749
    scalep = 5.1 
    scalem = -6.6
    PDF = 1.7
    alphas = 2.1
else : print ("invalid LHC energy")
##########################
##
## function 5D
##
##########################
def fi(kl,kt,c2,cg,c2g,A0,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11,A12,A13,A14):
    result = A0*kt**4 + A1*c2**2 + (A2*kt**2 + A3*cg**2)*kl**2  + A4*c2g**2 + ( A5*c2 + A6*kt*kl )*kt**2  + (A7*kt*kl + A8*cg*kl )*c2 + A9*c2*c2g  + (A10*cg*kl + A11*c2g)*kt**2+ (A12*kl*cg + A13*c2g )*kt*kl + A14*cg*c2g*kl
    return result
if (chan==1) :
   contou = [0.5/(xs*BR),1/(xs*BR),30/(xs*BR),50/(xs*BR),100/(xs*BR),150/(xs*BR),150/(xs*BR),200/(xs*BR),300/(xs*BR)]
   contours= np.array(contou)
elif (chan==2) : 
    contou = [0.1/(xs*BR),0.2/(xs*BR),5/(xs*BR),10/(xs*BR),20/(xs*BR),20/(xs*BR),50/(xs*BR),100/(xs*BR),300/(xs*BR)]
    contours= np.array(contou)
elif (chan==3) : 
    contou = [2/(xs*BR),5/(xs*BR),10/(xs*BR),50/(xs*BR),100/(xs*BR),300/(xs*BR),500/(xs*BR),1000/(xs*BR),1500/(xs*BR)]
    contours= np.array(contou)
elif (chan==4) : 
    contou = [50/(xs*BR),100/(xs*BR),200/(xs*BR),500/(xs*BR),1000/(xs*BR),3000/(xs*BR),5000/(xs*BR),10000/(xs*BR),15000/(xs*BR)]
    contours= np.array(contou)
##########################
## (x,y) = (c2,kt) , kl =0
##########################
def fc2kt(x,par):
   kl=float(par[15])
   c2 = x[0]
   kt = x[1]
   cg = float(par[16])
   c2g = float(par[17])
   teste = (fi(kl,kt,c2,cg,c2g,float(par[0]),float(par[1]),float(par[2]),float(par[3]),float(par[4]),float(par[5]),float(par[6]),float(par[7]),float(par[8]),float(par[9]),float(par[10]),float(par[11]),float(par[12]),float(par[13]),float(par[14])))
   return teste 
parameters = np.array(A + [1] + [0] + [0] )
ff15d = TF2('fc2kt',fc2kt,-4.3,4.8,0.5,2.5,19)
#ff15d.SetParameters(parameters)
ff15d.SetParameter(0, float(A[0]))
ff15d.SetParameter(1, float(A[1]))
ff15d.SetParameter(2, float(A[2]))
ff15d.SetParameter(3, float(A[3]))
ff15d.SetParameter(4, float(A[4]))
ff15d.SetParameter(5, float(A[5]))
ff15d.SetParameter(6, float(A[6]))
ff15d.SetParameter(7, float(A[7]))
ff15d.SetParameter(8, float(A[8]))
ff15d.SetParameter(9, float(A[9]))
ff15d.SetParameter(10, float(A[10]))
ff15d.SetParameter(11, float(A[11]))
ff15d.SetParameter(12, float(A[12]))
ff15d.SetParameter(13, float(A[13]))
ff15d.SetParameter(14, float(A[14]))
ff15d.SetParameter(15, 1.0)
ff15d.SetParameter(16, 0.0)
ff15d.SetParameter(17, 0.0)
ff15d.SetTitle("")
ff15d.SetMinimum(0)
ff15d.SetLineColor(16) 
ff15d.SetLineStyle(8)
ff15d.SetContour(9,contours)    
print "RHH (SM) : " + str((ff15d.Eval(0.0,1.0))) 
##########################
## (x,y) = (c2,kt) , kl =-15
##########################
ff15dm15 = TF2('fc2kt',fc2kt,-4.3,3,0.5,2.5,19)
#ff15d.SetParameters(parameters)
ff15dm15.SetParameter(0, float(A[0]))
ff15dm15.SetParameter(1, float(A[1]))
ff15dm15.SetParameter(2, float(A[2]))
ff15dm15.SetParameter(3, float(A[3]))
ff15dm15.SetParameter(4, float(A[4]))
ff15dm15.SetParameter(5, float(A[5]))
ff15dm15.SetParameter(6, float(A[6]))
ff15dm15.SetParameter(7, float(A[7]))
ff15dm15.SetParameter(8, float(A[8]))
ff15dm15.SetParameter(9, float(A[9]))
ff15dm15.SetParameter(10, float(A[10]))
ff15dm15.SetParameter(11, float(A[11]))
ff15dm15.SetParameter(12, float(A[12]))
ff15dm15.SetParameter(13, float(A[13]))
ff15dm15.SetParameter(14, float(A[14]))
ff15dm15.SetParameter(15, -15.0)
ff15dm15.SetParameter(16, 0.0)
ff15dm15.SetParameter(17, 0.0)
ff15dm15.SetContour(9,contours) 
ff15dm15.SetTitle("")
ff15dm15.SetMinimum(0)
ff15dm15.SetLineColor(16) 
ff15dm15.SetLineStyle(8)
##########################
## (x,y) = (c2,kt) , kl =15
##########################
ff15d15 = TF2('fc2kt',fc2kt,-4.3,5.5,0.5,2.5,19)
#ff15d.SetParameters(parameters)
ff15d15.SetParameter(0, float(A[0]))
ff15d15.SetParameter(1, float(A[1]))
ff15d15.SetParameter(2, float(A[2]))
ff15d15.SetParameter(3, float(A[3]))
ff15d15.SetParameter(4, float(A[4]))
ff15d15.SetParameter(5, float(A[5]))
ff15d15.SetParameter(6, float(A[6]))
ff15d15.SetParameter(7, float(A[7]))
ff15d15.SetParameter(8, float(A[8]))
ff15d15.SetParameter(9, float(A[9]))
ff15d15.SetParameter(10, float(A[10]))
ff15d15.SetParameter(11, float(A[11]))
ff15d15.SetParameter(12, float(A[12]))
ff15d15.SetParameter(13, float(A[13]))
ff15d15.SetParameter(14, float(A[14]))
ff15d15.SetParameter(15, 15.0)
ff15d15.SetParameter(16, 0.0)
ff15d15.SetParameter(17, 0.0)
ff15d15.SetContour(9,contours) 
ff15d15.SetTitle("")
ff15d15.SetMinimum(0)
ff15d15.SetLineColor(16) 
ff15d15.SetLineStyle(8)
#print "RHH (SM) : " + str(math.exp(ff15d.Eval(0.0,1.0))) 
##########################
## (x,y) = (kl,kt)
##########################
def fklkt(x,par):
    kl= x[0]
    c2 = float(par[15])
    kt = x[1]
    cg = float(par[16])
    c2g = float(par[17])
    teste = fi(kl,kt,c2,cg,c2g,float(par[0]),float(par[1]),float(par[2]),float(par[3]),float(par[4]),float(par[5]),float(par[6]),float(par[7]),float(par[8]),float(par[9]),float(par[10]),float(par[11]),float(par[12]),float(par[13]),float(par[14]))
    result =0
    if (teste >0) : result = (teste)
    return result 
ff25d = TF2('fklkt',fklkt,-20.5,20,0.5,2.5,19)
#ff15d.SetParameters(parameters)
ff25d.SetParameter(0, float(A[0]))
ff25d.SetParameter(1, float(A[1]))
ff25d.SetParameter(2, float(A[2]))
ff25d.SetParameter(3, float(A[3]))
ff25d.SetParameter(4, float(A[4]))
ff25d.SetParameter(5, float(A[5]))
ff25d.SetParameter(6, float(A[6]))
ff25d.SetParameter(7, float(A[7]))
ff25d.SetParameter(8, float(A[8]))
ff25d.SetParameter(9, float(A[9]))
ff25d.SetParameter(10, float(A[10]))
ff25d.SetParameter(11, float(A[11]))
ff25d.SetParameter(12, float(A[12]))
ff25d.SetParameter(13, float(A[13]))
ff25d.SetParameter(14, float(A[14]))
ff25d.SetParameter(15, 0.0)
ff25d.SetParameter(16, 0.0)
ff25d.SetParameter(17, 0.0)
ff25d.SetTitle("")
ff25d.SetContour(9,contours) 
ff25d.SetMinimum(0)
ff25d.SetLineColor(16) 
ff25d.SetLineStyle(8)
print "RHH (SM) : " + str((ff25d.Eval(1.0,1.0))) 
##########################
## (x,y) = (kl,cg)
##########################
def fklcg(x,par):
    kl= x[0]
    c2 = float(par[15])
    kt = float(par[16])
    cg = x[1]
    c2g = -x[1]
    teste = fi(kl,kt,c2,cg,c2g,float(par[0]),float(par[1]),float(par[2]),float(par[3]),float(par[4]),float(par[5]),float(par[6]),float(par[7]),float(par[8]),float(par[9]),float(par[10]),float(par[11]),float(par[12]),float(par[13]),float(par[14]))
    result =0
    if (teste >0) : result = (teste)
    return result 
ff35d = TF2('fklcg',fklcg,-20.,20,-1.1,1.05,18)
#ff15d.SetParameters(parameters)
ff35d.SetParameter(0, float(A[0]))
ff35d.SetParameter(1, float(A[1]))
ff35d.SetParameter(2, float(A[2]))
ff35d.SetParameter(3, float(A[3]))
ff35d.SetParameter(4, float(A[4]))
ff35d.SetParameter(5, float(A[5]))
ff35d.SetParameter(6, float(A[6]))
ff35d.SetParameter(7, float(A[7]))
ff35d.SetParameter(8, float(A[8]))
ff35d.SetParameter(9, float(A[9]))
ff35d.SetParameter(10, float(A[10]))
ff35d.SetParameter(11, float(A[11]))
ff35d.SetParameter(12, float(A[12]))
ff35d.SetParameter(13, float(A[13]))
ff35d.SetParameter(14, float(A[14]))
ff35d.SetParameter(15, 0.0)
ff35d.SetParameter(16, 1.0)
ff35d.SetLineColor(16) 
ff35d.SetLineStyle(8)
ff35d.SetContour(9,contours) 
ff35d.SetTitle("")
ff35d.SetMinimum(0)
print "RHH (SM) : " + str((ff35d.Eval(1.0,0.0))) 
##########################
## (x,y) = (cg,c2g)
##########################
def fcgc2g(x,par):
    kl= float(par[17])
    c2 = float(par[15])
    kt = float(par[16])
    cg = x[0]
    c2g = x[1]
    teste = fi(kl,kt,c2,cg,c2g,float(par[0]),float(par[1]),float(par[2]),float(par[3]),float(par[4]),float(par[5]),float(par[6]),float(par[7]),float(par[8]),float(par[9]),float(par[10]),float(par[11]),float(par[12]),float(par[13]),float(par[14]))
    result =0
    if (teste >0) : result = (teste)
    return result 
ff45d = TF2('fcgc2g',fcgc2g,-1.35,1.1,-1.2,1.3,19)
#ff15d.SetParameters(parameters)
ff45d.SetParameter(0, float(A[0]))
ff45d.SetParameter(1, float(A[1]))
ff45d.SetParameter(2, float(A[2]))
ff45d.SetParameter(3, float(A[3]))
ff45d.SetParameter(4, float(A[4]))
ff45d.SetParameter(5, float(A[5]))
ff45d.SetParameter(6, float(A[6]))
ff45d.SetParameter(7, float(A[7]))
ff45d.SetParameter(8, float(A[8]))
ff45d.SetParameter(9, float(A[9]))
ff45d.SetParameter(10, float(A[10]))
ff45d.SetParameter(11, float(A[11]))
ff45d.SetParameter(12, float(A[12]))
ff45d.SetParameter(13, float(A[13]))
ff45d.SetParameter(14, float(A[14]))
ff45d.SetParameter(15, 0.0)
ff45d.SetParameter(16, 1.0)
ff45d.SetParameter(17, 1.0)
ff45d.SetLineColor(16) 
ff45d.SetLineStyle(8)
ff45d.SetContour(9,contours) 
ff45d.SetTitle("")
ff45d.SetMinimum(0)
print "RHH (SM) : " + str((ff45d.Eval(0.0,0.0))) 
##########################
## (x,y) = (c2,cg = -c2g) 
##########################
def fc2cg(x,par):
    kl= float(par[15])
    c2 = x[0] 
    kt = float(par[16])
    cg = x[1]
    c2g = -x[1]
    teste = fi(kl,kt,c2,cg,c2g,float(par[0]),float(par[1]),float(par[2]),float(par[3]),float(par[4]),float(par[5]),float(par[6]),float(par[7]),float(par[8]),float(par[9]),float(par[10]),float(par[11]),float(par[12]),float(par[13]),float(par[14]))
    result =0
    if (teste >0) : result = (teste)
    return result 
ff55d = TF2('fc2cg',fc2cg,-4.8,5.7,-1.1,1.05,18)
#ff15d.SetParameters(parameters)
ff55d.SetParameter(0, float(A[0]))
ff55d.SetParameter(1, float(A[1]))
ff55d.SetParameter(2, float(A[2]))
ff55d.SetParameter(3, float(A[3]))
ff55d.SetParameter(4, float(A[4]))
ff55d.SetParameter(5, float(A[5]))
ff55d.SetParameter(6, float(A[6]))
ff55d.SetParameter(7, float(A[7]))
ff55d.SetParameter(8, float(A[8]))
ff55d.SetParameter(9, float(A[9]))
ff55d.SetParameter(10, float(A[10]))
ff55d.SetParameter(11, float(A[11]))
ff55d.SetParameter(12, float(A[12]))
ff55d.SetParameter(13, float(A[13]))
ff55d.SetParameter(14, float(A[14]))
ff55d.SetParameter(15, 1.0)
ff55d.SetParameter(16, 1.0)
ff55d.SetLineColor(16) 
ff55d.SetLineStyle(8)
ff55d.SetContour(9,contours) 
ff55d.SetTitle("")
ff55d.SetMinimum(0)
print "RHH (SM) : " + str((ff55d.Eval(0.0,0.0))) 
##########################
## (x,y) = (cg,c2g), c2 =0.5
##########################
def fcgc2g(x,par):
    kl= float(par[17])
    c2 = float(par[15])
    kt = float(par[16])
    cg = x[0]
    c2g = x[1]
    teste = fi(kl,kt,c2,cg,c2g,float(par[0]),float(par[1]),float(par[2]),float(par[3]),float(par[4]),float(par[5]),float(par[6]),float(par[7]),float(par[8]),float(par[9]),float(par[10]),float(par[11]),float(par[12]),float(par[13]),float(par[14]))
    result =0
    if (teste >0) : result = (teste)
    return result 
ff65d = TF2('fcgc2g',fcgc2g,-1.35,1.1,-1.2,1.3,19)
#ff15d.SetParameters(parameters)
ff65d.SetParameter(0, float(A[0]))
ff65d.SetParameter(1, float(A[1]))
ff65d.SetParameter(2, float(A[2]))
ff65d.SetParameter(3, float(A[3]))
ff65d.SetParameter(4, float(A[4]))
ff65d.SetParameter(5, float(A[5]))
ff65d.SetParameter(6, float(A[6]))
ff65d.SetParameter(7, float(A[7]))
ff65d.SetParameter(8, float(A[8]))
ff65d.SetParameter(9, float(A[9]))
ff65d.SetParameter(10, float(A[10]))
ff65d.SetParameter(11, float(A[11]))
ff65d.SetParameter(12, float(A[12]))
ff65d.SetParameter(13, float(A[13]))
ff65d.SetParameter(14, float(A[14]))
ff65d.SetParameter(15, 0.5)
ff65d.SetParameter(16, 1.0)
ff65d.SetParameter(17, 1.0)
ff65d.SetLineColor(16) 
ff65d.SetLineStyle(8)
ff65d.SetContour(9,contours) 
ff65d.SetTitle("")
ff65d.SetMinimum(0)
##########################
## (x,y) = (c2,kt) , kl =-12.5
##########################
ff15dm12p5 = TF2('fc2kt',fc2kt,-4.3,3,0.5,2.5,19)
#ff15d.SetParameters(parameters)
ff15dm12p5.SetParameter(0, float(A[0]))
ff15dm12p5.SetParameter(1, float(A[1]))
ff15dm12p5.SetParameter(2, float(A[2]))
ff15dm12p5.SetParameter(3, float(A[3]))
ff15dm12p5.SetParameter(4, float(A[4]))
ff15dm12p5.SetParameter(5, float(A[5]))
ff15dm12p5.SetParameter(6, float(A[6]))
ff15dm12p5.SetParameter(7, float(A[7]))
ff15dm12p5.SetParameter(8, float(A[8]))
ff15dm12p5.SetParameter(9, float(A[9]))
ff15dm12p5.SetParameter(10, float(A[10]))
ff15dm12p5.SetParameter(11, float(A[11]))
ff15dm12p5.SetParameter(12, float(A[12]))
ff15dm12p5.SetParameter(13, float(A[13]))
ff15dm12p5.SetParameter(14, float(A[14]))
ff15dm12p5.SetParameter(15, -12.5)
ff15dm12p5.SetParameter(16, 0.0)
ff15dm12p5.SetParameter(17, 0.0)
ff15dm12p5.SetContour(9,contours) 
ff15dm12p5.SetTitle("")
ff15dm12p5.SetMinimum(0)
ff15dm12p5.SetLineColor(16) 
ff15dm12p5.SetLineStyle(8)
##########################
## (x,y) = (c2,kt) , kl =12.5
##########################
ff15d12p5 = TF2('fc2kt',fc2kt,-4.3,5.5,0.5,2.5,19)
#ff15d.SetParameters(parameters)
ff15d12p5.SetParameter(0, float(A[0]))
ff15d12p5.SetParameter(1, float(A[1]))
ff15d12p5.SetParameter(2, float(A[2]))
ff15d12p5.SetParameter(3, float(A[3]))
ff15d12p5.SetParameter(4, float(A[4]))
ff15d12p5.SetParameter(5, float(A[5]))
ff15d12p5.SetParameter(6, float(A[6]))
ff15d12p5.SetParameter(7, float(A[7]))
ff15d12p5.SetParameter(8, float(A[8]))
ff15d12p5.SetParameter(9, float(A[9]))
ff15d12p5.SetParameter(10, float(A[10]))
ff15d12p5.SetParameter(11, float(A[11]))
ff15d12p5.SetParameter(12, float(A[12]))
ff15d12p5.SetParameter(13, float(A[13]))
ff15d12p5.SetParameter(14, float(A[14]))
ff15d12p5.SetParameter(15, 12.5)
ff15d12p5.SetParameter(16, 0.0)
ff15d12p5.SetParameter(17, 0.0)
ff15d12p5.SetContour(9,contours) 
ff15d12p5.SetTitle("")
ff15d12p5.SetMinimum(0)
ff15d12p5.SetLineColor(16) 
ff15d12p5.SetLineStyle(8)
##########################
## (x,y) = (c2,kt) , kl =-10.0
##########################
ff15dm10p0 = TF2('fc2kt',fc2kt,-4.3,3,0.5,2.5,19)
#ff15d.SetParameters(parameters)
ff15dm10p0.SetParameter(0, float(A[0]))
ff15dm10p0.SetParameter(1, float(A[1]))
ff15dm10p0.SetParameter(2, float(A[2]))
ff15dm10p0.SetParameter(3, float(A[3]))
ff15dm10p0.SetParameter(4, float(A[4]))
ff15dm10p0.SetParameter(5, float(A[5]))
ff15dm10p0.SetParameter(6, float(A[6]))
ff15dm10p0.SetParameter(7, float(A[7]))
ff15dm10p0.SetParameter(8, float(A[8]))
ff15dm10p0.SetParameter(9, float(A[9]))
ff15dm10p0.SetParameter(10, float(A[10]))
ff15dm10p0.SetParameter(11, float(A[11]))
ff15dm10p0.SetParameter(12, float(A[12]))
ff15dm10p0.SetParameter(13, float(A[13]))
ff15dm10p0.SetParameter(14, float(A[14]))
ff15dm10p0.SetParameter(15, -10.0)
ff15dm10p0.SetParameter(16, 0.0)
ff15dm10p0.SetParameter(17, 0.0)
ff15dm10p0.SetContour(9,contours) 
ff15dm10p0.SetTitle("")
ff15dm10p0.SetMinimum(0)
ff15dm10p0.SetLineColor(16) 
ff15dm10p0.SetLineStyle(8)
##########################
## (x,y) = (c2,kt) , kl =10.0
##########################
ff15d10p0 = TF2('fc2kt',fc2kt,-4.3,5.5,0.5,2.5,19)
#ff15d.SetParameters(parameters)
ff15d10p0.SetParameter(0, float(A[0]))
ff15d10p0.SetParameter(1, float(A[1]))
ff15d10p0.SetParameter(2, float(A[2]))
ff15d10p0.SetParameter(3, float(A[3]))
ff15d10p0.SetParameter(4, float(A[4]))
ff15d10p0.SetParameter(5, float(A[5]))
ff15d10p0.SetParameter(6, float(A[6]))
ff15d10p0.SetParameter(7, float(A[7]))
ff15d10p0.SetParameter(8, float(A[8]))
ff15d10p0.SetParameter(9, float(A[9]))
ff15d10p0.SetParameter(10, float(A[10]))
ff15d10p0.SetParameter(11, float(A[11]))
ff15d10p0.SetParameter(12, float(A[12]))
ff15d10p0.SetParameter(13, float(A[13]))
ff15d10p0.SetParameter(14, float(A[14]))
ff15d10p0.SetParameter(15, 10.0)
ff15d10p0.SetParameter(16, 0.0)
ff15d10p0.SetParameter(17, 0.0)
ff15d10p0.SetContour(9,contours) 
ff15d10p0.SetTitle("")
ff15d10p0.SetMinimum(0)
ff15d10p0.SetLineColor(16) 
ff15d10p0.SetLineStyle(8)
##########################
## (x,y) = (c2,kt) , kl =-7.5
##########################
ff15dm7p5 = TF2('fc2kt',fc2kt,-4.3,3,0.5,2.5,19)
#ff15d.SetParameters(parameters)
ff15dm7p5.SetParameter(0, float(A[0]))
ff15dm7p5.SetParameter(1, float(A[1]))
ff15dm7p5.SetParameter(2, float(A[2]))
ff15dm7p5.SetParameter(3, float(A[3]))
ff15dm7p5.SetParameter(4, float(A[4]))
ff15dm7p5.SetParameter(5, float(A[5]))
ff15dm7p5.SetParameter(6, float(A[6]))
ff15dm7p5.SetParameter(7, float(A[7]))
ff15dm7p5.SetParameter(8, float(A[8]))
ff15dm7p5.SetParameter(9, float(A[9]))
ff15dm7p5.SetParameter(10, float(A[10]))
ff15dm7p5.SetParameter(11, float(A[11]))
ff15dm7p5.SetParameter(12, float(A[12]))
ff15dm7p5.SetParameter(13, float(A[13]))
ff15dm7p5.SetParameter(14, float(A[14]))
ff15dm7p5.SetParameter(15, -7.5)
ff15dm7p5.SetParameter(16, 0.0)
ff15dm7p5.SetParameter(17, 0.0)
ff15dm7p5.SetContour(9,contours) 
ff15dm7p5.SetTitle("")
ff15dm7p5.SetMinimum(0)
ff15dm7p5.SetLineColor(16) 
ff15dm7p5.SetLineStyle(8)
##########################
## (x,y) = (c2,kt) , kl =7.5
##########################
ff15d7p5 = TF2('fc2kt',fc2kt,-4.3,5.5,0.5,2.5,19)
#ff15d.SetParameters(parameters)
ff15d7p5.SetParameter(0, float(A[0]))
ff15d7p5.SetParameter(1, float(A[1]))
ff15d7p5.SetParameter(2, float(A[2]))
ff15d7p5.SetParameter(3, float(A[3]))
ff15d7p5.SetParameter(4, float(A[4]))
ff15d7p5.SetParameter(5, float(A[5]))
ff15d7p5.SetParameter(6, float(A[6]))
ff15d7p5.SetParameter(7, float(A[7]))
ff15d7p5.SetParameter(8, float(A[8]))
ff15d7p5.SetParameter(9, float(A[9]))
ff15d7p5.SetParameter(10, float(A[10]))
ff15d7p5.SetParameter(11, float(A[11]))
ff15d7p5.SetParameter(12, float(A[12]))
ff15d7p5.SetParameter(13, float(A[13]))
ff15d7p5.SetParameter(14, float(A[14]))
ff15d7p5.SetParameter(15, 7.5)
ff15d7p5.SetParameter(16, 0.0)
ff15d7p5.SetParameter(17, 0.0)
ff15d7p5.SetContour(9,contours) 
ff15d7p5.SetTitle("")
ff15d7p5.SetMinimum(0)
ff15d7p5.SetLineColor(16) 
ff15d7p5.SetLineStyle(8)
##########################
## (x,y) = (c2,kt) , kl =-5.0
##########################
ff15dm5p0 = TF2('fc2kt',fc2kt,-4.3,3,0.5,2.5,19)
#ff15d.SetParameters(parameters)
ff15dm5p0.SetParameter(0, float(A[0]))
ff15dm5p0.SetParameter(1, float(A[1]))
ff15dm5p0.SetParameter(2, float(A[2]))
ff15dm5p0.SetParameter(3, float(A[3]))
ff15dm5p0.SetParameter(4, float(A[4]))
ff15dm5p0.SetParameter(5, float(A[5]))
ff15dm5p0.SetParameter(6, float(A[6]))
ff15dm5p0.SetParameter(7, float(A[7]))
ff15dm5p0.SetParameter(8, float(A[8]))
ff15dm5p0.SetParameter(9, float(A[9]))
ff15dm5p0.SetParameter(10, float(A[10]))
ff15dm5p0.SetParameter(11, float(A[11]))
ff15dm5p0.SetParameter(12, float(A[12]))
ff15dm5p0.SetParameter(13, float(A[13]))
ff15dm5p0.SetParameter(14, float(A[14]))
ff15dm5p0.SetParameter(15, -5.0)
ff15dm5p0.SetParameter(16, 0.0)
ff15dm5p0.SetParameter(17, 0.0)
ff15dm5p0.SetContour(9,contours) 
ff15dm5p0.SetTitle("")
ff15dm5p0.SetMinimum(0)
ff15dm5p0.SetLineColor(16) 
ff15dm5p0.SetLineStyle(8)
##########################
## (x,y) = (c2,kt) , kl =5.0
##########################
ff15d5p0 = TF2('fc2kt',fc2kt,-4.3,5.5,0.5,2.5,19)
#ff15d.SetParameters(parameters)
ff15d5p0.SetParameter(0, float(A[0]))
ff15d5p0.SetParameter(1, float(A[1]))
ff15d5p0.SetParameter(2, float(A[2]))
ff15d5p0.SetParameter(3, float(A[3]))
ff15d5p0.SetParameter(4, float(A[4]))
ff15d5p0.SetParameter(5, float(A[5]))
ff15d5p0.SetParameter(6, float(A[6]))
ff15d5p0.SetParameter(7, float(A[7]))
ff15d5p0.SetParameter(8, float(A[8]))
ff15d5p0.SetParameter(9, float(A[9]))
ff15d5p0.SetParameter(10, float(A[10]))
ff15d5p0.SetParameter(11, float(A[11]))
ff15d5p0.SetParameter(12, float(A[12]))
ff15d5p0.SetParameter(13, float(A[13]))
ff15d5p0.SetParameter(14, float(A[14]))
ff15d5p0.SetParameter(15, 5.0)
ff15d5p0.SetParameter(16, 0.0)
ff15d5p0.SetParameter(17, 0.0)
ff15d5p0.SetContour(9,contours) 
ff15d5p0.SetTitle("")
ff15d5p0.SetMinimum(0)
ff15d5p0.SetLineColor(16) 
ff15d5p0.SetLineStyle(8)
##########################
## (x,y) = (c2,kt) , kl =-3.5
##########################
ff15dm3p5 = TF2('fc2kt',fc2kt,-4.3,3,0.5,2.5,19)
#ff15d.SetParameters(parameters)
ff15dm3p5.SetParameter(0, float(A[0]))
ff15dm3p5.SetParameter(1, float(A[1]))
ff15dm3p5.SetParameter(2, float(A[2]))
ff15dm3p5.SetParameter(3, float(A[3]))
ff15dm3p5.SetParameter(4, float(A[4]))
ff15dm3p5.SetParameter(5, float(A[5]))
ff15dm3p5.SetParameter(6, float(A[6]))
ff15dm3p5.SetParameter(7, float(A[7]))
ff15dm3p5.SetParameter(8, float(A[8]))
ff15dm3p5.SetParameter(9, float(A[9]))
ff15dm3p5.SetParameter(10, float(A[10]))
ff15dm3p5.SetParameter(11, float(A[11]))
ff15dm3p5.SetParameter(12, float(A[12]))
ff15dm3p5.SetParameter(13, float(A[13]))
ff15dm3p5.SetParameter(14, float(A[14]))
ff15dm3p5.SetParameter(15, -3.5)
ff15dm3p5.SetParameter(16, 0.0)
ff15dm3p5.SetParameter(17, 0.0)
ff15dm3p5.SetContour(9,contours) 
ff15dm3p5.SetTitle("")
ff15dm3p5.SetMinimum(0)
ff15dm3p5.SetLineColor(16) 
ff15dm3p5.SetLineStyle(8)
##########################
## (x,y) = (c2,kt) , kl =3.5
##########################
ff15d3p5 = TF2('fc2kt',fc2kt,-4.3,5.5,0.5,2.5,19)
#ff15d.SetParameters(parameters)
ff15d3p5.SetParameter(0, float(A[0]))
ff15d3p5.SetParameter(1, float(A[1]))
ff15d3p5.SetParameter(2, float(A[2]))
ff15d3p5.SetParameter(3, float(A[3]))
ff15d3p5.SetParameter(4, float(A[4]))
ff15d3p5.SetParameter(5, float(A[5]))
ff15d3p5.SetParameter(6, float(A[6]))
ff15d3p5.SetParameter(7, float(A[7]))
ff15d3p5.SetParameter(8, float(A[8]))
ff15d3p5.SetParameter(9, float(A[9]))
ff15d3p5.SetParameter(10, float(A[10]))
ff15d3p5.SetParameter(11, float(A[11]))
ff15d3p5.SetParameter(12, float(A[12]))
ff15d3p5.SetParameter(13, float(A[13]))
ff15d3p5.SetParameter(14, float(A[14]))
ff15d3p5.SetParameter(15, 3.5)
ff15d3p5.SetParameter(16, 0.0)
ff15d3p5.SetParameter(17, 0.0)
ff15d3p5.SetContour(9,contours) 
ff15d3p5.SetTitle("")
ff15d3p5.SetMinimum(0)
ff15d3p5.SetLineColor(16) 
ff15d3p5.SetLineStyle(8)
##########################
## (x,y) = (c2,kt) , kl =-2.4
##########################
ff15dm2p4 = TF2('fc2kt',fc2kt,-4.3,3,0.5,2.5,19)
#ff15d.SetParameters(parameters)
ff15dm2p4.SetParameter(0, float(A[0]))
ff15dm2p4.SetParameter(1, float(A[1]))
ff15dm2p4.SetParameter(2, float(A[2]))
ff15dm2p4.SetParameter(3, float(A[3]))
ff15dm2p4.SetParameter(4, float(A[4]))
ff15dm2p4.SetParameter(5, float(A[5]))
ff15dm2p4.SetParameter(6, float(A[6]))
ff15dm2p4.SetParameter(7, float(A[7]))
ff15dm2p4.SetParameter(8, float(A[8]))
ff15dm2p4.SetParameter(9, float(A[9]))
ff15dm2p4.SetParameter(10, float(A[10]))
ff15dm2p4.SetParameter(11, float(A[11]))
ff15dm2p4.SetParameter(12, float(A[12]))
ff15dm2p4.SetParameter(13, float(A[13]))
ff15dm2p4.SetParameter(14, float(A[14]))
ff15dm2p4.SetParameter(15, -2.4)
ff15dm2p4.SetParameter(16, 0.0)
ff15dm2p4.SetParameter(17, 0.0)
ff15dm2p4.SetContour(9,contours) 
ff15dm2p4.SetTitle("")
ff15dm2p4.SetMinimum(0)
ff15dm2p4.SetLineColor(16) 
ff15dm2p4.SetLineStyle(8)
##########################
## (x,y) = (c2,kt) , kl =2.4
##########################
ff15d2p4 = TF2('fc2kt',fc2kt,-5,5.5,0.5,2.5,19)
#ff15d.SetParameters(parameters)
ff15d2p4.SetParameter(0, float(A[0]))
ff15d2p4.SetParameter(1, float(A[1]))
ff15d2p4.SetParameter(2, float(A[2]))
ff15d2p4.SetParameter(3, float(A[3]))
ff15d2p4.SetParameter(4, float(A[4]))
ff15d2p4.SetParameter(5, float(A[5]))
ff15d2p4.SetParameter(6, float(A[6]))
ff15d2p4.SetParameter(7, float(A[7]))
ff15d2p4.SetParameter(8, float(A[8]))
ff15d2p4.SetParameter(9, float(A[9]))
ff15d2p4.SetParameter(10, float(A[10]))
ff15d2p4.SetParameter(11, float(A[11]))
ff15d2p4.SetParameter(12, float(A[12]))
ff15d2p4.SetParameter(13, float(A[13]))
ff15d2p4.SetParameter(14, float(A[14]))
ff15d2p4.SetParameter(15, 2.4)
ff15d2p4.SetParameter(16, 0.0)
ff15d2p4.SetParameter(17, 0.0)
ff15d2p4.SetContour(9,contours) 
ff15d2p4.SetTitle("")
ff15d2p4.SetMinimum(0)
ff15d2p4.SetLineColor(16) 
ff15d2p4.SetLineStyle(8)
##########################
## declare histos 
##########################
nclu=12

Histoc2ktm15 = [None]*nclu 
Histoc2ktm15Exclu = [None]*nclu 
Histoc2kt15 = [None]*nclu 
Histoc2kt15Exclu = [None]*nclu 
Histoc2ktm12p5 = [None]*nclu 
Histoc2ktm12p5Exclu = [None]*nclu 
Histoc2kt12p5 = [None]*nclu 
Histoc2kt12p5Exclu = [None]*nclu 
Histoc2ktm10p0 = [None]*nclu 
Histoc2ktm10p0Exclu = [None]*nclu 
Histoc2kt10p0 = [None]*nclu 
Histoc2kt10p0Exclu = [None]*nclu 
Histoc2ktm7p5 = [None]*nclu 
Histoc2ktm7p5Exclu = [None]*nclu 
Histoc2kt7p5 = [None]*nclu 
Histoc2kt7p5Exclu = [None]*nclu 
Histoc2ktm5p0 = [None]*nclu 
Histoc2ktm5p0Exclu = [None]*nclu 
Histoc2kt5p0 = [None]*nclu 
Histoc2kt5p0Exclu = [None]*nclu 
Histoc2ktm3p5 = [None]*nclu 
Histoc2ktm3p5Exclu = [None]*nclu 
Histoc2kt3p5 = [None]*nclu 
Histoc2kt3p5Exclu = [None]*nclu 
Histoc2ktm2p4 = [None]*nclu 
Histoc2ktm2p4Exclu = [None]*nclu 
Histoc2kt2p4 = [None]*nclu 
Histoc2kt2p4Exclu = [None]*nclu 
#
Histoc2kt = [None]*nclu 
Histoc2ktExclu = [None]*nclu 
Histoklkt = [None]*nclu 
HistoklktExclu = [None]*nclu 
Histoklcg = [None]*nclu 
HistoklcgExclu = [None]*nclu 
Histocgc2g = [None]*nclu 
Histocgc2gExclu = [None]*nclu 
Histoc2cg = [None]*nclu 
Histoc2cgExclu = [None]*nclu 
Histocgc2g05 = [None]*nclu 
Histocgc2g05Exclu = [None]*nclu  
#
mc = [221, 1, 208, 205, 99, 8, 209, 209, 3, 28, 30, 221, 38, 40, 41, 44, 45, 46, 48]
mt= [34,34,22,20,34, 34,23,20,22,23,23,23]
mtexclu= [28,28,26,24,28, 28,32,24,26,32,32,32]
tick=[0.5,1,1.5,2,2.5]
ticks= np.array(tick)
for ii in range(0,nclu):
    #
    Histoc2kt[ii] = TH2D("","", 500,-4.8,3.5,500,0.3,3.8 )
    Histoc2kt[ii].GetYaxis().SetTitle(" ")
    Histoc2kt[ii].GetXaxis().SetTitle("c_{2}")
    #    Histoc2kt[ii].GetXaxis().SetLabel(ticks)
    Histoc2kt[ii].SetLineColor(mc[ii])
    Histoc2kt[ii].SetMarkerColor(mc[ii])
    Histoc2kt[ii].SetMarkerStyle(mt[ii])
    Histoc2kt[ii].SetMarkerSize(2.0)
    #    
    Histoc2ktExclu[ii] = TH2D("","", 500,-3.5,3.5,500,0.3,2.8 )
    Histoc2ktExclu[ii].GetYaxis().SetTitle(" ")
    Histoc2ktExclu[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2ktExclu[ii].SetLineColor(mc[ii])
    Histoc2ktExclu[ii].SetMarkerColor(mc[ii])
    Histoc2ktExclu[ii].SetMarkerStyle(mtexclu[ii])
    Histoc2ktExclu[ii].SetMarkerSize(2.0)
    # kl = -15
    Histoc2ktm15[ii] = TH2D("","", 500,-4.8,3.5,500,0.3,3.8 )
    Histoc2ktm15[ii].GetYaxis().SetTitle(" ")
    Histoc2ktm15[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2ktm15[ii].SetLineColor(mc[ii])
    Histoc2ktm15[ii].SetMarkerColor(mc[ii])
    Histoc2ktm15[ii].SetMarkerStyle(mt[ii])
    Histoc2ktm15[ii].SetMarkerSize(2.0)
    #    
    Histoc2ktm15Exclu[ii] = TH2D("","", 500,-3.5,3.5,500,0.3,2.8 )
    Histoc2ktm15Exclu[ii].GetYaxis().SetTitle(" ")
    Histoc2ktm15Exclu[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2ktm15Exclu[ii].SetLineColor(mc[ii])
    Histoc2ktm15Exclu[ii].SetMarkerColor(mc[ii])
    Histoc2ktm15Exclu[ii].SetMarkerStyle(mtexclu[ii])
    Histoc2ktm15Exclu[ii].SetMarkerSize(2.0)
    # kl = 15
    Histoc2kt15[ii] = TH2D("","", 500,-3.8,5.5,500,0.3,3.8 )
    Histoc2kt15[ii].GetYaxis().SetTitle(" ")
    Histoc2kt15[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2kt15[ii].SetLineColor(mc[ii])
    Histoc2kt15[ii].SetMarkerColor(mc[ii])
    Histoc2kt15[ii].SetMarkerStyle(mt[ii])
    Histoc2kt15[ii].SetMarkerSize(2.0)
    #    
    Histoc2kt15Exclu[ii] = TH2D("","", 500,-3.5,3.5,500,0.3,2.8 )
    Histoc2kt15Exclu[ii].GetYaxis().SetTitle(" ")
    Histoc2kt15Exclu[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2kt15Exclu[ii].SetLineColor(mc[ii])
    Histoc2kt15Exclu[ii].SetMarkerColor(mc[ii])
    Histoc2kt15Exclu[ii].SetMarkerStyle(mtexclu[ii])
    Histoc2kt15Exclu[ii].SetMarkerSize(2.0)
    #
    Histoklkt[ii] = TH2D("","", 500,-21,16.5,800,0.3,3.8  )
    Histoklkt[ii].GetYaxis().SetTitle(" ")
    Histoklkt[ii].GetXaxis().SetTitle("#kappa_{#lambda}")
    Histoklkt[ii].SetLineColor(mc[ii])
    Histoklkt[ii].SetMarkerColor(mc[ii])
    Histoklkt[ii].SetMarkerStyle(mt[ii])
    Histoklkt[ii].SetMarkerSize(2.0)
    #    
    HistoklktExclu[ii] = TH2D("","", 500,-24,16.5,800,0.0,3.8 )
    HistoklktExclu[ii].GetYaxis().SetTitle(" ")
    HistoklktExclu[ii].GetXaxis().SetTitle("#kappa_{#lambda}")
    HistoklktExclu[ii].SetLineColor(mc[ii])
    HistoklktExclu[ii].SetMarkerColor(mc[ii])
    HistoklktExclu[ii].SetMarkerStyle(mtexclu[ii])
    HistoklktExclu[ii].SetMarkerSize(2.0)
    #
    Histoklcg[ii] = TH2D("","", 500,-20,16.5,500,-1.1,2.2  )
    Histoklcg[ii].GetYaxis().SetTitle(" ")
    Histoklcg[ii].GetXaxis().SetTitle("#kappa_{#lambda}")
    Histoklcg[ii].SetLineColor(mc[ii])
    Histoklcg[ii].SetMarkerColor(mc[ii])
    Histoklcg[ii].SetMarkerStyle(mt[ii])
    Histoklcg[ii].SetMarkerSize(2.0)
    #    
    HistoklcgExclu[ii] = TH2D("","", 500,-20,16.5,500,-1.1,1.5 )
    HistoklcgExclu[ii].GetYaxis().SetTitle(" ")
    HistoklcgExclu[ii].GetXaxis().SetTitle("#kappa_{#lambda}")
    HistoklcgExclu[ii].SetLineColor(mc[ii])
    HistoklcgExclu[ii].SetMarkerColor(mc[ii])
    HistoklcgExclu[ii].SetMarkerStyle(mtexclu[ii])
    HistoklcgExclu[ii].SetMarkerSize(2.0)
    #
    Histocgc2g[ii] = TH2D("","", 500,-1.4,1.1,500,-1.1,2.2  )
    Histocgc2g[ii].GetYaxis().SetTitle("")
    Histocgc2g[ii].GetXaxis().SetTitle("c_{g}")
    Histocgc2g[ii].SetLineColor(mc[ii])
    Histocgc2g[ii].SetMarkerColor(mc[ii])
    Histocgc2g[ii].SetMarkerStyle(mt[ii])
    Histocgc2g[ii].SetMarkerSize(2.0)
    #    
    Histocgc2gExclu[ii] = TH2D("","", 500,-20,16.5,500,-1.1,1.5 )
    Histocgc2gExclu[ii].GetYaxis().SetTitle("")
    Histocgc2gExclu[ii].GetXaxis().SetTitle("c_{g}")
    Histocgc2gExclu[ii].SetLineColor(mc[ii])
    Histocgc2gExclu[ii].SetMarkerColor(mc[ii])
    Histocgc2gExclu[ii].SetMarkerStyle(mtexclu[ii])
    Histocgc2gExclu[ii].SetMarkerSize(2.0)
    #
    Histoc2cg[ii] = TH2D("","", 500,-3.5,5.6,500,-1.2,2.2  )
    Histoc2cg[ii].GetYaxis().SetTitle(" ")
    Histoc2cg[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2cg[ii].SetLineColor(mc[ii])
    Histoc2cg[ii].SetMarkerColor(mc[ii])
    Histoc2cg[ii].SetMarkerStyle(mt[ii])
    Histoc2cg[ii].SetMarkerSize(2.0)
    #    
    Histoc2cgExclu[ii] = TH2D("","", 500,-20,16.5,500,-1.1,1.5 )
    Histoc2cgExclu[ii].GetYaxis().SetTitle("c_{2g}")
    Histoc2cgExclu[ii].GetXaxis().SetTitle("c_{g}")
    Histoc2cgExclu[ii].SetLineColor(mc[ii])
    Histoc2cgExclu[ii].SetMarkerColor(mc[ii])
    Histoc2cgExclu[ii].SetMarkerStyle(mtexclu[ii])
    Histoc2cgExclu[ii].SetMarkerSize(2.0)
    #
    Histocgc2g05[ii] = TH2D("","", 500,-1.4,1.1,500,-1.1,2.2  )
    Histocgc2g05[ii].GetYaxis().SetTitle("c_{2g}")
    Histocgc2g05[ii].GetXaxis().SetTitle("c_{g}")
    Histocgc2g05[ii].SetLineColor(mc[ii])
    Histocgc2g05[ii].SetMarkerColor(mc[ii])
    Histocgc2g05[ii].SetMarkerStyle(mt[ii])
    Histocgc2g05[ii].SetMarkerSize(2.0)
    #    
    Histocgc2g05Exclu[ii] = TH2D("","", 500,-20,16.5,500,-1.1,1.5 )
    Histocgc2g05Exclu[ii].GetYaxis().SetTitle("c_{2g}")
    Histocgc2g05Exclu[ii].GetXaxis().SetTitle("c_{g}")
    Histocgc2g05Exclu[ii].SetLineColor(mc[ii])
    Histocgc2g05Exclu[ii].SetMarkerColor(mc[ii])
    Histocgc2g05Exclu[ii].SetMarkerStyle(mtexclu[ii])
    Histocgc2g05Exclu[ii].SetMarkerSize(2.0)
    # kl = 12p5
    Histoc2kt12p5[ii] = TH2D("","", 500,-3.8,5.5,500,0.3,3.8 )
    Histoc2kt12p5[ii].GetYaxis().SetTitle(" ")
    Histoc2kt12p5[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2kt12p5[ii].SetLineColor(mc[ii])
    Histoc2kt12p5[ii].SetMarkerColor(mc[ii])
    Histoc2kt12p5[ii].SetMarkerStyle(mt[ii])
    Histoc2kt12p5[ii].SetMarkerSize(2.0)
    #    
    Histoc2kt12p5Exclu[ii] = TH2D("","", 500,-3.5,3.5,500,0.3,2.8 )
    Histoc2kt12p5Exclu[ii].GetYaxis().SetTitle(" ")
    Histoc2kt12p5Exclu[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2kt12p5Exclu[ii].SetLineColor(mc[ii])
    Histoc2kt12p5Exclu[ii].SetMarkerColor(mc[ii])
    Histoc2kt12p5Exclu[ii].SetMarkerStyle(mtexclu[ii])
    Histoc2kt12p5Exclu[ii].SetMarkerSize(2.0)
    # kl = -12p5
    Histoc2ktm12p5[ii] = TH2D("","", 500,-4.8,3.5,500,0.3,3.8 )
    Histoc2ktm12p5[ii].GetYaxis().SetTitle(" ")
    Histoc2ktm12p5[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2ktm12p5[ii].SetLineColor(mc[ii])
    Histoc2ktm12p5[ii].SetMarkerColor(mc[ii])
    Histoc2ktm12p5[ii].SetMarkerStyle(mt[ii])
    Histoc2ktm12p5[ii].SetMarkerSize(2.0)
    #    
    Histoc2ktm12p5Exclu[ii] = TH2D("","", 500,-3.5,3.5,500,0.3,2.8 )
    Histoc2ktm12p5Exclu[ii].GetYaxis().SetTitle(" ")
    Histoc2ktm12p5Exclu[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2ktm12p5Exclu[ii].SetLineColor(mc[ii])
    Histoc2ktm12p5Exclu[ii].SetMarkerColor(mc[ii])
    Histoc2ktm12p5Exclu[ii].SetMarkerStyle(mtexclu[ii])
    Histoc2ktm12p5Exclu[ii].SetMarkerSize(2.0)
    # kl = 10p0
    Histoc2kt10p0[ii] = TH2D("","",500,-3.8,5.5,500,0.3,3.8 )
    Histoc2kt10p0[ii].GetYaxis().SetTitle(" ")
    Histoc2kt10p0[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2kt10p0[ii].SetLineColor(mc[ii])
    Histoc2kt10p0[ii].SetMarkerColor(mc[ii])
    Histoc2kt10p0[ii].SetMarkerStyle(mt[ii])
    Histoc2kt10p0[ii].SetMarkerSize(2.0)
    #    
    Histoc2kt10p0Exclu[ii] = TH2D("","", 500,-3.5,3.5,500,0.3,2.8 )
    Histoc2kt10p0Exclu[ii].GetYaxis().SetTitle(" ")
    Histoc2kt10p0Exclu[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2kt10p0Exclu[ii].SetLineColor(mc[ii])
    Histoc2kt10p0Exclu[ii].SetMarkerColor(mc[ii])
    Histoc2kt10p0Exclu[ii].SetMarkerStyle(mtexclu[ii])
    Histoc2kt10p0Exclu[ii].SetMarkerSize(2.0)
    # kl = -10p0
    Histoc2ktm10p0[ii] = TH2D("","", 500,-4.8,3.5,500,0.3,3.8 )
    Histoc2ktm10p0[ii].GetYaxis().SetTitle(" ")
    Histoc2ktm10p0[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2ktm10p0[ii].SetLineColor(mc[ii])
    Histoc2ktm10p0[ii].SetMarkerColor(mc[ii])
    Histoc2ktm10p0[ii].SetMarkerStyle(mt[ii])
    Histoc2ktm10p0[ii].SetMarkerSize(2.0)
    #    
    Histoc2ktm10p0Exclu[ii] = TH2D("","", 500,-3.5,3.5,500,0.3,2.8 )
    Histoc2ktm10p0Exclu[ii].GetYaxis().SetTitle(" ")
    Histoc2ktm10p0Exclu[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2ktm10p0Exclu[ii].SetLineColor(mc[ii])
    Histoc2ktm10p0Exclu[ii].SetMarkerColor(mc[ii])
    Histoc2ktm10p0Exclu[ii].SetMarkerStyle(mtexclu[ii])
    Histoc2ktm10p0Exclu[ii].SetMarkerSize(2.0)
    # kl = 7p5
    Histoc2kt7p5[ii] = TH2D("","", 500,-3.8,5.5,500,0.3,3.8 )
    Histoc2kt7p5[ii].GetYaxis().SetTitle(" ")
    Histoc2kt7p5[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2kt7p5[ii].SetLineColor(mc[ii])
    Histoc2kt7p5[ii].SetMarkerColor(mc[ii])
    Histoc2kt7p5[ii].SetMarkerStyle(mt[ii])
    Histoc2kt7p5[ii].SetMarkerSize(2.0)
    #    
    Histoc2kt7p5Exclu[ii] = TH2D("","", 500,-3.8,5.5,500,0.3,3.8 )
    Histoc2kt7p5Exclu[ii].GetYaxis().SetTitle(" ")
    Histoc2kt7p5Exclu[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2kt7p5Exclu[ii].SetLineColor(mc[ii])
    Histoc2kt7p5Exclu[ii].SetMarkerColor(mc[ii])
    Histoc2kt7p5Exclu[ii].SetMarkerStyle(mtexclu[ii])
    Histoc2kt7p5Exclu[ii].SetMarkerSize(2.0)
    # kl = -7p5
    Histoc2ktm7p5[ii] = TH2D("","", 500,-4.8,3.5,500,0.3,3.8 )
    Histoc2ktm7p5[ii].GetYaxis().SetTitle(" ")
    Histoc2ktm7p5[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2ktm7p5[ii].SetLineColor(mc[ii])
    Histoc2ktm7p5[ii].SetMarkerColor(mc[ii])
    Histoc2ktm7p5[ii].SetMarkerStyle(mt[ii])
    Histoc2ktm7p5[ii].SetMarkerSize(2.0)
    #    
    Histoc2ktm7p5Exclu[ii] = TH2D("","", 500,-3.5,3.5,500,0.3,2.8 )
    Histoc2ktm7p5Exclu[ii].GetYaxis().SetTitle(" ")
    Histoc2ktm7p5Exclu[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2ktm7p5Exclu[ii].SetLineColor(mc[ii])
    Histoc2ktm7p5Exclu[ii].SetMarkerColor(mc[ii])
    Histoc2ktm7p5Exclu[ii].SetMarkerStyle(mtexclu[ii])
    Histoc2ktm7p5Exclu[ii].SetMarkerSize(2.0)
    # kl = 5p0
    Histoc2kt5p0[ii] = TH2D("","", 500,-3.8,5.5,500,0.3,3.8  )
    Histoc2kt5p0[ii].GetYaxis().SetTitle(" ")
    Histoc2kt5p0[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2kt5p0[ii].SetLineColor(mc[ii])
    Histoc2kt5p0[ii].SetMarkerColor(mc[ii])
    Histoc2kt5p0[ii].SetMarkerStyle(mt[ii])
    Histoc2kt5p0[ii].SetMarkerSize(2.0)
    #    
    Histoc2kt5p0Exclu[ii] = TH2D("","", 500,-3.8,5.5,500,0.3,3.8  )
    Histoc2kt5p0Exclu[ii].GetYaxis().SetTitle(" ")
    Histoc2kt5p0Exclu[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2kt5p0Exclu[ii].SetLineColor(mc[ii])
    Histoc2kt5p0Exclu[ii].SetMarkerColor(mc[ii])
    Histoc2kt5p0Exclu[ii].SetMarkerStyle(mtexclu[ii])
    Histoc2kt5p0Exclu[ii].SetMarkerSize(2.0)
    # kl = -5p0
    Histoc2ktm5p0[ii] = TH2D("","", 500,-4.8,3.5,500,0.3,3.8 )
    Histoc2ktm5p0[ii].GetYaxis().SetTitle(" ")
    Histoc2ktm5p0[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2ktm5p0[ii].SetLineColor(mc[ii])
    Histoc2ktm5p0[ii].SetMarkerColor(mc[ii])
    Histoc2ktm5p0[ii].SetMarkerStyle(mt[ii])
    Histoc2ktm5p0[ii].SetMarkerSize(2.0)
    #    
    Histoc2ktm5p0Exclu[ii] = TH2D("","", 500,-3.5,3.5,500,0.3,2.8 )
    Histoc2ktm5p0Exclu[ii].GetYaxis().SetTitle(" ")
    Histoc2ktm5p0Exclu[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2ktm5p0Exclu[ii].SetLineColor(mc[ii])
    Histoc2ktm5p0Exclu[ii].SetMarkerColor(mc[ii])
    Histoc2ktm5p0Exclu[ii].SetMarkerStyle(mtexclu[ii])
    Histoc2ktm5p0Exclu[ii].SetMarkerSize(2.0)
    # kl = 3p5
    Histoc2kt3p5[ii] = TH2D("","", 500,-3.8,5.5,500,0.3,3.8 )
    Histoc2kt3p5[ii].GetYaxis().SetTitle(" ")
    Histoc2kt3p5[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2kt3p5[ii].SetLineColor(mc[ii])
    Histoc2kt3p5[ii].SetMarkerColor(mc[ii])
    Histoc2kt3p5[ii].SetMarkerStyle(mt[ii])
    Histoc2kt3p5[ii].SetMarkerSize(2.0)
    #    
    Histoc2kt3p5Exclu[ii] = TH2D("","", 500,-3.8,5.5,500,0.3,3.8  )
    Histoc2kt3p5Exclu[ii].GetYaxis().SetTitle(" ")
    Histoc2kt3p5Exclu[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2kt3p5Exclu[ii].SetLineColor(mc[ii])
    Histoc2kt3p5Exclu[ii].SetMarkerColor(mc[ii])
    Histoc2kt3p5Exclu[ii].SetMarkerStyle(mtexclu[ii])
    Histoc2kt3p5Exclu[ii].SetMarkerSize(2.0)
    # kl = -3p5
    Histoc2ktm3p5[ii] = TH2D("","", 500,-4.8,3.5,500,0.3,3.8 )
    Histoc2ktm3p5[ii].GetYaxis().SetTitle(" ")
    Histoc2ktm3p5[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2ktm3p5[ii].SetLineColor(mc[ii])
    Histoc2ktm3p5[ii].SetMarkerColor(mc[ii])
    Histoc2ktm3p5[ii].SetMarkerStyle(mt[ii])
    Histoc2ktm3p5[ii].SetMarkerSize(2.0)
    #    
    Histoc2ktm3p5Exclu[ii] = TH2D("","", 500,-3.5,3.5,500,0.3,2.8 )
    Histoc2ktm3p5Exclu[ii].GetYaxis().SetTitle(" ")
    Histoc2ktm3p5Exclu[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2ktm3p5Exclu[ii].SetLineColor(mc[ii])
    Histoc2ktm3p5Exclu[ii].SetMarkerColor(mc[ii])
    Histoc2ktm3p5Exclu[ii].SetMarkerStyle(mtexclu[ii])
    Histoc2ktm3p5Exclu[ii].SetMarkerSize(2.0)
    # kl = 2p4
    Histoc2kt2p4[ii] = TH2D("","", 500,-4.8,3.5,500,0.3,3.8  )
    Histoc2kt2p4[ii].GetYaxis().SetTitle(" ")
    Histoc2kt2p4[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2kt2p4[ii].SetLineColor(mc[ii])
    Histoc2kt2p4[ii].SetMarkerColor(mc[ii])
    Histoc2kt2p4[ii].SetMarkerStyle(mt[ii])
    Histoc2kt2p4[ii].SetMarkerSize(2.0)
    #    
    Histoc2kt2p4Exclu[ii] = TH2D("","", 500,-3.8,5.5,500,0.3,3.8 )
    Histoc2kt2p4Exclu[ii].GetYaxis().SetTitle(" ")
    Histoc2kt2p4Exclu[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2kt2p4Exclu[ii].SetLineColor(mc[ii])
    Histoc2kt2p4Exclu[ii].SetMarkerColor(mc[ii])
    Histoc2kt2p4Exclu[ii].SetMarkerStyle(mtexclu[ii])
    Histoc2kt2p4Exclu[ii].SetMarkerSize(2.0)
    # kl = -2.4
    Histoc2ktm2p4[ii] = TH2D("","", 500,-4.8,3.5,500,0.3,3.8 )
    Histoc2ktm2p4[ii].GetYaxis().SetTitle(" ")
    Histoc2ktm2p4[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2ktm2p4[ii].SetLineColor(mc[ii])
    Histoc2ktm2p4[ii].SetMarkerColor(mc[ii])
    Histoc2ktm2p4[ii].SetMarkerStyle(mt[ii])
    Histoc2ktm2p4[ii].SetMarkerSize(2.0)
    #    
    Histoc2ktm2p4Exclu[ii] = TH2D("","", 500,-3.5,3.5,500,0.3,2.8 )
    Histoc2ktm2p4Exclu[ii].GetYaxis().SetTitle(" ")
    Histoc2ktm2p4Exclu[ii].GetXaxis().SetTitle("c_{2}")
    Histoc2ktm2p4Exclu[ii].SetLineColor(mc[ii])
    Histoc2ktm2p4Exclu[ii].SetMarkerColor(mc[ii])
    Histoc2ktm2p4Exclu[ii].SetMarkerStyle(mtexclu[ii])
    Histoc2ktm2p4Exclu[ii].SetMarkerSize(2.0)
#####
allowed = TH2D("","", 500,-4.5,3.5,500,0.3,3.8 )
allowed.GetYaxis().SetTitle("#kappa_{t}")
allowed.GetXaxis().SetTitle("c_{2}")
allowed.SetLineColor(mc[ii])
allowed.SetMarkerColor(1)
allowed.SetMarkerStyle(20)
allowed.SetMarkerSize(2.0)
#
excluded = TH2D("","", 500,-4.5,3.5,500,0.3,3.8 )
excluded.GetYaxis().SetTitle("#kappa_{t}")
excluded.GetXaxis().SetTitle("c_{2}")
excluded.SetLineColor(mc[ii])
excluded.SetMarkerColor(1)
excluded.SetMarkerStyle(24)
excluded.SetMarkerSize(2.0)
#  
#
################################
##
## read the translation
##
###########################
npoints=1507
fpoints = "list_all_translation_1507.txt"
fp = open(fpoints, 'r+')
linesp = fp.readlines() # get all lines as a list (array)
L = np.zeros((npoints))
y = np.zeros((npoints))
c2 = np.zeros((npoints))
cg = np.zeros((npoints))
c2g = np.zeros((npoints))
# Iterate over each line, printing each line and then move to the next
counter =0
for line in linesp:
    #print line
    tokens = line.split()
    L[counter] = float(tokens[0])
    y[counter] = float(tokens[1])    
    c2[counter] = float(tokens[2])    
    cg[counter] = float(tokens[3])
    c2g[counter] = float(tokens[4])
    #print str(tokens[0])+ " " + str(tokens[1])+ " " + str(tokens[2])+ " " + str(tokens[3])+ " " + str(tokens[4])
    counter+=1
fp.close()

#for counter in range(0,1507): print str(L[counter])+ " " + str(y[counter])+ " " + str(c2[counter])+ " " + str(cg[counter])+ " " + str(c2g[counter])
########################
##
##
##
########################
fileclusters12 = "Translation_1507points/clustering_nev20k_Nclu12_50_5.asc"
fclu = open(fileclusters12, 'r+')
linespclu = fclu.readlines() 
head = np.zeros((nclu))
clusters = [[]] #np.zeros((nclu,500))
counter = 0
for line in linespclu:
    tokens = line.split()
    #print "menbers: "+  str(len(tokens))+ " head: "+tokens[0]
    head[counter] = tokens[0]
    clusters.append([])
    for ii in range(0,len(tokens)) : clusters[counter].append(int(tokens[ii]))
    #print str(counter)+" "+str(len(clusters[counter]))
    counter+=1
########################
## 
## loop on points cluster
##
#######################
#for ii in range(0,nclu): print len(clusters[ii])
#if(type==1) : 
spreadx = np.zeros((npoints))
spready = np.zeros((npoints))
benchx = np.zeros((nclu))
benchy = np.zeros((nclu))
for point in range(0,1507):
    for ii in range(0,nclu):
        #print clusters[ii]
        if (point == clusters[ii][0]) : 
            benchx[ii] = ii+1
            benchy[ii] =  limitsExp[point]
        if point in clusters[ii]: 
           ###
           #spread[ii].Fill(limitsExp[ii] )
           spreadx[point] = ii+1
           spready[point] =  limitsExp[point]
           #print "point "+str(point) +" "+ str(limitsExp[ii]) 
           #print "it is in cluster:  " +str(ii+1)
           if(L[point]==15.0 and cg[point] ==0 and c2g[point] ==0 ) : 
               if ( (ff15d15.Eval(c2[point],y[point]))*xs*BR > limitsExp[ii]  ) : Histoc2kt15Exclu[ii].Fill(c2[point],y[point])
               else : Histoc2kt15[ii].Fill(c2[point],y[point])  
           if(L[point]==-15.0 and cg[point] ==0 and c2g[point] ==0 ) : 
               if ( (ff15dm15.Eval(c2[point],y[point]))*xs*BR > limitsExp[ii]  ) : Histoc2ktm15Exclu[ii].Fill(c2[point],y[point])
               else : Histoc2ktm15[ii].Fill(c2[point],y[point]) 
           if(L[point]==12.5 and cg[point] ==0 and c2g[point] ==0 ) : 
               if ( (ff15d12p5.Eval(c2[point],y[point]))*xs*BR > limitsExp[ii]  ) : Histoc2kt12p5Exclu[ii].Fill(c2[point],y[point])
               else : Histoc2kt12p5[ii].Fill(c2[point],y[point])  
           if(L[point]==-12.5 and cg[point] ==0 and c2g[point] ==0 ) : 
               if ( (ff15dm12p5.Eval(c2[point],y[point]))*xs*BR > limitsExp[ii]  ) : Histoc2ktm12p5Exclu[ii].Fill(c2[point],y[point])
               else : Histoc2ktm12p5[ii].Fill(c2[point],y[point]) 
           if(L[point]==10.0 and cg[point] ==0 and c2g[point] ==0 ) : 
               if ( (ff15d10p0.Eval(c2[point],y[point]))*xs*BR > limitsExp[ii]  ) : Histoc2kt10p0Exclu[ii].Fill(c2[point],y[point])
               else : Histoc2kt10p0[ii].Fill(c2[point],y[point])  
           if(L[point]==-10.0 and cg[point] ==0 and c2g[point] ==0 ) : 
               if ( (ff15dm10p0.Eval(c2[point],y[point]))*xs*BR > limitsExp[ii]  ) : Histoc2ktm10p0Exclu[ii].Fill(c2[point],y[point])
               else : Histoc2ktm10p0[ii].Fill(c2[point],y[point]) 
           if(L[point]==7.5 and cg[point] ==0 and c2g[point] ==0 ) : 
               if ( (ff15d7p5.Eval(c2[point],y[point]))*xs*BR > limitsExp[ii]  ) : Histoc2kt7p5Exclu[ii].Fill(c2[point],y[point])
               else : Histoc2kt7p5[ii].Fill(c2[point],y[point])  
           if(L[point]==-7.5 and cg[point] ==0 and c2g[point] ==0 ) : 
               if ( (ff15dm7p5.Eval(c2[point],y[point]))*xs*BR > limitsExp[ii]  ) : Histoc2ktm7p5Exclu[ii].Fill(c2[point],y[point])
               else : Histoc2ktm7p5[ii].Fill(c2[point],y[point]) 
           if(L[point]==5.0 and cg[point] ==0 and c2g[point] ==0 ) : 
               if ( (ff15d5p0.Eval(c2[point],y[point]))*xs*BR > limitsExp[ii]  ) : Histoc2kt5p0Exclu[ii].Fill(c2[point],y[point])
               else : Histoc2kt5p0[ii].Fill(c2[point],y[point])  
           if(L[point]==-5.0 and cg[point] ==0 and c2g[point] ==0 ) : 
               if ( (ff15dm5p0.Eval(c2[point],y[point]))*xs*BR > limitsExp[ii]  ) : Histoc2ktm5p0Exclu[ii].Fill(c2[point],y[point])
               else : Histoc2ktm5p0[ii].Fill(c2[point],y[point]) 
           if(L[point]==3.5 and cg[point] ==0 and c2g[point] ==0 ) : 
               if ( (ff15d3p5.Eval(c2[point],y[point]))*xs*BR > limitsExp[ii]  ) : Histoc2kt3p5Exclu[ii].Fill(c2[point],y[point])
               else : Histoc2kt3p5[ii].Fill(c2[point],y[point])  
           if(L[point]==-3.5 and cg[point] ==0 and c2g[point] ==0 ) : 
               if ( (ff15dm3p5.Eval(c2[point],y[point]))*xs*BR > limitsExp[ii]  ) : Histoc2ktm3p5Exclu[ii].Fill(c2[point],y[point])
               else : Histoc2ktm3p5[ii].Fill(c2[point],y[point])
           if(L[point]==2.4 and cg[point] ==0 and c2g[point] ==0 ) : 
               if ( (ff15d2p4.Eval(c2[point],y[point]))*xs*BR > limitsExp[ii]  ) : Histoc2kt2p4Exclu[ii].Fill(c2[point],y[point])
               else : Histoc2kt2p4[ii].Fill(c2[point],y[point])  
           if(L[point]==-2.4 and cg[point] ==0 and c2g[point] ==0 ) : 
               if ( (ff15dm3p5.Eval(c2[point],y[point]))*xs*BR > limitsExp[ii]  ) : Histoc2ktm2p4Exclu[ii].Fill(c2[point],y[point])
               else : Histoc2ktm2p4[ii].Fill(c2[point],y[point])
######
           if(L[point]==1 and cg[point] ==0 and c2g[point] ==0 ) : 
               if ( (ff15d.Eval(c2[point],y[point]))*xs*BR > limitsExp[ii]  ) : Histoc2ktExclu[ii].Fill(c2[point],y[point])
               else : Histoc2kt[ii].Fill(c2[point],y[point])
           if(c2[point]==0 and cg[point] ==0 and c2g[point] ==0 ) : 
               if ( (ff25d.Eval(L[point],y[point]))*xs*BR > limitsExp[ii]  ) : HistoklktExclu[ii].Fill(L[point],y[point])
               else : Histoklkt[ii].Fill(L[point],y[point])                   
           if(c2[point]==0 and y[point] ==1 and c2g[point] == -cg[point] ) : 
               if ( (ff35d.Eval(L[point],cg[point]))*xs*BR > limitsExp[ii]  ) : HistoklcgExclu[ii].Fill(L[point],cg[point])
               else : Histoklcg[ii].Fill(L[point],cg[point])  
           if(c2[point]==0 and y[point] ==1 and L[point] == 1) : 
               if ( (ff45d.Eval(cg[point],c2g[point]))*xs*BR > limitsExp[ii]  ) : Histocgc2gExclu[ii].Fill(cg[point],c2g[point])
               else : Histocgc2g[ii].Fill(cg[point],c2g[point])  
           if(c2g[point] == -cg[point] and y[point] ==1 and L[point] == 1) : 
               if ( (ff55d.Eval(c2[point],cg[point]))*xs*BR > limitsExp[ii]  ) : Histoc2cgExclu[ii].Fill(c2[point],cg[point])
               else : Histoc2cg[ii].Fill(c2[point],cg[point])  
           if(c2[point]==0.5 and y[point] ==1 and L[point] == 1) : 
               if ( (ff65d.Eval(cg[point],c2g[point]))*xs*BR > limitsExp[ii]  ) : Histocgc2g05Exclu[ii].Fill(cg[point],c2g[point])
               else : Histocgc2g05[ii].Fill(cg[point],c2g[point])  
           #print str(point) + " "+str(c2[point]) + " "+str(y[point])+" cluster "+str(ii)+" "+  str(limitsExp[ii])  +" TH: "+str(math.exp(ff15d.Eval(c2[point],y[point]))*xs*BR)

spread = None
print len(spreadx)
    #for ii in range(0,nclu):
spread = TGraph(npoints,spreadx,spready)
spread.GetYaxis().SetTitle(channel)
spread.GetXaxis().SetTitle("Shape Benchmark")
#
bench = None
print len(spreadx)
#for ii in range(0,nclu):
bench = TGraph(nclu,benchx,benchy)
bench.GetYaxis().SetTitle(channel)
bench.GetXaxis().SetTitle("Shape Benchmark")
#spread.SetLineColor(mc[ii])
bench.SetMarkerColor(2)

#spread.SetMarkerStyle(10)
#spread[ii].SetMarkerSize(0.5)
#spread[ii].SetMaximum(1000000)
#spread[ii].SetMinimum(100)
########################
## 
## draw
##
#######################
text = TLatex() # CMS
text.SetTextSize(0.04)
textlumi = TLatex() # 
textlumi.SetTextSize(0.04)
textlumi.SetTextFont(42)
text3 = TLatex()
text3.SetTextSize(0.04)
text2 = TLatex()
text2.SetTextSize(0.028) 
text4 = TLatex()
text4.SetTextSize(0.06) 
#
cx = TLatex()
cx.SetTextSize(0.028);
#
lineHc2kt =  TLine(-4.8,2.7,3.5,2.7)
lineHc2ktpos =  TLine(-3.8,2.7,5.5,2.7)
lineTc2kt =  TLine(-0.9,2.7,-0.9,3.8)
lineTc2ktpos =  TLine(0.8,2.7,0.8,3.8)
#
lineHklcg =  TLine(-20,1.1,16,1.1)
lineTklcg =  TLine(-2.0,1.1,-2.0,2.2)
#
lineHklkt =  TLine(-21,2.65,16.5,2.65)
lineTklkt =  TLine(-2.5,2.65,-2.5,3.8)
#
lineHc2cg =  TLine(-3.5,1.1,5.6,1.1)
lineTc2cg =  TLine(0.9,1.1,0.9,2.2)
#
lineHcgc2g =  TLine(-1.4,1.1,1.1,1.1)
lineTcgc2g =  TLine(-0.2,2.2,-0.2,1.1)
# kt axis (of c2kt plots)
axisc2kt = TGaxis(-4.8,0.4,-4.8,2.5,0.4,2.5,5,"")     
axisc2kt.SetName("axisc2kt")
# kt axis (of c2kt plots) kl >0
axisc2ktpos = TGaxis(-3.8,0.4,-3.8,2.5,0.4,2.5,5,"")     
axisc2ktpos.SetName("axisc2ktpos")
# kt axis (of cgc2g plots)
axiscgc2g = TGaxis(-1.4,-1.1,-1.4,1.0,-1.1,1.0,5,"")     
axiscgc2g.SetName("axisc2kt")
################################
c=TCanvas("c2","c2",200,50,600,600)
Histoc2kt[0].SetNdivisions(0, "Y") #.GetYaxis().SetLabelOffset(999)
Histoc2kt[0].Draw()
leg2.AddEntry(allowed, "Allowed", "P")
leg2.AddEntry(excluded, "Excluded", "P")
leg3.AddEntry(ff15d, "Th. cross section", "L")
if(type==1) : 
  if (chan==4 or chan==3) : leg.AddEntry(Histoc2kt[0], str(round_sig(limitsExp[0]/1000, 3)), "P")
  else : leg.AddEntry(Histoc2kt[0], str(round_sig(limitsExp[0], 3)), "P")
elif(type==2) : leg.AddEntry(Histoc2kt[0], str(1), "P")
Histoc2ktExclu[0].Draw("same")
ff15d.Draw("same")
for ii in range(1,nclu): 
   Histoc2kt[ii].Draw("same")
   if(type==1) : 
      if (chan==4 or chan==3) : leg.AddEntry(Histoc2kt[ii],str(round_sig(limitsExp[ii]/1000, 3)),"P") # lege20[ii], "P")
      else : leg.AddEntry(Histoc2kt[ii],str(round_sig(limitsExp[ii], 3)),"P") 
   elif(type==2) : leg.AddEntry(Histoc2kt[ii], str(ii+1), "P")
   Histoc2ktExclu[ii].Draw("same")
#text.DrawLatex(-4.2,3.55,"#kappa_{#lambda} = 1 ; c_{g} = c_{2g} = 0")
#text2.DrawLatex(-4.2,3.55,"#sigma(pp #rightarrow HH #rightarrow #gamma#gamma b#bar{b})")
text3.DrawLatex(-4.5,3.55,channel)
text2.DrawLatex(-4.5,2.8,"(Assuming SM H decays)")
text.DrawLatex(-4.4,2.45,"#kappa_{#lambda} = 1")
text.DrawLatex(-4.8,3.9,warning)
textlumi.DrawLatex(0.2,3.9,lumi)
lineHc2kt.Draw("same")
lineTc2kt.Draw("same")
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
if (chan==1) :
  cx.SetTextAngle(50);
  cx.DrawLatex(-4.1,1.63,"#color[12]{100 fb}");
  cx.SetTextAngle(75);
  cx.DrawLatex(-3.5,0.6,"#color[12]{50 fb}");
if (chan==2) :
    cx.SetTextAngle(50);
    cx.DrawLatex(-4.1,1.63,"#color[12]{20 fb}");
    cx.SetTextAngle(75);
    cx.DrawLatex(-3.5,0.6,"#color[12]{10 fb}");
if (chan==3) :
    cx.SetTextAngle(70);
    cx.DrawLatex(-4.1,1.23,"#color[12]{500 fb}");
    cx.SetTextAngle(75);
    cx.DrawLatex(-3.5,0.6,"#color[12]{300 fb}");
    #print (ff15d.Eval(-3,1))*(xs*BR)
# kt axis
axisc2kt.Draw()
text4.SetTextAngle(90)
text4.DrawLatex(-5.7,2.3,"#kappa_{t}")
c.Print(outfolder+"/c2_kt.png")
c.Close()
#############################
ckl=TCanvas("c2","c2",200,50,600,600)
Histoklkt[0].SetNdivisions(0, "Y") #.GetYaxis().SetLabelOffset(999)
Histoklkt[0].GetYaxis().CenterTitle()
Histoklkt[0].Draw()
HistoklktExclu[0].Draw("same")
ff25d.Draw("same")
for ii in range(1,nclu): 
    Histoklkt[ii].Draw("same")
    HistoklktExclu[ii].Draw("same")
#text.DrawLatex(-19,3.55,"c_{2} = c_{2g} = c_{g} = 0 ")
text3.DrawLatex(-19.5,3.55,channel)
text.DrawLatex(-21,3.9,warning)
textlumi.DrawLatex(2.1,3.9,lumi)
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
text2.DrawLatex(-19,2.8,"(Assuming SM H decays)")
lineHklkt.Draw("same")
lineTklkt.Draw("same")
if (chan==1) :
  cx.SetTextAngle(33);
  cx.DrawLatex(-19,1.81,"#color[12]{200 fb}");
  cx.SetTextAngle(25);
  cx.DrawLatex(-19,1.405,"#color[12]{100 fb}");
  cx.SetTextAngle(25);
  cx.DrawLatex(-19,1.01,"#color[12]{50 fb}");
if (chan==2) :
    cx.SetTextAngle(33);
    cx.DrawLatex(-19,1.95,"#color[12]{50 fb}");
    cx.SetTextAngle(28);
    cx.DrawLatex(-19,1.35,"#color[12]{20 fb}");
    cx.SetTextAngle(25);
    cx.DrawLatex(-19,1.0,"#color[12]{10 fb}");
if (chan==3) :
    cx.SetTextAngle(30);
    cx.DrawLatex(-19,1.25,"#color[12]{500 fb}");
    cx.SetTextAngle(25);
    cx.DrawLatex(-19,1.01,"#color[12]{300 fb}");
    cx.SetTextAngle(20);
    cx.DrawLatex(-19,0.63,"#color[12]{100 fb}");
# kt axis
axis2 = TGaxis(-21.,0.4,-21,2.5,0.4,2.5,5,"")     
axis2.SetName("axis2")
axis2.Draw()
text4.SetTextAngle(90)
text4.DrawLatex(-25,2.3,"#kappa_{t}")
ckl.Print(outfolder+"/kl_kt.png")
ckl.Print(outfolder+"/kl_kt.pdf")
###############################
ckl=TCanvas("c2","c2",200,50,600,600)
Histoklcg[0].SetNdivisions(0, "Y")
Histoklcg[0].Draw()
HistoklcgExclu[0].Draw("same")
ff35d.Draw("same")
for ii in range(1,nclu): 
    Histoklcg[ii].Draw("same")
    HistoklcgExclu[ii].Draw("same")
#text.DrawLatex(-19,2.0,"#kappa_{t} = 1 ; c_{2} = 0 ; c_{2} = -c_{2g}")
text3.DrawLatex(-19,1.95,channel)
text.DrawLatex(-20,2.3,warning)
textlumi.DrawLatex(2,2.3,lumi)
lineHklcg.Draw("same")
lineTklcg.Draw("same")
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
if (chan==1) :
  cx.SetTextAngle(50);
  cx.DrawLatex(-18,0.08,"#color[12]{50 fb}");
  cx.SetTextAngle(35);
  cx.DrawLatex(-18,-0.48,"#color[12]{30 fb}");
elif (chan==2) :
    cx.SetTextAngle(50);
    cx.DrawLatex(-18,0.05,"#color[12]{10 fb}");
    cx.SetTextAngle(35);
    cx.DrawLatex(-18,-0.65,"#color[12]{5 fb}");
elif (chan==3) :
    cx.SetTextAngle(53);
    cx.DrawLatex(-18.6,0.045,"#color[12]{300 fb}");
    cx.SetTextAngle(35);
    cx.DrawLatex(-18.6,-1.04,"#color[12]{100 fb}");
text2.DrawLatex(-18.5,1.2,"(Assuming SM H decays)")
axis3 = TGaxis(-20.,-1.1,-20,1.2,-1.1,1.2,5,"")     
axis3.SetName("axis3")
axis3.Draw()
text4.SetTextAngle(90)
text4.DrawLatex(-23.8,0.3,"#scale[0.8]{c_{g} (= - c_{2g} )}")
ckl.Print(outfolder+"/kl_cg.png")
####################################
ccgc2g=TCanvas("c2","c2",200,50,600,600)
Histocgc2g[0].SetNdivisions(0, "Y")
Histocgc2g[0].Draw()
Histocgc2gExclu[0].Draw("same")
ff45d.Draw("same")
for ii in range(1,nclu): 
    Histocgc2g[ii].Draw("same")
    Histocgc2gExclu[ii].Draw("same")
#text.DrawLatex(-19,2.0,"#kappa_{t} = 1 ; c_{2} = 0 ; c_{2} = -c_{2g}")
text3.DrawLatex(-1.35,1.95,channel)
textlumi.DrawLatex(0.1,2.25,lumi)
text.DrawLatex(-1.4,2.25,warning)
text2.DrawLatex(-1.3,1.2,"(Assuming SM H decays)")
lineHcgc2g.Draw("same")
lineTcgc2g.Draw("same")
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
if (chan==1) :
    cx.SetTextAngle(15);
    cx.DrawLatex(-1.3,-0.2,"#color[12]{0.5 fb}");
    cx.SetTextAngle(15);
    cx.DrawLatex(-1.3,0.4,"#color[12]{1 fb}");
elif (chan==2) :
    cx.SetTextAngle(15);
    cx.DrawLatex(-1.3,-0.35,"#color[12]{0.1 fb}");
    cx.SetTextAngle(15);
    cx.DrawLatex(-1.3,0.35,"#color[12]{0.2 fb}");
elif (chan==3) : 
    cx.SetTextAngle(10);
    cx.DrawLatex(-1.3,0.9,"#color[12]{10 fb}");
    cx.SetTextAngle(10);
    cx.DrawLatex(-1.3,0.25,"#color[12]{5 fb}");
    print (ff45d.Eval(-1,0.3))*(xs*BR)
axiscgc2g.Draw()
text4.SetTextAngle(90)
text4.DrawLatex(-1.6,0.75,"c_{2g}")
ccgc2g.Print(outfolder+"/cg_c2g.png")
##################################
cc2cg=TCanvas("c2","c2",200,50,600,600)
Histoc2cg[0].SetNdivisions(0, "Y")
Histoc2cg[0].Draw()
Histoc2cgExclu[0].Draw("same")
ff55d.Draw("same")
lineHc2cg.Draw("same")
lineTc2cg.Draw("same")
for ii in range(1,nclu): 
    Histoc2cg[ii].Draw("same")
    Histoc2cgExclu[ii].Draw("same")
#text.DrawLatex(-19,2.0,"#kappa_{t} = 1 ; c_{2} = 0 ; c_{2} = -c_{2g}")
text3.DrawLatex(-3.2,1.95,channel)
text.DrawLatex(-3.5,2.26,warning)
textlumi.DrawLatex(2,2.26,lumi)
#lineHklcg.Draw("same")
#lineTklcg.Draw("same")
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
if (chan==1) :
    cx.SetTextAngle(-83);
    cx.DrawLatex(3.97,-0.38,"#color[12]{50 fb}");
    cx.SetTextAngle(-83);
    cx.DrawLatex(5.15,0.35,"#color[12]{100 fb}");
#print (ff55d.Eval(3,0))*(xs*BR)
elif (chan==2) :
    cx.SetTextAngle(-85);
    cx.DrawLatex(3.9,-0.35,"#color[12]{10 fb}");
    cx.SetTextAngle(-75);
    cx.DrawLatex(4.5,0.35,"#color[12]{20 fb}");
elif (chan==3) : 
    cx.SetTextAngle(-80);
    cx.DrawLatex(3.97,-0.38,"#color[12]{300 fb}");
    cx.SetTextAngle(-80);
    cx.DrawLatex(4.7,0.35,"#color[12]{500 fb}");
#print (ff55d.Eval(0,1))*(xs*BR)
text2.DrawLatex(-3.0,1.2,"(Assuming SM H decays)")
axis4 = TGaxis(-3.5,-1.1,-3.5,1.2,-1.1,1.2,5,"")     
axis4.SetName("axis3")
axis4.Draw()
text4.SetTextAngle(90)
text4.DrawLatex(-4.48,0.3,"#scale[0.75]{c_{g} (= - c_{2g} )}")
cc2cg.Print(outfolder+"/c2_c2g.png")
####################################
# skip
ccgc2g05=TCanvas("c2","c2",200,50,600,600)
Histocgc2g05[0].Draw()
Histocgc2g05Exclu[0].Draw("same")
text.DrawLatex(-1.4,0.9,"c_{2} = 0.5")
ff65d.Draw("same")
for ii in range(1,nclu): 
    Histocgc2g05[ii].Draw("same")
    Histocgc2g05Exclu[ii].Draw("same")
#text.DrawLatex(-19,2.0,"#kappa_{t} = 1 ; c_{2} = 0 ; c_{2} = -c_{2g}")
text3.DrawLatex(-1.3,1.95,channel)
text.DrawLatex(-1.3,2.3,warning)
textlumi.DrawLatex(0.2,2.3,lumi)
text2.DrawLatex(-1.3,1.2,"(Assuming SM H decays)")
#lineHklcg.Draw("same")
#lineTklcg.Draw("same")
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
if (chan==5) :
    cx.SetTextAngle(15);
    cx.DrawLatex(-1.3,-0.2,"#color[12]{0.5 fb}");
    cx.SetTextAngle(15);
    cx.DrawLatex(-1.3,0.4,"#color[12]{1 fb}");
elif (chan==5) :
    cx.SetTextAngle(15);
    cx.DrawLatex(-1.3,-0.35,"#color[12]{0.1 fb}");
    cx.SetTextAngle(15);
    cx.DrawLatex(-1.3,0.35,"#color[12]{0.2 fb}");
text2.DrawLatex(-19,1.2,"(Assuming SM H decays)")
ccgc2g05.Print(outfolder+"/cg_c2g_c20p5.png")
###################################
cm15=TCanvas("c2","c2",200,50,600,600)
Histoc2ktm15[0].SetNdivisions(0, "Y")
Histoc2ktm15[0].Draw()
Histoc2kt[0].SetTickLength(0.0, "X")
gPad.Update()
Histoc2ktm15Exclu[0].Draw("same")
ff15dm15.Draw("same")
for ii in range(1,nclu): 
    Histoc2ktm15[ii].Draw("same")
    Histoc2ktm15Exclu[ii].Draw("same")
#text.DrawLatex(-4.1,3.55,"#kappa_{#lambda} = -15 ; c_{g} = c_{2g} = 0")
text3.DrawLatex(-4.5,3.55,channel)
text2.DrawLatex(-4.5,2.8,"(Assuming SM H decays)")
text.DrawLatex(-4.55,2.45,"#kappa_{#lambda} = -15")
text.DrawLatex(-4.8,3.85,warning)
textlumi.DrawLatex(0.3,3.85,lumi)
lineHc2kt.Draw("same")
lineTc2kt.Draw("same")
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
if (chan==1) :
    cx.SetTextAngle(30);
    cx.DrawLatex(-3.95,1.14,"#color[12]{150 fb}");
    cx.SetTextAngle(30);
    cx.DrawLatex(-3.9,0.85,"#color[12]{100 fb}");
    cx.SetTextAngle(35);
    cx.DrawLatex(-3.8,0.5,"#color[12]{50 fb}");
if (chan==2) :
    cx.SetTextAngle(30);
    cx.DrawLatex(-3.98,1.36,"#color[12]{30 fb}");
    cx.SetTextAngle(35);
    cx.DrawLatex(-3.8,0.5,"#color[12]{20 fb}");
if (chan==3) :
    cx.SetTextAngle(30);
    cx.DrawLatex(-3.98,1.4,"#color[12]{1000 fb}");
    cx.SetTextAngle(35);
    cx.DrawLatex(-4,0.95,"#color[12]{1500 fb}");
    #print (ff15dm15.Eval(-4,1))*(xs*BR)
axisc2kt.Draw()
text4.SetTextAngle(90)
text4.DrawLatex(-5.7,2.3,"#kappa_{t}")
cm15.Print(outfolder+"/c2_kt_klm15.png")
cm15.Close()
###################################
c15=TCanvas("c22","c22",200,50,600,600)
Histoc2kt15[0].SetNdivisions(0, "Y")
Histoc2kt15[0].Draw()
Histoc2kt15[0].SetTickLength(0.01, "X")
gPad.Update()
Histoc2kt15Exclu[0].Draw("same")
ff15d15.Draw("same")
for ii in range(1,nclu): 
    Histoc2kt15[ii].Draw("same")
    Histoc2kt15Exclu[ii].Draw("same")
#text.DrawLatex(-4.1,3.55,"#kappa_{#lambda} = -15 ; c_{g} = c_{2g} = 0")
text2.DrawLatex(-3.4,2.8,"(Assuming SM H decays)")
text.DrawLatex(3.8,2.45,"#kappa_{#lambda} = 15")
text3.DrawLatex(-3.5,3.55,channel)
text.DrawLatex(-3.8,3.88,warning)
textlumi.DrawLatex(1.8,3.85,lumi)
lineHc2ktpos.Draw("same")
lineTc2ktpos.Draw("same")
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
if (chan==3) :
    cx.SetTextAngle(-50);
    cx.DrawLatex(3.0,0.85,"#color[12]{500 fb}");
    cx.SetTextAngle(-57);
    cx.DrawLatex(4.0,1.5,"#color[12]{1000 fb}");
if (chan==2) :
    cx.SetTextAngle(-54);
    cx.DrawLatex(3.3,0.85,"#color[12]{20 fb}");
    cx.SetTextAngle(-50);
    cx.DrawLatex(1.95,0.8,"#color[12]{10 fb}");
if (chan==1) :
    cx.SetTextAngle(-54);
    cx.DrawLatex(3.45,0.85,"#color[12]{100 fb}");
    cx.SetTextAngle(-56);
    cx.DrawLatex(4.0,1.2,"#color[12]{150 fb}");
#print (ff15d15.Eval(3,1))*(xs*BR)
# kt axis
axisc2ktpos.Draw()
text4.SetTextAngle(90)
text4.DrawLatex(-4.8,2.3,"#kappa_{t}")
c15.Print(outfolder+"/c2_kt_kl15.png")
c15.Close()
###############################
# 12.5
###################################
cm12p5=TCanvas("c23","c23",200,50,600,600)
Histoc2ktm12p5[0].SetNdivisions(0, "Y")
Histoc2ktm12p5[0].Draw()
Histoc2kt12p5[0].SetTickLength(0.01, "X")
gPad.Update()
Histoc2ktm12p5Exclu[0].Draw("same")
ff15dm12p5.Draw("same")
for ii in range(1,nclu): 
    Histoc2ktm12p5[ii].Draw("same")
    Histoc2ktm12p5Exclu[ii].Draw("same")
#text.DrawLatex(-4.1,3.55,"#kappa_{#lambda} = -15 ; c_{g} = c_{2g} = 0")
text3.DrawLatex(-4.65,3.55,channel)
text2.DrawLatex(-4.5,2.8,"(Assuming SM H decays)")
text.DrawLatex(-4.6,2.45,"#scale[0.85]{#kappa_{#lambda} = -12.5}")
text.DrawLatex(-4.8,3.85,warning)
textlumi.DrawLatex(0.3,3.85,lumi)
lineHc2kt.Draw("same")
lineTc2kt.Draw("same")
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
if (chan==1) :
    cx.SetTextAngle(30);
    cx.DrawLatex(-4.1,1.73,"#color[12]{300 fb}");
    cx.SetTextAngle(30);
    cx.DrawLatex(-4.1,1.25,"#color[12]{200 fb}");
    cx.SetTextAngle(38);
    cx.DrawLatex(-4.1,0.9,"#color[12]{150 fb}");
#print ff15dm15.Eval(-3.0,2.0)*xs*BR
if (chan==2) :
    cx.SetTextAngle(33);
    cx.DrawLatex(-4.04,1.45,"#color[12]{50 fb}");
    cx.SetTextAngle(38);
    cx.DrawLatex(-3.8,0.55,"#color[12]{20 fb}");
if (chan==3) :
    cx.SetTextAngle(33);
    cx.DrawLatex(-3.95,1.14,"#color[12]{500 fb}");
    cx.SetTextAngle(38);
    cx.DrawLatex(-3.8,0.5,"#color[12]{300 fb}");
#print ff15dm15.Eval(-3.8,0.5)*xs*BR
axisc2kt.Draw()
text4.SetTextAngle(90)
text4.DrawLatex(-5.7,2.3,"#kappa_{t}")
cm12p5.Print(outfolder+"/c2_kt_klm12p5.png")
cm12p5.Close()
###################################
c12p5=TCanvas("c2","c2",200,50,600,600)
Histoc2kt12p5[0].SetNdivisions(0, "Y")
Histoc2kt12p5[0].Draw()
Histoc2kt12p5[0].SetTickLength(0.01, "XY")
gPad.Update()
Histoc2kt12p5Exclu[0].Draw("same")
ff15d12p5.Draw("same")
for ii in range(1,nclu): 
    Histoc2kt12p5[ii].Draw("same")
    Histoc2kt12p5Exclu[ii].Draw("same")
#text.DrawLatex(-4.1,3.55,"#kappa_{#lambda} = -15 ; c_{g} = c_{2g} = 0")
text3.DrawLatex(-3.5,3.55,channel)
text2.DrawLatex(-3.4,2.8,"(Assuming SM H decays)")
text.DrawLatex(3.6,2.45,"#kappa_{#lambda} = 12.5")
text.DrawLatex(-3.8,3.88,warning)
textlumi.DrawLatex(1.8,3.88,lumi)
lineHc2ktpos.Draw("same")
lineTc2ktpos.Draw("same")
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
if (chan==1) :
    cx.SetTextAngle(-68);
    cx.DrawLatex(4.4,1.25,"#color[12]{150 fb}");
    cx.SetTextAngle(-62);
    cx.DrawLatex(3.87,0.75,"#color[12]{100 fb}");
#print ff15d12p5.Eval(3,1.5)*xs*BR
if (chan==2) :
    cx.SetTextAngle(-65);
    cx.DrawLatex(3.65,0.85,"#color[12]{20 fb}");
    cx.SetTextAngle(-60);
    cx.DrawLatex(2.17,0.85,"#color[12]{10 fb}");
if (chan==3) :
    cx.SetTextAngle(-68);
    cx.DrawLatex(4.8,1.25,"#color[12]{1000 fb}");
    cx.SetTextAngle(-62);
    cx.DrawLatex(3.5,0.75,"#color[12]{500 fb}");
#    print ff15d12p5.Eval(3,1)*xs*BR
text2.DrawLatex(-19,1.2,"(Assuming SM H decays)")
# kt axis
axisc2ktpos.Draw()
text4.SetTextAngle(90)
text4.DrawLatex(-4.8,2.3,"#kappa_{t}")
c12p5.Print(outfolder+"/c2_kt_kl12p5.png")
c12p5.Close()
###############################
# 10.0
###################################
cm10p0=TCanvas("c2","c2",200,50,600,600)
Histoc2ktm10p0[0].SetNdivisions(0, "Y")
Histoc2ktm10p0[0].Draw()
Histoc2kt10p0[0].SetTickLength(0.01, "X")
gPad.Update()
Histoc2ktm10p0Exclu[0].Draw("same")
ff15dm10p0.Draw("same")
for ii in range(1,nclu): 
    Histoc2ktm10p0[ii].Draw("same")
    Histoc2ktm10p0Exclu[ii].Draw("same")
#text.DrawLatex(-4.1,3.55,"#kappa_{#lambda} = -15 ; c_{g} = c_{2g} = 0")
text3.DrawLatex(-4.7,3.55,channel)
text2.DrawLatex(-4.5,2.8,"(Assuming SM H decays)")
text.DrawLatex(-4.55,2.45,"#kappa_{#lambda} = -10")
text.DrawLatex(-4.8,3.85,warning)
textlumi.DrawLatex(0.3,3.85,lumi)
lineHc2kt.Draw("same")
lineTc2kt.Draw("same")
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
if (chan==1) :
    cx.SetTextAngle(38);
    cx.DrawLatex(-3.98,1.46,"#color[12]{300 fb}");
    cx.SetTextAngle(38);
    cx.DrawLatex(-3.98,1.1,"#color[12]{200 fb}");
    cx.SetTextAngle(48);
    cx.DrawLatex(-3.8,0.65,"#color[12]{150 fb}");
#print ff15dm15.Eval(-3.0,1.5)*xs*BR
if (chan==2) :
    cx.SetTextAngle(38);
    cx.DrawLatex(-3.98,1.65,"#color[12]{50 fb}");
    cx.SetTextAngle(48);
    cx.DrawLatex(-3.8,0.63,"#color[12]{10 fb}");
if (chan==3) :
    cx.SetTextAngle(38);
    cx.DrawLatex(-3.98,1.25,"#color[12]{1000 fb}");
    cx.SetTextAngle(48);
    cx.DrawLatex(-3.8,0.5,"#color[12]{500 fb}");
#print ff15dm15.Eval(-3.8,0.5)*xs*BR
axisc2kt.Draw()
text4.SetTextAngle(90)
text4.DrawLatex(-5.7,2.3,"#kappa_{t}")
cm10p0.Print(outfolder+"/c2_kt_klm10p0.png")
cm10p0.Close()
###################################
c10p0=TCanvas("c2","c2",200,50,600,600)
Histoc2kt10p0[0].SetNdivisions(0, "Y")
Histoc2kt10p0[0].Draw()
Histoc2kt10p0[0].SetTickLength(0.01, "X")
gPad.Update()
Histoc2kt10p0Exclu[0].Draw("same")
ff15d10p0.Draw("same")
for ii in range(1,nclu): 
    Histoc2kt10p0[ii].Draw("same")
    Histoc2kt10p0Exclu[ii].Draw("same")
#text.DrawLatex(-4.1,3.55,"#kappa_{#lambda} = -15 ; c_{g} = c_{2g} = 0")
text2.DrawLatex(-3.4,2.8,"(Assuming SM H decays)")
text.DrawLatex(3.6,2.45,"#kappa_{#lambda} = 10")
text3.DrawLatex(-3.5,3.55,channel)
text.DrawLatex(-3.8,3.88,warning)
textlumi.DrawLatex(1.8,3.85,lumi)
lineHc2ktpos.Draw("same")
lineTc2ktpos.Draw("same")
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
if (chan==1) :
    cx.SetTextAngle(-72);
    cx.DrawLatex(5.0,1.1,"#color[12]{200 fb}");
    cx.SetTextAngle(-69);
    cx.DrawLatex(4.17,0.8,"#color[12]{150 fb}");
#print ff15dm15.Eval(3.0,2.0)*xs*BR
if (chan==2) :
    cx.SetTextAngle(-67);
    cx.DrawLatex(3.93,0.85,"#color[12]{20 fb}");
    cx.SetTextAngle(-65);
    cx.DrawLatex(2.45,0.85,"#color[12]{10 fb}");
if (chan==3) :
    cx.SetTextAngle(-67);
    cx.DrawLatex(3.7,0.8,"#color[12]{500 fb}");
# kt axis
axisc2ktpos.Draw()
text4.SetTextAngle(90)
text4.DrawLatex(-4.8,2.3,"#kappa_{t}")
#print ff15dm15.Eval(-3.8,0.5)*xs*BR
c10p0.Print(outfolder+"/c2_kt_kl10p0.png")
c10p0.Close()
###############################
# 7.5
###################################
cm7p5=TCanvas("c2","c2",200,50,600,600)
Histoc2ktm7p5[0].SetNdivisions(0, "Y")
Histoc2ktm7p5[0].Draw()
Histoc2ktm7p5[0].SetTickLength(0.01, "X")
gPad.Update()
Histoc2ktm7p5Exclu[0].Draw("same")
ff15dm7p5.Draw("same")
for ii in range(1,nclu): 
    Histoc2ktm7p5[ii].Draw("same")
    Histoc2ktm7p5Exclu[ii].Draw("same")
#text.DrawLatex(-4.1,3.55,"#kappa_{#lambda} = -15 ; c_{g} = c_{2g} = 0")
if (chan==3 or chan==2) :text3.DrawLatex(-4.5,3.55,channel)
elif (chan==1) :text3.DrawLatex(-4.7,3.55,channel)
text2.DrawLatex(-4.5,2.8,"(Assuming SM H decays)")
text.DrawLatex(-4.55,2.45,"#scale[0.9]{#kappa_{#lambda} = -7.5 }")
text.DrawLatex(-4.8,3.9,warning)
textlumi.DrawLatex(0.3,3.85,lumi)
lineHc2kt.Draw("same")
lineTc2kt.Draw("same")
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
if (chan==1) :
    cx.SetTextAngle(44);
    cx.DrawLatex(-4.2,1.6,"#color[12]{200 fb}");
    cx.SetTextAngle(42);
    cx.DrawLatex(-4.2,1.2,"#color[12]{150 fb}");
    cx.SetTextAngle(53);
    cx.DrawLatex(-4,0.7,"#color[12]{100 fb}");
#print ff15dm7p5.Eval(-3,2)*xs*BR
if (chan==2) :
    cx.SetTextAngle(40);
    cx.DrawLatex(-4.2,1.83,"#color[12]{50 fb}");
    cx.SetTextAngle(55);
    cx.DrawLatex(-4,0.65,"#color[12]{20 fb}");
if (chan==3) :
    cx.SetTextAngle(40);
    cx.DrawLatex(-4.2,1.36,"#color[12]{1000 fb}");
    cx.SetTextAngle(55);
    cx.DrawLatex(-4,0.5,"#color[12]{500 fb}");
#print ff15dm7p5.Eval(-3,1)*xs*BR
axisc2kt.Draw()
text4.SetTextAngle(90)
text4.DrawLatex(-5.7,2.3,"#kappa_{t}")
cm7p5.Print(outfolder+"/c2_kt_klm7p5.png")
cm7p5.Close()
###################################
c7p5=TCanvas("c2","c2",200,50,600,600)
Histoc2kt7p5[0].SetNdivisions(0, "Y")
Histoc2kt7p5[0].Draw()
Histoc2kt7p5[0].SetTickLength(0.01, "X")
gPad.Update()
Histoc2kt7p5Exclu[0].Draw("same")
ff15d7p5.Draw("same")
for ii in range(1,nclu): 
    Histoc2kt7p5[ii].Draw("same")
    Histoc2kt7p5Exclu[ii].Draw("same")
#text.DrawLatex(-4.1,3.55,"#kappa_{#lambda} = -15 ; c_{g} = c_{2g} = 0")
text2.DrawLatex(-3.4,2.8,"(Assuming SM H decays)")
text.DrawLatex(3.6,2.45,"#kappa_{#lambda} = 7.5")
text3.DrawLatex(-3.5,3.55,channel)
text.DrawLatex(-3.8,3.88,warning)
textlumi.DrawLatex(1.8,3.85,lumi)
lineHc2ktpos.Draw("same")
lineTc2ktpos.Draw("same")
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
if (chan==1) :
    cx.SetTextAngle(-75);
    cx.DrawLatex(3.0,0.8,"#color[12]{100 fb}");
    cx.SetTextAngle(-76);
    cx.DrawLatex(4.35,0.88,"#color[12]{150 fb}");
#print ff15d7p5.Eval(3.0,0.5)*xs*BR
if (chan==2) :
    cx.SetTextAngle(-77);
    cx.DrawLatex(4.25,0.85,"#color[12]{20 fb}");
    cx.SetTextAngle(-75);
    cx.DrawLatex(2.8,0.85,"#color[12]{10 fb}");
if (chan==3) :
    cx.SetTextAngle(-75);
    cx.DrawLatex(3.0,0.8,"#color[12]{300 fb}");
    cx.SetTextAngle(-75);
    cx.DrawLatex(4.0,0.88,"#color[12]{500 fb}");
#print ff15d7p5.Eval(3.0,0.5)*xs*BR
# kt axis
axisc2ktpos.Draw()
text4.SetTextAngle(90)
text4.DrawLatex(-4.8,2.3,"#kappa_{t}")
c7p5.Print(outfolder+"/c2_kt_kl7p5.png")
c7p5.Close()
###############################
# 5.0
###################################
cm5p0=TCanvas("c2","c2",200,50,600,600)
Histoc2ktm5p0[0].SetNdivisions(0, "Y")
Histoc2ktm5p0[0].Draw()
Histoc2ktm5p0[0].SetTickLength(0.01, "X")
gPad.Update()
Histoc2ktm5p0Exclu[0].Draw("same")
ff15dm5p0.Draw("same")
for ii in range(1,nclu): 
    Histoc2ktm5p0[ii].Draw("same")
    Histoc2ktm5p0Exclu[ii].Draw("same")
#text.DrawLatex(-4.1,3.55,"#kappa_{#lambda} = -15 ; c_{g} = c_{2g} = 0")
if (chan==3 or chan==2) : text3.DrawLatex(-4.5,3.55,channel)
elif (chan==1) : text3.DrawLatex(-4.7,3.55,channel)
text2.DrawLatex(-4.5,2.8,"(Assuming SM H decays)")
text.DrawLatex(-4.55,2.45,"#scale[0.9]{#kappa_{#lambda} = -5.0 }")
text.DrawLatex(-4.8,3.9,warning)
textlumi.DrawLatex(0.3,3.85,lumi)
lineHc2kt.Draw("same")
lineTc2kt.Draw("same")
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
if (chan==1) :
    cx.SetTextAngle(45);
    cx.DrawLatex(-4.0,1.53,"#color[12]{150 fb}");
    cx.SetTextAngle(55);
    cx.DrawLatex(-4.0,0.9,"#color[12]{100 fb}");
#print ff15dm5p0.Eval(-3.0,2.0)*xs*BR
if (chan==2) :
    cx.SetTextAngle(60);
    cx.DrawLatex(-2.8,0.65,"#color[12]{10 fb}");
    cx.SetTextAngle(55);
    cx.DrawLatex(-4.25,0.65,"#color[12]{20 fb}");
if (chan==3) :
    cx.SetTextAngle(45);
    cx.DrawLatex(-4.0,1.68,"#color[12]{1000 fb}");
    cx.SetTextAngle(55);
    cx.DrawLatex(-4.0,0.65,"#color[12]{500 fb}");
#print ff15dm5p0.Eval(-3.0,1.0)*xs*BR
# [5/(xs*BR),10/(xs*BR),20/(xs*BR),50/(xs*BR),--100/(xs*BR),300/(xs*BR),500/(xs*BR),1000/(xs*BR),1500/(xs*BR)]
axisc2kt.Draw()
text4.SetTextAngle(90)
text4.DrawLatex(-5.7,2.3,"#kappa_{t}")
cm5p0.Print(outfolder+"/c2_kt_klm5p0.png")
cm5p0.Close()
###################################
c5p0=TCanvas("c2","c2",200,50,600,600)
Histoc2kt5p0[0].SetNdivisions(0, "Y")
Histoc2kt5p0[0].Draw()
Histoc2kt5p0[0].SetTickLength(0.01, "X")
gPad.Update()
Histoc2kt5p0Exclu[0].Draw("same")
ff15d5p0.Draw("same")
for ii in range(1,nclu): 
    Histoc2kt5p0[ii].Draw("same")
    Histoc2kt5p0Exclu[ii].Draw("same")
#text.DrawLatex(-4.1,3.55,"#kappa_{#lambda} = -15 ; c_{g} = c_{2g} = 0")
text2.DrawLatex(-3.4,2.8,"(Assuming SM H decays)")
text.DrawLatex(3.6,2.45,"#kappa_{#lambda} = 5.0")
text3.DrawLatex(-3.5,3.55,channel)
text.DrawLatex(-3.8,3.88,warning)
textlumi.DrawLatex(1.8,3.85,lumi)
lineHc2ktpos.Draw("same")
lineTc2ktpos.Draw("same")
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
if (chan==1) :
    cx.SetTextAngle(-80);
    cx.DrawLatex(3.2,0.8,"#color[12]{50 fb}");
    cx.SetTextAngle(-90);
    cx.DrawLatex(4.7,0.88,"#color[12]{100 fb}");
#print ff15dm5p0.Eval(4.6,0.5)*xs*BR
if (chan==2) :
    cx.SetTextAngle(-87);
    cx.DrawLatex(4.55,0.85,"#color[12]{20 fb}");
    cx.SetTextAngle(-85);
    cx.DrawLatex(3.15,0.85,"#color[12]{10 fb}");
if (chan==3) :
    cx.SetTextAngle(-80);
    cx.DrawLatex(3.2,0.8,"#color[12]{300 fb}");
    cx.SetTextAngle(-80);
    cx.DrawLatex(4.2,0.88,"#color[12]{500 fb}");
#print ff15dm5p0.Eval(3.0,0.5)*xs*BR
text2.DrawLatex(-19,1.2,"(Assuming SM H decays)")
# kt axis
axisc2ktpos.Draw()
text4.SetTextAngle(90)
text4.DrawLatex(-4.8,2.3,"#kappa_{t}")
c5p0.Print(outfolder+"/c2_kt_kl5p0.png")
c5p0.Close()
###############################
# 3.5
###################################
cm3p5=TCanvas("c2","c2",200,50,600,600)
Histoc2ktm3p5[0].SetNdivisions(0, "Y")
Histoc2ktm3p5[0].Draw()
Histoc2ktm3p5[0].SetTickLength(0.01, "X")
gPad.Update()
Histoc2ktm3p5Exclu[0].Draw("same")
ff15dm3p5.Draw("same")
for ii in range(1,nclu): 
    Histoc2ktm3p5[ii].Draw("same")
    Histoc2ktm3p5Exclu[ii].Draw("same")
#text.DrawLatex(-4.1,3.55,"#kappa_{#lambda} = -15 ; c_{g} = c_{2g} = 0")
if (chan==3 or chan ==2) :text3.DrawLatex(-4.5,3.55,channel)
elif (chan==1) :text3.DrawLatex(-4.7,3.55,channel)
text2.DrawLatex(-4.5,2.8,"(Assuming SM H decays)")
text.DrawLatex(-4.55,2.45,"#scale[0.9]{#kappa_{#lambda} = -3.5 }")
text.DrawLatex(-4.8,3.9,warning)
textlumi.DrawLatex(0.3,3.85,lumi)
lineHc2kt.Draw("same")
lineTc2kt.Draw("same")
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
if (chan==1) :
    cx.SetTextAngle(55);
    cx.DrawLatex(-4.25,0.9,"#color[12]{100 fb}");
    cx.SetTextAngle(65);
    cx.DrawLatex(-3.25,0.5,"#color[12]{50 fb}");
if (chan==2) :
    cx.SetTextAngle(60);
    cx.DrawLatex(-2.98,0.65,"#color[12]{10 fb}");
    cx.SetTextAngle(60);
    cx.DrawLatex(-4.4,0.65,"#color[12]{20 fb}");
if (chan==3) :
    cx.SetTextAngle(65);
    cx.DrawLatex(-4.25,0.5,"#color[12]{500 fb}");
    cx.SetTextAngle(65);
    cx.DrawLatex(-3.25,0.5,"#color[12]{300 fb}");
#print ff15dm3p5.Eval(-4,0.5)*xs*BR
axisc2kt.Draw()
text4.SetTextAngle(90)
text4.DrawLatex(-5.7,2.3,"#kappa_{t}")
cm3p5.Print(outfolder+"/c2_kt_klm3p5.png")
cm3p5.Close()
###################################
c3p5=TCanvas("c2","c2",200,50,600,600)
Histoc2kt3p5[0].SetNdivisions(0, "Y")
Histoc2kt3p5[0].Draw()
Histoc2kt3p5[0].SetTickLength(0.01, "X")
gPad.Update()
Histoc2kt3p5Exclu[0].Draw("same")
ff15d3p5.Draw("same")
for ii in range(1,nclu): 
    Histoc2kt3p5[ii].Draw("same")
    Histoc2kt3p5Exclu[ii].Draw("same")
#text.DrawLatex(-4.1,3.55,"#kappa_{#lambda} = -15 ; c_{g} = c_{2g} = 0")
text3.DrawLatex(-3.5,3.55,channel)
text2.DrawLatex(-3.5,2.8,"(Assuming SM H decays)")
text.DrawLatex(3.6,2.45,"#scale[0.9]{#kappa_{#lambda} = 3.5 }")
text.DrawLatex(-3.8,3.9,warning)
textlumi.DrawLatex(1.8,3.85,lumi)
lineHc2ktpos.Draw("same")
lineTc2ktpos.Draw("same")
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
if (chan==1) :
    cx.SetTextAngle(-88);
    cx.DrawLatex(3.45,0.8,"#color[12]{50 fb}");
    cx.SetTextAngle(-88);
    cx.DrawLatex(4.85,0.88,"#color[12]{100 fb}");
#print ff15d3p5.Eval(3.0,0.5)*xs*BR
if (chan==2) :
    cx.SetTextAngle(-93);
    cx.DrawLatex(4.7,0.85,"#color[12]{20 fb}");
    cx.SetTextAngle(-93);
    cx.DrawLatex(3.35,0.85,"#color[12]{10 fb}");
if (chan==3) :
    cx.SetTextAngle(-90);
    cx.DrawLatex(3.45,0.8,"#color[12]{300 fb}");
    cx.SetTextAngle(-88);
    cx.DrawLatex(4.45,0.88,"#color[12]{500 fb}");
#print ff15d3p5.Eval(3.0,0.5)*xs*BR
# kt axis
axisc2ktpos.Draw()
text4.SetTextAngle(90)
text4.DrawLatex(-4.8,2.3,"#kappa_{t}")
c3p5.Print(outfolder+"/c2_kt_kl3p5.png")
c3p5.Close()
###############################
# 2.4
###################################
cm2p4=TCanvas("c2","c2",200,50,600,600)
Histoc2ktm2p4[0].SetNdivisions(0, "Y")
Histoc2ktm2p4[0].Draw()
Histoc2ktm2p4[0].SetTickLength(0.01, "X")
gPad.Update()
Histoc2ktm2p4Exclu[0].Draw("same")
ff15dm2p4.Draw("same")
for ii in range(1,nclu): 
    Histoc2ktm2p4[ii].Draw("same")
    Histoc2ktm2p4Exclu[ii].Draw("same")
#text.DrawLatex(-4.1,3.55,"#kappa_{#lambda} = -15 ; c_{g} = c_{2g} = 0")
if (chan==3 or chan ==2) :text3.DrawLatex(-4.5,3.55,channel)
elif (chan==1) :text3.DrawLatex(-4.7,3.55,channel)
text2.DrawLatex(-4.5,2.8,"(Assuming SM H decays)")
text.DrawLatex(-4.55,2.45,"#scale[0.9]{#kappa_{#lambda} = -2.4 }")
text.DrawLatex(-4.8,3.9,warning)
textlumi.DrawLatex(0.3,3.85,lumi)
lineHc2kt.Draw("same")
lineTc2kt.Draw("same")
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
if (chan==1) :
    cx.SetTextAngle(58);
    cx.DrawLatex(-4.32,0.95,"#color[12]{100 fb}");
    cx.SetTextAngle(65);
    cx.DrawLatex(-3.32,0.5,"#color[12]{50 fb}");
if (chan==2) :
    cx.SetTextAngle(60);
    cx.DrawLatex(-3.1,0.65,"#color[12]{10 fb}");
    cx.SetTextAngle(60);
    cx.DrawLatex(-4.3,0.85,"#color[12]{20 fb}");
if (chan==3) :
    cx.SetTextAngle(65);
    cx.DrawLatex(-4.32,0.5,"#color[12]{500 fb}");
    cx.SetTextAngle(65);
    cx.DrawLatex(-3.32,0.5,"#color[12]{300 fb}");
#print ff15dm2p4.Eval(-4,0.5)*xs*BR
axisc2kt.Draw()
text4.SetTextAngle(90)
text4.DrawLatex(-5.7,2.3,"#kappa_{t}")
cm2p4.Print(outfolder+"/c2_kt_klm2p4.png")
cm2p4.Close()
###################################
c2p4=TCanvas("c2","c2",200,50,600,600)
Histoc2kt2p4[0].SetNdivisions(0, "Y")
Histoc2kt2p4[0].Draw()
Histoc2kt2p4[0].SetTickLength(0.01, "X")
gPad.Update()
Histoc2kt2p4Exclu[0].Draw("same")
ff15d2p4.Draw("same")
for ii in range(1,nclu): 
    Histoc2kt2p4[ii].Draw("same")
    Histoc2kt2p4Exclu[ii].Draw("same")
#text.DrawLatex(-4.1,3.55,"#kappa_{#lambda} = -15 ; c_{g} = c_{2g} = 0")
text3.DrawLatex(-4.5,3.55,channel)
text2.DrawLatex(-4.5,2.8,"(Assuming SM H decays)")
text.DrawLatex(-4.5,2.45,"#scale[0.9]{#kappa_{#lambda} = 2.4 }")
text.DrawLatex(-4.8,3.9,warning)
textlumi.DrawLatex(0.3,3.85,lumi)
lineHc2kt.Draw("same")
lineTc2kt.Draw("same")
leg.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
if (chan==1) :
    cx.SetTextAngle(65);
    cx.DrawLatex(-4.4,1.65,"#color[12]{100 fb}");
    cx.SetTextAngle(83);
    cx.DrawLatex(-3.65,0.5,"#color[12]{50 fb}");
#print ff15d2p4.Eval(-3.0,1.5)*xs*BR
if (chan==2) :
    cx.SetTextAngle(80);
    cx.DrawLatex(-3.55,0.65,"#color[12]{10 fb}");
    cx.SetTextAngle(65);
    cx.DrawLatex(-4.4,1.5,"#color[12]{20 fb}");
if (chan==3) :
    cx.SetTextAngle(71);
    cx.DrawLatex(-4.3,1.3,"#color[12]{500 fb}");
    cx.SetTextAngle(80);
    cx.DrawLatex(-3.7,0.5,"#color[12]{300 fb}");
#    print ff15d2p4.Eval(-3.8,0.5)*xs*BR
# kt axis
axisc2kt.Draw()
text4.SetTextAngle(90)
text4.DrawLatex(-5.7,2.3,"#kappa_{t}")
c2p4.Print(outfolder+"/c2_kt_kl2p4.png")
c2p4.Close()
########################
if(type==2) : 
  cspread=TCanvas("c2","c2",200,50,600,600)
  spread.Draw("A*")
  bench.Draw("same,*")
  cspread.SetLogy(1)
  cspread.Print(outfolder+"/spread.png")
  cspread.Close()


