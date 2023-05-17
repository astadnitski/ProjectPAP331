import ROOT
from array import array
import numpy as np

def BreitWigner(x, par): return par[0] / ((x[0] - par[1])**2 + 0.25 * par[2]**2)

def Landau(x, par): return par[0] * np.exp(-0.5 * ((x[0] - par[1]) / par[2])**2)

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

        #print("inMass = ", inMass[0])

        if inMass[0] == 0:
            continue

        # inMass[0] =((muon_vector + antimuon_vector).M()) * float(normalization)
        Muons_F.Fill()
    
    # Write and close the output ROOT file
    xsection.Write()
    events.Write()
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

    # These numbers come from Pythia, inaccurate - may be off by orders of magnitude
    #xsec_signal = signal.Get('Cross section').GetTitle()
    #xsec_drellyan = drellyan.Get('Cross section').GetTitle()
    #xsec_ttbar = ttbar.Get('Cross section').GetTitle()

    # These numbers come from Sami, multiplied by 1e3 to convert picobarns to femtobarns
    xsec_drellyan = (135281.434721 / 81150179.769282) * 6025.2 * 1e3
    xsec_ttbar = 831.76 * 1e3   
    # This I am not sure about, calculated manually. Supposed to be Higgs cross section * H -> mu mu BR
    xsec_signal = 54133.8 * 2.176e-4

    norm_signal = norm(xsec_signal, N_signal)
    norm_drellyan = norm(xsec_drellyan, N_drellyan)
    norm_ttbar = norm(xsec_ttbar, N_ttbar)

    print 'Signal: 300/fb * ' + str(xsec_signal) + ' fb / ' + str(N_signal) + ' = ' + str(norm_signal)
    print 'Drell-Yan: 300/fb * ' + str(xsec_drellyan) + ' fb / ' + str(N_drellyan) + ' = ' + str(norm_drellyan)
    print 'TTbar: 300/fb * ' + str(xsec_ttbar) + ' fb / ' + str(N_ttbar) + ' = ' + str(norm_ttbar)

    hist_signal = ROOT.TH1F('hist_signal',
                            'Signal (norm: ' + str(norm_signal) + ')',
                            50, 0, 200)
    hist_drellyan = ROOT.TH1F('hist_drellyan',
                              'Drell-Yan background (norm: ' + str(norm_drellyan) + ')',
                              50, 0, 200)
    hist_ttbar = ROOT.TH1F('hist_ttbar',
                           'TTbar background (norm: ' + str(norm_ttbar) + ')',
                           50, 0, 200)

    canvas.cd(1)
    signal_tree.Draw('inMass>>hist_signal')
    hist_signal.Scale(norm_signal, option = 'nosw2')
    hist_signal.GetXaxis().SetTitle('Invariant mass [GeV]')
    hist_signal.GetXaxis().CenterTitle(True)
    hist_signal.SetLineColor(1)
    hist_signal.SetFillColor(3)
    #hist_signal.Scale(2.293311, option = 'nosw2')

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

    canvas.Print("Plots/Channels.png")

    hist_bg = ROOT.TH1F('hist_bg', 'Background', 50, 0, 200)
    hist_total = ROOT.TH1F('hist_total', 'Background + Signal', 50, 0, 200)
    canvas = ROOT.TCanvas('canvas', 'Invariant mass of muons', 1280, 660)
    canvas.Divide(2, 1)

    canvas.cd(1)
    drellyan_tree.Draw('inMass>>hist_bg')
    hist_bg.Add(hist_drellyan, hist_ttbar)
    hist_bg.GetXaxis().SetNdivisions(-8)
    hist_bg.GetXaxis().SetTitle('Invariant mass [GeV]')
    hist_bg.GetXaxis().CenterTitle(True)
    hist_bg.SetAxisRange(0, 45000, 'Y')
    hist_bg.SetLineColor(1)
    hist_bg.SetFillColor(880)
    hist_bg.Draw()

    canvas.cd(2)
    drellyan_tree.Draw('inMass>>hist_total')
    hist_total.Add(hist_drellyan, hist_ttbar)
    hist_total.Add(hist_bg, hist_signal)
    hist_total.GetXaxis().SetNdivisions(-8)
    hist_total.GetXaxis().SetTitle('Invariant mass [GeV]')
    hist_total.GetXaxis().CenterTitle(True)
    hist_total.SetAxisRange(0, 45000, 'Y')
    hist_total.SetLineColor(1)
    hist_total.SetFillColor(13)
    hist_total.Draw()

    canvas.Print("Plots/SignalComparison.png")

    # Close the ROOT files
    signal.Close()
    drellyan.Close()
    ttbar.Close()


def main():

    #invar_mass('signal')
    #invar_mass('drellyan')
    #invar_mass('ttbar') 

    #fit('signal', 'drellyan', 'ttbar')
    makePlots('signal', 'drellyan', 'ttbar')

if __name__ == '__main__': main() 