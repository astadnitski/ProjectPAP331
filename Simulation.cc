#include <string.h>
#include "Pythia8/Pythia.h"
#include "TFile.h"
#include "TTree.h"

using namespace Pythia8;
using namespace std;

float HLT_DoubleIsoMu20_eta2p1(float pT, float eta) { return pT >= 20 && eta >= -2.1 && eta <= 2.1; }

void simulate(string channel, int N) {

    TFile* file = TFile::Open(("Root/Level0/" + channel + ".root").c_str(), "RECREATE");
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
        //pythia.readString("PhaseSpace:mHatMin = 80.");
        pythia.readString("PhaseSpace:mHatMin = 120.");
        pythia.readString("PhaseSpace:mHatMax = 130.");
    }

    else if (!(strcmp(channel.c_str(), "ttbar"))) {
        cout << "TTBAR SIMULATION" << endl;
        pythia.readString("Top:gg2ttbar = on");
        pythia.readString("Top:qqbar2ttbar = on");
    }

    else { return; }    

    pythia.readString("Beams:eCM = 13600.");
    pythia.readString("Next:numberShowEvent = 0");
    pythia.init();

    TTree* muons = new TTree("Muons", "Analysis of Higgs decay to muons");
    TTree* pions = new TTree("Pions", "Tracking pions to calculate isolation");
    
    int eventID, trigger;
    muons -> Branch("Event", &eventID, "Event/I");
    muons -> Branch("IsoMu20_eta2p1", &trigger, "IsoMu20_eta2p1/I");

    float mu_pT, mu_eta, mu_q, mu_phi, mu_theta, mu_m;
    muons -> Branch("pT", &mu_pT, "pT/F");
    muons -> Branch("eta", &mu_eta, "eta/F");
    muons -> Branch("charge", &mu_q, "charge/F");
    muons -> Branch("phi", &mu_phi, "phi/F");
    muons -> Branch("theta", &mu_theta, "theta/F");
    muons -> Branch("m", &mu_m, "m/F");

    float pi_pT, pi_eta, pi_phi, pi_m;
    pions -> Branch("Event", &eventID, "Event/I");
    pions -> Branch("pT", &pi_pT, "pT/F");
    pions -> Branch("eta", &pi_eta, "eta/F");
    pions -> Branch("phi", &pi_phi, "phi/F");
    pions -> Branch("m", &pi_m, "m/F");

    float accepted = 0.;

    for (int i = 0; i < N; i++) {

        if (!pythia.next()) continue;
        
        int check = 0;

        for (int j = 0; j < pythia.event.size(); j++) {

            if (pythia.event[j].id() == 13 || pythia.event[j].id() == -13) {
                eventID = i;
                mu_pT = pythia.event[j].pT();
                mu_eta = pythia.event[j].eta();
                mu_q = pythia.event[j].charge();
                mu_phi = pythia.event[j].phi();
                mu_theta = pythia.event[j].theta();
                mu_m = pythia.event[j].m();
                muons -> Fill();
                trigger = HLT_DoubleIsoMu20_eta2p1(mu_pT, mu_eta);
                check += trigger;
            }

            else if (pythia.event[j].id() == 211 || pythia.event[j].id() == -211) {
                eventID = i;
                pi_pT = pythia.event[j].pT();
                pi_eta = pythia.event[j].eta();
                pi_phi = pythia.event[j].phi();
                pi_m = pythia.event[j].m();
                pions -> Fill();
            }
            
        }

        if (check > 1) { accepted++; }
        
    }

    string xsec = to_string(1e12 * pythia.info.sigmaGen()); // [fb]
    string eff = to_string(accepted / N);

    TNamed* efficiency = new TNamed("Efficiency", eff);
    TNamed* xsection = new TNamed("Cross section", xsec);
    TNamed* events = new TNamed("Total events", to_string(N));

    efficiency -> Write();
    xsection -> Write();
    events -> Write();

    muons -> Write();
    pions -> Write();
    file -> Close();

}

int main() {
    simulate("signal", 10000);
    simulate("drellyan", 1000000);
    simulate("ttbar", 1000000);
    return 0;
}