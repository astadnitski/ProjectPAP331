#include <string.h>
#include "Pythia8/Pythia.h"
#include "TFile.h"
#include "TTree.h"

using namespace Pythia8;
using namespace std;

float HLT_DoubleIsoMu20_eta2p1(float pT, float eta) { return pT >= 20 && eta >= -2.1 && eta <= 2.1; }
float HLT_DoubleIsoMu30(float pT) { return pT >= 30; }

void simulate(string channel, int N) {

    TFile* file = TFile::Open(("Root/" + channel + ".root").c_str(), "RECREATE");
    Pythia pythia;

    if (!(strcmp(channel.c_str(), "signal"))) {
        cout << "SIGNAL SIMULATION" << endl;
        pythia.readString("HiggsSM:all = on");
        pythia.readString("25:onMode = off");
        pythia.readString("25:onIfMatch = -13 13");
    }

    else if (!(strcmp(channel.c_str(), "drellyan"))) {
        cout << "DRELL-YAN SIMULATION" << endl;
        pythia.readString("WeakSingleBoson:ffbar2gmZ = on");
        pythia.readString("PhaseSpace:mHatMin = 80.");
    }

    else if (!(strcmp(channel.c_str(), "ttbar"))) {
        cout << "TTBAR SIMULATION" << endl;
        pythia.readString("Top:gg2ttbar = on");
        pythia.readString("Top:qqbar2ttbar = on");
    } // Can be also Top ttbar all: on (last question: how to improve the analysis)

    else { return; }    

    pythia.readString("Beams:eCM = 13600.");
    pythia.readString("Next:numberShowEvent = 0");
    pythia.init();

    TTree* muons = new TTree("Muons", "Analysis of Higgs decay to muons");
    TTree* pions = new TTree("Pions", "Tracking pions to calculate isolation");
    float eventID, trigger;
    
    muons -> Branch("Event", &eventID, "Event/F");
    muons -> Branch("IsoMu20_eta2p1", &trigger, "IsoMu20_eta2p1/F");

    float mu_pT, mu_eta, mu_q, mu_phi, mu_m;
    muons -> Branch("Muon_pT", &mu_pT, "Muon_pT/F");
    muons -> Branch("Muon_eta", &mu_eta, "Muon_eta/F");
    muons -> Branch("Muon_charge", &mu_q, "Muon_charge/F");
    muons -> Branch("Muon_phi", &mu_phi, "Muon_phi/F");
    muons -> Branch("Muon_mass", &mu_m, "Muon_mass/F");

    float pi_pT, pi_eta, pi_phi;
    pions -> Branch("Pion_pT", &pi_pT, "Pion_pT/F");
    pions -> Branch("Pion_eta", &pi_eta, "Pion_eta/F");
    pions -> Branch("Pion_phi", &pi_phi, "Pion_phi/F");

    float accepted = 0.;

    for (int i = 0; i < N; i++) {

        if (!pythia.next()) continue;

        cout << endl;
        cout << "Loop iteration " << i << endl;
        int check = 0;

        for (int j = 0; j < pythia.event.size(); j++) {

            if (pythia.event[j].id() == 13 || pythia.event[j].id() == -13) {
            
                cout << "Observed muon in event " << i << " with ID " << pythia.event[j].id() << endl;
                
                eventID = i;

                mu_pT = pythia.event[j].pT();
                mu_eta = pythia.event[j].eta();
                mu_q = pythia.event[j].charge();
                mu_phi = pythia.event[j].phi();
                mu_m = pythia.event[j].m();

                trigger = HLT_DoubleIsoMu20_eta2p1(mu_pT, mu_eta);
                if (trigger) { cout << "This particle passed the trigger: " << trigger << endl; }
                check += trigger;

                muons -> Fill();

            }

            else if (pythia.event[j].id() == 211 || pythia.event[j].id() == -211) {

                eventID = i;

                pi_pT = pythia.event[j].pT();
                pi_eta = pythia.event[j].eta();
                pi_phi = pythia.event[j].phi();

                pions -> Fill();

            }
            
        }

        // This stuff with check should be moved to Analysis.cc?
        //cout << "Amount of muons passing the trigger: " << check << endl;
        if (check > 1) { accepted++; }
        
    }

    cout << "Efficiency: " << accepted / N << endl;
    muons -> Write();
    pions -> Write();
    file -> Close();

}

int main() {
    simulate("signal", 1000);
    simulate("drellyan", 1000);
    simulate("ttbar", 1000);
    return 0;
}