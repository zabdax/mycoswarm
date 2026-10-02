## **Main Proposal:** Myco-Swarm: An In-Silico Proof of Concept for Synthetic Symbiosis

**The Premise:** Current bioremediation requires an *ex-situ* bioreactor because bacteria are too small to physically capture scattered microplastics in the environment. We propose a synthetic predator/prey symbiosis: engineered bacteria ("Scouts") bind to microplastics and emit a synthetic pheromone, which triggers an engineered fungal network ("Harvesters") to swarm, physically envelop, and sequester the plastics.

**The Novelty (Preserved):** This is a paradigm shift from single-cell metabolic engineering to **Ecosystem-Level Behavioral Symbiosis**. It solves the impossible physical scale problem of microplastics by turning invisible dust into macroscopic, harvestable mycelial mats.

**Refined Scope & Methodology (Addressing the Feedback):** As the TA noted, physically building and validating a cross-kingdom signaling system in a wet lab is a multi-year Ph.D. project. Therefore, for SIBRP, this project is aggressively narrowed to a **purely computational proof-of-concept**.

1. **Peptide Design (AlphaFold 3):** We will use structural ML (AlphaFold 3 / RFdiffusion) to design the surface-display peptides for the Scout bacteria that specifically bind to PET surfaces.  
2. **Ecological & Spatial Modeling (Agent-Based Simulation):** The core of the SIBRP project will be building a 3D spatial simulation (using NetLogo or a custom PyTorch environment).  
   * We will model the physical diffusion gradient of the theoretical synthetic pheromone emitted by the Scout bacteria across a simulated soil matrix.  
   * We will model the chemotactic branching behavior of a filamentous fungus (e.g., *Trichoderma*) in response to that gradient.

**Success Metric:** The deliverable is the finalized *in-silico* peptide structures and a mathematical simulation proving that a synthetic fungal-bacterial swarm can physically aggregate scattered microplastics 10x-50x faster than passive bacterial diffusion. This simulation serves as the mandatory groundwork required before any future wet-lab team attempts to build the system.

---

**Abstract:**   
	Microplastics pervasively contaminate agricultural soils, acting as vectors for heavy metals and pathogens. Current synthetic bioremediation relies on engineering single bacterial strains for metabolic degradation. The critical engineering gap is the inability of bacteria to physically aggregate scattered microplastics in-situ, forcing reliance on ex-situ bioreactors. We propose Myco-Swarm, an in-silico proof-of-concept for a synthetic bacterial-fungal symbiosis. Our objective is to design a system where engineered bacteria bind to microplastics and emit synthetic pheromones, triggering engineered fungal networks to chemotactically swarm and physically sequester the plastics into macroscopic mats. We will validate this computationally by using AlphaFold 3 to design the plastic-binding peptides and Agent-Based Modeling to simulate the fungal chemotaxis and sequestration rate across a 3D soil matrix. This project provides a foundational theoretical framework for in-situ microplastic extraction, moving synthetic biology beyond single-cell metabolism toward ecosystem-level behavioral symbiosis.  
