import ROOT
from array import array
import numpy as np

def BreitWigner(x, par):
    return par[0] / ((x[0] - par[1])**2 + 0.25 * par[2]**2)

def Landau(x, par):
    return par[0] * np.exp(-0.5 * ((x[0] - par[1]) / par[2])**2)

def invar_mass(channel):

    # Open the ROOT file
    FILE = ROOT.TFile.Open(('Root/Level2/' + channel + '.root'), 'READ')
    Muons = FILE.Get('Muons')
    normalization = FILE.Get('Normalization').GetTitle()

    print("normalization = ", normalization)
    
    FILE_F = ROOT.TFile.Open(('Root/InvariantMass/' + channel + '.root'), 'RECREATE')
    Muons_F = ROOT.TTree('Muons', 'Invariant mass of muons')

    inMass = array('f', [0])
    Muons_F.Branch('inMass', inMass, 'inMass/F')

    # Create TLorentzVector objects for muons
    muon_vector = ROOT.TLorentzVector()
    antimuon_vector = ROOT.TLorentzVector()

    muons = []
    event = []

    for muon in Muons:
        muons.append([muon.Event, muon.pT, muon.eta, muon.charge, muon.phi, muon.theta, muon.m])

    finish = muons[-1][0] + 1

    for i in range(finish):
        muonsInEvent = []
        for muon in muons:
            if muon[0] == i:
                muonsInEvent.append(muon)
        event.append(muonsInEvent)

    # print("event = ", event)

    for oneEvent in event:
        muonmaxPt = 0.0
        antimuonmaxPt = 0.0

        temppart_muon = [0] * 7
        temppart_anti = [0] * 7

        for particle in oneEvent:
            if particle[3] == 1 and particle[1] > muonmaxPt:
                muonmaxPt = particle[1]
                temppart_muon = particle

            elif particle[3] == -1 and particle[1] > antimuonmaxPt:
                antimuonmaxPt = particle[1]
                temppart_anti = particle
        
        muon_vector.SetPtEtaPhiM(temppart_muon[1], temppart_muon[2], temppart_muon[4], temppart_muon[6])
        antimuon_vector.SetPtEtaPhiM(temppart_anti[1], temppart_anti[2], temppart_anti[4], temppart_anti[6])
        inMass[0] = (muon_vector+antimuon_vector).M()

        print("inMass = ", inMass[0])

        if inMass[0] == 0:
            continue

        # inMass[0] =((muon_vector + antimuon_vector).M()) * float(normalization)
        Muons_F.Fill()
    
    # Write and close the output ROOT file
    FILE_F.Write()
    FILE_F.Close()
    FILE.Close()

def fit(channel1, channel2, channel3):
    
    # Open the ROOT file containing the histograms
    signal = ROOT.TFile.Open('Root/InvariantMass/' + channel1 + '.root', 'READ')
    drellyan = ROOT.TFile.Open('Root/InvariantMass/' + channel2 + '.root', 'READ')
    ttbar = ROOT.TFile.Open('Root/InvariantMass/' + channel3 + '.root', 'READ')

    # Get the invariant mass trees
    signal_tree = signal.Get('Muons')
    drellyan_tree = drellyan.Get('Muons')
    ttbar_tree = ttbar.Get('Muons')

    # signalmass = array('f', [0])
    # drellyanmass = array('f', [0])
    # ttbarmass = array('f', [0])

    # signalbranch = signal_tree.GetBranch('inMass')
    # drellyanbranch = drellyan_tree.GetBranch('inMass')
    # ttbarbranch = ttbar_tree.GetBranch('inMass')

    # # Set the branch address
    # signalbranch.SetAddress(signalmass)
    # drellyanbranch.SetAddress(drellyanmass)
    # ttbarbranch.SetAddress(ttbarmass)

    # Create a canvas and draw the histograms
    canvas = ROOT.TCanvas('canvas', 'Invariant mass of muons', 1000, 1000)

    canvas.Divide(2, 1)

    pad1 = canvas.cd(1)

    # Create a histogram for the invariant mass
    hist_signal = ROOT.TH1F('hist_signal', 'Invariant mass of muons', 100, 124, 126)
    hist_drellyan = ROOT.TH1F('hist_drellyan', 'Invariant mass of muons', 100, 0, 126)
    hist_ttbar = ROOT.TH1F('hist_ttbar', 'Invariant mass of muons', 100, 0, 126)

    # Fill the histograms
    signal_tree.Draw('inMass>>hist_signal')
    drellyan_tree.Draw('inMass>>hist_drellyan')
    ttbar_tree.Draw('inMass>>hist_ttbar')

    # Create a background histogram
    # hist_background = hist_drellyan

    hist_background = hist_drellyan.Clone("hist_background")

    hist_background.Add(hist_background, hist_ttbar, 1.0, 1.0)

    # hist_total = hist_signal

    hist_total = hist_signal.Clone("hist_total")
    hist_total.Add(hist_total, hist_background, 1.0, 1.0)

    fit_total = ROOT.TF1('fit_total', BreitWigner,  0, 126, 3)
    fit_total.SetParameters(100, 125, 1)
    fit_total.SetParNames('Constant', 'Mean', 'Gamma')
    fit_total.SetLineColor(ROOT.kRed)

    # # Create a legend and add the histograms to it
    # legend = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)
    # legend.AddEntry(hist_total, 'Signal + Background', 'l')
    # legend.AddEntry(hist_background, 'Background', 'l')
    # legend.AddEntry(fit_total, 'Breit-Wigner', 'l')

    # # Draw the legend
    # legend.Draw()

    # Fit the histograms with the Breit-Wigner function
    hist_total.Fit(fit_total)

    # Draw the histograms
    hist_total.Draw()

    pad2 = canvas.cd(2)

    fit_background = ROOT.TF1('fit_background', Landau, 90, 93, 3)
    fit_background.SetParameters(90, 93, 1)
    fit_background.SetParNames('Constant', 'Mean', 'Sigma')
    fit_background.SetLineColor(ROOT.kBlack)

    hist_background.Fit(fit_background)

    hist_background.Draw()

    # Save the canvas as a PDF file
    canvas.SaveAs('Plots/' + channel1 + '.pdf')
    canvas.Print("Plots/TEST1.png")

    # Close the ROOT files
    signal.Close()
    drellyan.Close()
    ttbar.Close()

def main():

    invar_mass('signal')
    invar_mass('drellyan')
    invar_mass('ttbar') 

    fit('signal', 'drellyan', 'ttbar')

if __name__ == '__main__': main() 