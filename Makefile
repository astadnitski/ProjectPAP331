PYTHIA8_URL = https://pythia.org/download/pythia83/pythia8307.tgz
PYTHIA8_TGZ = $(notdir $(PYTHIA8_URL))
PYTHIA8_DIR = $(basename $(PYTHIA8_TGZ))

INC = -I$(PYTHIA8_DIR)/include -Iinterface -I$(ROOTSYS)/include
LIB = -L$(PYTHIA8_DIR)/lib -lpythia8 -ldl
OPT = -g -Wall
ROOTLIBS = -L$(ROOTSYS)/lib -lCore -lTree -lMathCore -lRIO -lHist -lGpad

all: 
	$(MAKE) makePythia
	$(MAKE) compile
	$(MAKE) clean

getPythia:
	@if [ -d "./pythia8307" ]; then echo "Pythia already installed"; else $(MAKE) getPythia0; fi

getPythia0:
	wget $(PYTHIA8_URL)
	tar xfvz $(PYTHIA8_TGZ)
	cd $(PYTHIA8_DIR) && ./configure && make
	@echo Installed Pythia

compile:
	@$(CXX) $(OPT) $(INC) ProjectMain.cc $(LIB) $(ROOTLIBS) -o simulate.exe
	@echo Compiled, running job script	
	@./simulate.job

clean:
	rm -rf $(wildcard *~ *.tgz *.txt *.exe)
	@echo State reset