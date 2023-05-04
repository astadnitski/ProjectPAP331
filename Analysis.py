#!/usr/bin/env python

from array import array
from ROOT import *
import numpy as np

def analyze(channel):

    FILE = TFile.Open(('Root/Level0/' + channel + '.root'), 'READ')
    Muons, Pions = FILE.Get('Muons'), FILE.Get('Pions')
    
    FILE_F = TFile.Open(('Root/Level1/' + channel + '.root'), 'RECREATE')
    Muons_F = TTree('Muons', 'Muons passing the IsoMu20_eta2p1 trigger')
    
    Event = array('i', [0])
    Muons_F.Branch('Event', Event, 'Event/I')

    pT = array('f', [0])
    Muons_F.Branch('pT', pT, 'pT/F')

    eta = array('f', [0])
    Muons_F.Branch('eta', eta, 'eta/F')

    charge = array('f', [0])
    Muons_F.Branch('charge', charge, 'charge/F')

    phi = array('f', [0])
    Muons_F.Branch('phi', phi, 'phi/F')

    mass = array('f', [0])
    Muons_F.Branch('mass', mass, 'mass/F')

    # This is just for helping to visualize stuff by printing arrays, will be removed later.
    ar = np.zeros([Muons.GetEntries(), 7]) # Could be also [, 6] if we throw out trigger flag

    for i, muon in enumerate(Muons): # Remove enumerate() if not needed

        if muon.IsoMu20_eta2p1:
            
            Event[0] = muon.Event
            pT[0] = muon.pT
            eta[0] = muon.eta
            charge[0] = muon.charge
            phi[0] = muon.phi
            mass[0] = muon.mass
            Muons_F.Fill()

            ar[i] = [muon.Event, True, muon.pT, muon.eta, muon.charge, muon.phi, muon.mass]


    Muons_F.Write()
    FILE_F.Close()

    #print(len(ar[:, 1]))
    #print(np.sum(ar[:, 1]))
    #print(ar[:, 1])

    print 'Finished analyzing ' + channel

def main():
    analyze('signal')
    analyze('drellyan')
    analyze('ttbar')

if __name__ == '__main__': main()