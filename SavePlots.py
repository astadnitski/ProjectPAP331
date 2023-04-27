#/usr/bin/env python
from array import array
import ROOT

def makePlot(channel, particle, name):

    canvas = ROOT.TCanvas('Canvas', '', 600, 450)
    canvas.SetFillColor(0)
    canvas.cd()
    
    pT = array('f', [0])
    particle.Branch('pT', pT, 'pT')
    hist = ROOT.TH1F('hist', channel + ' ' + name + ' pT', 100, 0, 900) 
    for i in particle: hist.Fill(i.pT)

    if 'anti' in name: hist.SetFillColor(2)
    else: hist.SetFillColor(4)

    hist.GetXaxis().SetTitle('pT')
    hist.GetXaxis().CenterTitle(True)
    hist.GetYaxis().SetRangeUser(0, 2500)

    hist.SetStats(0)
    hist.Draw()
    canvas.Print('Plots/' + channel + name + '.png')

def savePlot(channel):
    data = ROOT.TFile.Open('Root/' + channel + '.root', 'READ')
    makePlot(channel, data.Get('muon'), 'muon')
    makePlot(channel, data.Get('antimuon'), 'antimuon')

def main():
    savePlot('signal')
    savePlot('drellyan')
    savePlot('ttbar')    

if __name__ == '__main__': main()