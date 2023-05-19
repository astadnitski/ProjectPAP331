# PAP331 Project Work

## Structure of the project

The project has three main components: a simulation script (C++), which generates events using Pythia, an analysis script (Python), which selects events based on the given criteria, and an invariant mass script (Python), which evaluates invariant masses and produces the plots. The project can be run as a whole with the `make` command, or step by step:

- `make simulate`

- `make analyze`

- `make invmass`

This repository includes only generated data after the selections applied in part 2, due to the large file sizes of the unfiltered data. The complete data is saved in [this Google Drive folder](https://drive.google.com/drive/folders/17lVvOqkQQaxy5lSAAQ9y6Djubq0PacGZ?usp=sharing).

## Part 1: Event generation

Events generated using Pythia in `Simulation.cc` and saved to ROOT files in `/Root/Level0/`.

The trigger efficiencies are calculated to be

- Signal: 74.37%

- Drell-Yan: 2.38%

- TTbar: 7.97%

Due to the low efficiencies of the backgrounds, we have generated 10000 signal events and 1000000 of both Drell-Yan and TTbar events. To optimize results, the Drell-Yan events generated were limited to masses between 120 and 130 GeV.

## Part 2: Event analysis

### Additional criteria

Events analyzed with multiple functions in `Analysis.py` and saved to into subdirectories:

- `/Root/Level1/` contains only events that pass the HLT_DoubleIsoMu20_eta2p1 trigger

- `/Root/Level2/` contains only events that pass the criteria given in 2A

- `/Root/InvariantMass/` contains remaining events that can be used to calculate invariant mass (at least one muon and one antimuon)

The number of events passing the selection as a percentage of the original amounts are

- Signal: 48.63%

- Drell-Yan: 1.18%

- TTbar: 3.61 %

### Reconstructing the invariant mass

Plots are saved to the `/Plots/` subdirectory.

- `Channels.png` shows each of the channels individually with the normalization factor indicated

![Channels](https://github.com/astadnitski/ProjectPAP331/blob/main/Plots/Channels.png?raw=true)

- `SignalComparison.png` shows a comparison of the background and total (signal + background) data

![Signal comparison](https://github.com/astadnitski/ProjectPAP331/blob/main/Plots/SignalComparison.png?raw=true)

In the above histograms, a small difference can be seen, as the peak at 125 GeV is slightly taller in the combined signal-and-background plot.

Due to the limited phase space, the Landau fit is suitable for our needs. However, real data exhibits a more complex nature, necessitating the use of multiple background and signal fitting functions.

## Part 3: Project assessment

These results are not perfect. Because Pythia is a generator-level simulation program, and we have not used a detector-level simulator such as GEANT4, the results of this project cannot be compared to actual data from real detectors. Another reason is that the program only includes some of the backgrounds, and not all that would happen in a real experiment. In this program, only Drell-Yan and TTbar (gg2ttbar and qqbar2ttbar) backgrounds are taken into the account. There are also multiple other backgrounds that would have to be analyzed (e.g. W-boson and jets). By including the other backgrounds (e.g. by first allowing all TTbar processes), the results would become more realistic.

We have also limited the masses of the Drell-Yan background to between 120 and 130 GeV to optimize our results, which cannot be done in a real experiment, which would also require a more advanced method of fitting the data.

Another reason for unreliable results is caused by Gaussian smearing. A very small amount of muon θ-angles were so close to zero that, after Gaussian smearing, they became negative, which is outside of the allowed domain. This was avoided by not applying smearing in such cases. In a real experiment, the error would be a natural consequence and not need to be randomly added, so this pitfall would be avoided.

Another cause of error is doing the reconstruction by leading order of transverse momenta. Some of the events had produced more than two muons and antimuons (three or more). The program only reads the leading order values of transverse momenta for muon and antimuon, and reconstructs the invariant mass using only these two. This could also be done by using different permutations of the muon and antimuon pairs to get more accurate data and results.

A major source of error is in the normalization of the data sets, needed in order to add and compare histograms in the second part. For the backgrounds, we used the cross sections for 13 TeV centre-of-mass energy, although the rest of the project was conducted with 13.6 TeV as the energy parameter, leading to additional uncertainty in the result.

The statistical significance of the simulation was calculated to be 1.8σ, which is well below the 5σ threshold for discovery. Given more time and more computational power, we would be able to simulate even more data, producing a more statistically significant result. However, all of the above-listed shortcomings would need to be addressed before any discoveries could be discussed with the scientific community.