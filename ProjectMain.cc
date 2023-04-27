#include "TFile.h"
#include "TTree.h"
#include "Pythia8/Pythia.h"
#include <string.h>

using namespace Pythia8;
using namespace std;

#define Nevents 10000

// Can be simplified: return (condition AND condition AND condition)
bool HLT_DoubleIsoMu20_eta2p1(float pT, float eta) {
    if (pT <= 20) return false;
    if (eta >= 2.1) return false;
    if (eta <= -2.1) return false;
    return true;
}

bool HLT_DoubleIsoMu30(float pT) { return pT >= 30; }

void gen(string channel, TFile *events) {

    // Root initialization

    /// STEP 1: (Pythia) INITIALIZATION ///

    Pythia pythia;
    pythia.readString("Beams:eCM = 13600.");

    pythia.readString(channel + " = on");
    if (!(strcmp(channel.c_str(), "Top:gg2ttbar"))) {
        cout << "Compared, setting Top:qqbar2ttbar = on" << endl;
        pythia.readString("Top:qqbar2ttbar = on");
    }

    pythia.readString("25:onMode = off");
    pythia.readString("25:onIfMatch = -13 13");
    pythia.readString("Next:numberShowEvent = 0");

    pythia.init();

    /// STEP 2: EVENT GENERATION LOOP ///

    Hist transverse("Transverse momentum", 100, 0., 100.);
    Hist pseudo("Pseudorapidity", 100, 0., 100.);

    TTree* muon = new TTree("muon", "muon events generated with Pythia");
    TTree* antimuon = new TTree("antimuon", "antimuon events generated with Pythia");

    int isMuon, isAntimuon;
    float mu_pT, mu_eta, mu_m, mu_charge, mu_phi;
    float antimu_pT, antimu_eta, antimu_m, antimu_charge, antimu_phi;

    muon -> Branch("pT", &mu_pT, "pT/F");
    muon -> Branch("eta", &mu_eta, "eta/F");
    muon -> Branch("m", &mu_m, "m/F");
    muon -> Branch("charge", &mu_charge, "charge/F"); 
    muon -> Branch("phi", &mu_phi, "phi/F");

    antimuon -> Branch("pT", &antimu_pT, "pT/F");
    antimuon -> Branch("eta", &antimu_eta, "eta/F");
    antimuon -> Branch("m", &antimu_m, "m/F");
    antimuon -> Branch("charge", &antimu_charge, "charge/F");
    antimuon -> Branch("phi", &antimu_phi, "phi/F");

    float efficiency;
    int Nmuonpassed = 0, Nantimuonpassed = 0;
    int Nmuontotal = 0, Nantimuontotal = 0;

    for (int i = 0; i < Nevents; i++) {

        if (!pythia.next()) continue;

        isMuon = 0;
        isAntimuon = 0;

        for (int j = 0; j < pythia.event.size(); j++) {

            if (pythia.event[j].id() == -13) {

                isMuon = j;
                Nmuontotal++;

                mu_pT = pythia.event[isMuon].pT();
                mu_eta = pythia.event[isMuon].eta();

                transverse.fill(mu_pT);
                pseudo.fill(mu_eta);

                if (HLT_DoubleIsoMu20_eta2p1(mu_pT, mu_eta)) {

                    //if (HLT_DoubleIsoMu30(mu_pT)) {
                        mu_m = pythia.event[isMuon].m();
                        mu_charge = pythia.event[isMuon].charge();
                        mu_phi = pythia.event[isMuon].phi();
                        Nmuonpassed++;
                        muon -> Fill();
                    //}
                    
                } 

            }

            else if (pythia.event[j].id() == 13) {

                isAntimuon = j;
                Nantimuontotal++;

                antimu_pT = pythia.event[isAntimuon].pT();
                antimu_eta = pythia.event[isAntimuon].eta();

                transverse.fill(antimu_pT);
                pseudo.fill(antimu_eta);
                 
                 if (HLT_DoubleIsoMu20_eta2p1(antimu_pT, antimu_eta)) {
                    
                    // if (HLT_DoubleIsoMu30(antimu_pT)) {
                        antimu_m = pythia.event[isAntimuon].m();
                        antimu_charge = pythia.event[isAntimuon].charge();
                        antimu_phi = pythia.event[isAntimuon].phi();
                        Nantimuonpassed++;
                        antimuon -> Fill();
                    //}

                } 

            }

            else continue;
        }
        
    }

    /// STEP 3: PRINT AND SAVE DATA ///

    pythia.stat();
    cout << transverse;
    cout << pseudo;

    efficiency = 100.0 * (Nmuonpassed + Nantimuonpassed) / (Nmuontotal + Nantimuontotal);
    cout << endl << "Efficiency: " << efficiency << "%" << endl;

    muon -> Write();
    antimuon -> Write();
    events -> Close();

}

int main() {

    TFile* signal = TFile::Open("Root/signal.root", "RECREATE");
    gen("HiggsSM:all", signal); // Signal (Higgs)

    TFile* DrellYan = TFile::Open("Root/drellyan.root", "RECREATE");
    gen("WeakSingleBoson:ffbar2gmZ", DrellYan); // Drell-Yan background

    TFile* ttbar = TFile::Open("Root/ttbar.root", "RECREATE"); 
    gen("Top:gg2ttbar", ttbar); // ttbar background: function checks and turns on other channel

    return 0;

}

/* NOTES
- чому не прац дерева всі
- інвар мас
- селекшн 30
- зробити лаб 11, 12
*/