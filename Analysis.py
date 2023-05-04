#!/usr/bin/env python

from array import array
from ROOT import *
import numpy as np

def smear(): return np.random.normal(0, 0.1, 1)#[0] # Mean, standard deviation, length of output array

def filter0(channel):

    FILE = TFile.Open(('Root/Level0/' + channel + '.root'), 'READ')
    Muons, Pions = FILE.Get('Muons'), FILE.Get('Pions')
    
    FILE_F = TFile.Open(('Root/Level1/' + channel + '.root'), 'RECREATE')
    Muons_F = TTree('Muons', 'Muons passing the IsoMu20_eta2p1 trigger')
    Pions_F = TTree('Pions', 'Pions associated with muons passing the IsoMu20_eta2p1 trigger')
    
    Event = array('i', [0])
    Muons_F.Branch('Event', Event, 'Event/I')
    Pions_F.Branch('Event', Event, 'Event/I')

    mu_pT, pi_pT = array('f', [0]), array('f', [0])
    Muons_F.Branch('pT', mu_pT, 'pT/F')
    Pions_F.Branch('pT', pi_pT, 'pT/F')

    mu_eta, pi_eta = array('f', [0]), array('f', [0])
    Muons_F.Branch('eta', mu_eta, 'eta/F')
    Pions_F.Branch('eta', pi_eta, 'eta/F')

    mu_charge = array('f', [0])
    Muons_F.Branch('charge', mu_charge, 'charge/F')

    mu_phi, pi_phi = array('f', [0]), array('f', [0])
    Muons_F.Branch('phi', mu_phi, 'phi/F')
    Pions_F.Branch('phi', pi_phi, 'phi/F')

    mu_mass = array('f', [0])
    Muons_F.Branch('mass', mu_mass, 'mass/F')

    # This is just for helping to visualize stuff by printing arrays, will be removed later.
    ar = np.zeros([Muons.GetEntries(), 7]) # Could be also [, 6] if we throw out trigger flag
    
    trigger = [0] * 1000

    for muon in Muons:
        if muon.IsoMu20_eta2p1:
            trigger[muon.Event] += 1

    for i, muon in enumerate(Muons):

        if trigger[muon.Event] > 1:

            Event[0] = muon.Event
            mu_pT[0] = muon.pT
            mu_eta[0] = muon.eta
            mu_charge[0] = muon.charge
            mu_phi[0] = muon.phi
            mu_mass[0] = muon.mass
            Muons_F.Fill()

            ar[i] = [muon.Event, True, muon.pT, muon.eta, muon.charge, muon.phi, muon.mass]

    for pion in Pions:

        if trigger[pion.Event] > 1:

            Event[0] = pion.Event
            pi_pT[0] = pion.pT
            pi_eta[0] = pion.eta
            pi_phi[0] = pion.phi
            Pions_F.Fill()

    Muons_F.Write()
    Pions_F.Write()
    FILE_F.Close()

    print 'Completed level 1 filtering of ' + channel

def filter1(channel):
    print
    print 'This function will perform the following operations on ' + channel + ':'
    print 'Apply Gaussian blur: smear()'
    print 'Select muons with pT > 30'
    print 'Select muons with good isolation'

def main():
        
    filter0('signal')
    filter0('drellyan')
    filter0('ttbar')

    filter1('signal')

if __name__ == '__main__': main()