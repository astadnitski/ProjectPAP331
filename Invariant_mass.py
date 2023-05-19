import ROOT
from array import array
import numpy as np

def norm(xsec, N): return 300 * float(xsec) / int(N)

def invar_mass(channel):

    # Open the ROOT file
    FILE = ROOT.TFile.Open(('Root/Level2/' + channel + '.root'), 'READ')
    Muons = FILE.Get('Muons')
    
    FILE_F = ROOT.TFile.Open(('Root/InvariantMass/' + channel + '.root'), 'RECREATE')
    Muons_F = ROOT.TTree('Muons', 'Invariant mass of muons')
    xsection = FILE.Get('Cross section')
    events = FILE.Get('Total events')

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

        if inMass[0] == 0:
            continue

        Muons_F.Fill()
    
    # Write and close the output ROOT file
    xsection.Write()
    events.Write()
    FILE_F.Write()
    FILE_F.Close()
    FILE.Close()

def makePlots(channel1, channel2, channel3):
    
    # Open the ROOT file containing the histograms
    signal = ROOT.TFile.Open('Root/InvariantMass/' + channel1 + '.root', 'READ')
    drellyan = ROOT.TFile.Open('Root/InvariantMass/' + channel2 + '.root', 'READ')
    ttbar = ROOT.TFile.Open('Root/InvariantMass/' + channel3 + '.root', 'READ')

    signal_tree = signal.Get('Muons')
    drellyan_tree = drellyan.Get('Muons')
    ttbar_tree = ttbar.Get('Muons')

    canvas = ROOT.TCanvas('canvas', 'Invariant mass of muons', 1280, 430)
    canvas.Divide(3, 1)

    N_signal = signal.Get('Total events').GetTitle()
    N_drellyan = drellyan.Get('Total events').GetTitle()
    N_ttbar = ttbar.Get('Total events').GetTitle()

    # These numbers are for 13 TeV, multiplied by 1e3 to convert picobarns to femtobarns
    xsec_signal = 54133.8 * 2.176e-4
    xsec_drellyan = (135281.434721 / 81150179.769282) * 6025.2 * 1e3
    xsec_ttbar = 831.76 * 1e3

    norm_signal = norm(xsec_signal, N_signal)
    norm_drellyan = norm(xsec_drellyan, N_drellyan)
    norm_ttbar = norm(xsec_ttbar, N_ttbar)

    print('Signal: 300/fb * ' + str(xsec_signal) + ' fb / ' + str(N_signal) + ' = ' + str(norm_signal))
    print('Drell-Yan: 300/fb * ' + str(xsec_drellyan) + ' fb / ' + str(N_drellyan) + ' = ' + str(norm_drellyan))
    print('TTbar: 300/fb * ' + str(xsec_ttbar) + ' fb / ' + str(N_ttbar) + ' = ' + str(norm_ttbar))

    bins, xmin, xmax = 60, 0, 400

    hist_signal = ROOT.TH1F('hist_signal',
                            'Signal (norm: ' + str(norm_signal) + ')',
                            bins, xmin, xmax)
    hist_drellyan = ROOT.TH1F('hist_drellyan',
                              'Drell-Yan background (norm: ' + str(norm_drellyan) + ')',
                              bins, xmin, xmax)
    hist_ttbar = ROOT.TH1F('hist_ttbar',
                           'TTbar background (norm: ' + str(norm_ttbar) + ')',
                           bins, xmin, xmax)

    canvas.cd(1)
    signal_tree.Draw('inMass>>hist_signal')
    hist_signal.Scale(norm_signal, option = 'nosw2')
    hist_signal.GetXaxis().SetTitle('Invariant mass [GeV]')
    hist_signal.GetXaxis().CenterTitle(True)
    hist_signal.SetLineColor(1)
    hist_signal.SetFillColor(3)

    canvas.cd(2)
    drellyan_tree.Draw('inMass>>hist_drellyan')
    hist_drellyan.Scale(norm_drellyan, option = 'nosw2')
    hist_drellyan.GetXaxis().SetTitle('Invariant mass [GeV]')
    hist_drellyan.GetXaxis().CenterTitle(True)
    hist_drellyan.SetLineColor(1)
    hist_drellyan.SetFillColor(4)

    canvas.cd(3)
    ttbar_tree.Draw('inMass>>hist_ttbar')
    hist_ttbar.Scale(norm_ttbar, option = 'nosw2')
    hist_ttbar.GetXaxis().SetTitle('Invariant mass [GeV]')
    hist_ttbar.GetXaxis().CenterTitle(True)
    hist_ttbar.SetLineColor(1)
    hist_ttbar.SetFillColor(2)

    canvas.Print('Plots/Channels.png')

    hist_bg = ROOT.TH1F('hist_bg', 'Background', bins, xmin, xmax)
    hist_total = ROOT.TH1F('hist_total', 'Background + Signal', bins, xmin, xmax)
    canvas = ROOT.TCanvas('canvas', 'Invariant mass of muons', 1280, 660)
    canvas.Divide(2, 1)

    canvas.cd(1)
    drellyan_tree.Draw('inMass>>hist_bg')
    hist_bg.Add(hist_drellyan, hist_ttbar)
    hist_bg.GetXaxis().SetNdivisions(-8)
    hist_bg.GetXaxis().SetTitle('Invariant mass [GeV]')
    hist_bg.GetXaxis().CenterTitle(True)
    hist_bg.SetAxisRange(0, 65000, 'Y')
    hist_bg.SetLineColor(1)
    hist_bg.SetFillColor(880)

    fit_background = ROOT.TF1('fit_background', "landau", 120, 130)
    fit_background.SetLineColor(ROOT.kBlack)
    hist_bg.Fit(fit_background)
    hist_bg.Fit(fit_background)
    hist_bg.Draw()
    fit_background.Draw('same')
    canvas.Update()

    canvas.cd(2)
    drellyan_tree.Draw('inMass>>hist_total')
    hist_total.Add(hist_bg, hist_signal)
    hist_total.GetXaxis().SetNdivisions(-8)
    hist_total.GetXaxis().SetTitle('Invariant mass [GeV]')
    hist_total.GetXaxis().CenterTitle(True)
    hist_total.SetAxisRange(0, 65000, 'Y')
    hist_total.SetLineColor(1)
    hist_total.SetFillColor(13)
    
    fit_total = ROOT.TF1('fit_total', "landau", 120, 130)
    fit_total.SetLineColor(ROOT.kRed)
    hist_total.Fit(fit_total)
    hist_total.Draw()
    fit_total.Draw('same')
    canvas.Update()
    
    # Save the canvas as a PDF file
    canvas.SaveAs('Plots/Invariant_mass.pdf')
    canvas.SaveAs('Plots/Invariant_mass.png')
    canvas.SaveAs('Plots/Invariant_mass.root')

    # Close the ROOT files
    signal.Close()
    drellyan.Close()
    ttbar.Close()

    return norm_signal, norm_drellyan, norm_ttbar

def statsig(channel):
    FILE = ROOT.TFile.Open(('Root/Level2/' + channel + '.root'), 'READ')
    EventIDs = []
    for muon in FILE.Get('Muons'): EventIDs.append(muon.Event)
    return len(set(EventIDs))

def main():

    invar_mass('signal')
    invar_mass('drellyan')
    invar_mass('ttbar') 

    norm_signal, norm_drellyan, norm_ttbar = makePlots('signal', 'drellyan', 'ttbar')
    
    count_signal = statsig('signal') * norm_signal
    count_drellyan = statsig('drellyan') * norm_drellyan
    count_ttbar = statsig('ttbar') * norm_ttbar

    print('Statistical signifigance: ' + str(count_signal / np.sqrt(count_drellyan + count_ttbar)))

if __name__ == '__main__': main() 
