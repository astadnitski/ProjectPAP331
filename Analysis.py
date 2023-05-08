#!/usr/bin/env python

from array import array
from ROOT import *
import numpy as np

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

    mu_theta = array('f', [0])
    Muons_F.Branch('theta', mu_theta, 'theta/F')

    mu_m, pi_m = array('f', [0]), array('f', [0])
    Muons_F.Branch('m', mu_m, 'm/F')
    Pions_F.Branch('m', pi_m, 'm/F')

    # This is just for helping to visualize stuff by printing arrays, will be removed later.
    #ar = np.zeros([Muons.GetEntries(), 8]) # Could be also [, 7] if we throw out trigger flag
    
    trigger = [0] * 1000

    for muon in Muons:
        if muon.IsoMu20_eta2p1:
            trigger[muon.Event] += 1

    for muon in Muons:
        if trigger[muon.Event] > 1:
            Event[0] = muon.Event
            mu_pT[0] = muon.pT
            mu_eta[0] = muon.eta
            mu_charge[0] = muon.charge
            mu_phi[0] = muon.phi
            mu_theta[0] = muon.theta
            mu_m[0] = muon.m
            Muons_F.Fill()
            #ar[i] = [muon.Event, True, muon.pT, muon.eta, muon.charge, muon.phi, muon.theta, muon.m]

    for pion in Pions:
        if trigger[pion.Event] > 1:
            Event[0] = pion.Event
            pi_pT[0] = pion.pT
            pi_eta[0] = pion.eta
            pi_phi[0] = pion.phi
            pi_m[0] = pion.m
            Pions_F.Fill()

    FILE.Close()
    Muons_F.Write()
    Pions_F.Write()
    FILE_F.Close()

    print('Completed level 1 filtering of ' + channel)

def smear(channel):

    FILE = TFile.Open(('Root/Level1/' + channel + '.root'), 'READ')
    Muons = FILE.Get('Muons')
    
    FILE_F = TFile.Open(('Root/Level2/' + channel + '.root'), 'RECREATE')
    Muons_F = TTree('Muons', 'Muons passing the second set of triggers')

    Event = array('i', [0])
    Muons_F.Branch('Event', Event, 'Event/I')

    mu_pT = array('f', [0])
    Muons_F.Branch('pT', mu_pT, 'pT/F')

    mu_eta = array('f', [0])
    Muons_F.Branch('eta', mu_eta, 'eta/F')

    mu_charge = array('f', [0])
    Muons_F.Branch('charge', mu_charge, 'charge/F')

    mu_phi = array('f', [0])
    Muons_F.Branch('phi', mu_phi, 'phi/F')

    mu_theta = array('f', [0])
    Muons_F.Branch('theta', mu_theta, 'theta/F')

    mu_m = array('f', [0])
    Muons_F.Branch('m', mu_m, 'm/F')

    np.random.seed(3)
    for i, muon in enumerate(Muons):
        
        # https://www.desmos.com/calculator/oj6mh6anxe
        rng = np.random.normal(0, 0.2, 3)

        Event[0] = muon.Event
        mu_pT[0] = muon.pT + 0.01 * rng[0]
        mu_phi[0] = muon.phi + 0.002 * rng[1]
        mu_theta[0] = muon.theta + 0.002 * rng[2]
        mu_eta[0] = -1 * np.log(np.tan((mu_theta[0] / 2)))          ### CHECK THAT THIS IS CORRECT
        mu_charge[0] = muon.charge
        mu_m[0] = muon.m
        Muons_F.Fill()

        #print
        #print(str(muon.Event) + ' | ' + str(muon.pT) + ' | ' + str(dpT))
        #print(str(muon.Event) + ' | ' + str(muon.phi) + ' | ' + str(dphi))
        #print(str(muon.Event) + ' | ' + str(muon.theta) + ' | ' + str(dtheta))         

    FILE.Close()
    Muons_F.Write()
    FILE_F.Close()

def trigger30(channel):

    FILE = TFile.Open(('Root/Level2/' + channel + '.root'), 'READ')
    Muons = FILE.Get('Muons')

    FILE.Close() 
    print('Function not implemented yet: trigger30')

def isolate(channel):

    FILE = TFile.Open(('Root/Level2/' + channel + '.root'), 'READ')
    Muons = FILE.Get('Muons')
    Pions = TFile.Open(('Root/Level1/' + channel + '.root'), 'READ').Get('Pions')
    
    FILE.Close()
    print('Function not implemented yet: isolate')

#def filter1(channel):

    #print('Level 2 filtering of ' + channel + ': applied smear. Still need to select by momentum and isolation')

    #smear(channel)
    #trigger30(channel)
    #isolate(channel)

def main():
        
    filter0('signal')
    filter0('drellyan')
    filter0('ttbar')

    #filter1('signal')
    #filter1('drellyan')
    #filter1('ttbar') 

if __name__ == '__main__': main()
