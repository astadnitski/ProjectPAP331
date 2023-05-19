from ROOT import *
from array import array
import numpy as np

def filter0(channel):

    FILE = TFile.Open(('Root/Level0/' + channel + '.root'), 'READ')
    Muons, Pions = FILE.Get('Muons'), FILE.Get('Pions')
    efficiency, xsection, events = FILE.Get('Efficiency'), FILE.Get('Cross section'), FILE.Get('Total events')
    
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
    
    trigger = [0] * int(Pions.GetMaximum('Event') + 1)
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

    for pion in Pions:
        if trigger[pion.Event] > 1:
                Event[0] = pion.Event
                pi_pT[0] = pion.pT
                pi_eta[0] = pion.eta
                pi_phi[0] = pion.phi
                pi_m[0] = pion.m
                Pions_F.Fill()

    FILE.Close()

    efficiency.Write()
    xsection.Write()
    events.Write()

    Muons_F.Write()
    Pions_F.Write()
    FILE_F.Close()

    print('Completed level 1 filtering of ' + channel)

def filter1(channel):

    AllEvents = 0
    FILE0 = TFile.Open(('Root/Level0/' + channel + '.root'), 'READ')
    AllMuons = FILE0.Get('Muons')
    for i, muon in enumerate(AllMuons):
        if muon.Event+1 > AllEvents:
            AllEvents = muon.Event+1
    FILE0.Close()

    FILE = TFile.Open(('Root/Level1/' + channel + '.root'), 'READ')
    Muons = FILE.Get('Muons')
    Pions = FILE.Get('Pions')
    efficiency = FILE.Get('Efficiency')
    xsection = FILE.Get('Cross section')
    events = FILE.Get('Total events')
    
    FILE_F = TFile.Open(('Root/Level2/' + channel + '.root'), 'RECREATE')
    Muons_F = TTree('Muons', 'Muons passing the second set of triggers')

    Event_mu = array('i', [0])
    Muons_F.Branch('Event', Event_mu, 'Event/I')

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
    pions, muons = [], []

    for pion in Pions: pions.append([pion.Event, pion.pT, pion.eta, pion.phi, pion.m])
            
    for i, muon in enumerate(Muons):
        
        rng = np.random.normal(0, 1, 3)

        Event_number = muon.Event
        muonpT = muon.pT + 0.01 * rng[0]
        muonphi = muon.phi + 0.002 * rng[1]
        
        if muon.theta + 0.002 * rng[2] > 0: muontheta = muon.theta + 0.002 * rng[2]
        else: muontheta = muon.theta

        muoneta = -1 * np.log(np.tan((muontheta / 2)))
        muoncharge = muon.charge
        muonm = muon.m
        muons.append([Event_number, muonpT, muoneta, muonphi, muonm, muoncharge, muontheta])
    
    temp = []    

    # Filtering and isolating the muons
    for particle in muons:

        pion_pTs = []
        muon_vector = TLorentzVector()
        muon_vector.SetPtEtaPhiM(particle[1], particle[2], particle[3], particle[4])

        for subparticle in pions:

            if subparticle[0] == particle[0]:

                pion_vector = TLorentzVector()
                pion_vector.SetPtEtaPhiM(subparticle[1], subparticle[2], subparticle[3], subparticle[4])

                if muon_vector.DeltaR(pion_vector) < 0.3: pion_pTs.append(subparticle[1])
                    
        if particle[1] > 30.0 and sum(pion_pTs) < 1.5: temp.append(particle)
                
    filtered = []      
    finish = temp[-1][0] + 1  
    
    # Filtering all the events that have at least one antimuon and muon
    for i in range(finish):

        temp2 = []
        mutrigger = 0
        antimutrigger = 0

        for particle in temp:

            if particle[0] == i:

                temp2.append(particle)

                if particle[5] == 1.0: mutrigger += 1
                elif particle[5] == -1.0: antimutrigger += 1

        if mutrigger > 0 and antimutrigger > 0: filtered.append(temp2)
            
    # Filling and writing the Level 2 ROOT file with the filtered muons
    for element in filtered:
        for particle in element:
            Event_mu[0] = particle[0]
            mu_pT[0] = particle[1]
            mu_phi[0] = particle[3]
            mu_theta[0] = particle[6]
            mu_eta[0] = particle[2]
            mu_charge[0] = particle[5]
            mu_m[0] = particle[4]
            Muons_F.Fill()               

    FILE.Close()
    Muons_F.Write()
    efficiency.SetTitle(str(len(filtered) / float(AllEvents)))
    efficiency.Write()
    xsection.Write()
    events.Write()
    FILE_F.Close()
    
    print('Completed level 2 filtering of ' + channel)
    
def main():

    filter0('signal')
    filter0('drellyan')
    filter0('ttbar') 

    filter1('signal')
    filter1('drellyan')
    filter1('ttbar') 

if __name__ == '__main__': main() 