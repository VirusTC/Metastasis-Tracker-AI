📐 Pycnogonid Simulation Subsystem: Mathematical Models & Equations

This document details the analytical frameworks, fluid dynamics corrections, and population matrices used to resolve agent locomotion, extraintestinal digestion, and lifecycle scaling.

* * * * *

🌊 1. Hydrodynamics & Fluid Locomotion

Pycnogonids operate across low-to-intermediate Reynolds number regimes (\(Re\)). The software dynamically handles the transition between open water and dense substrates via a scale-dependent viscosity corrector.

Open-Water Swimming (Modified Stokes' Drag)

When moving through water, the agent's baseline velocity (\(v_{\text{water}}\)) balances thrust forces (\(F_{\text{thrust}}\)) directly against viscous drag, simplifying the organism to a geometric sphere with an effective hydrodynamic radius (\(R_{\text{eff}}\)):

\(v_{\text{water}}=\frac{F_{\text{thrust}}}{6\pi \mu R_{\text{eff}}}\)

Where:

-   \(\mu \) = Dynamic viscosity of the fluid medium (\(\text{Pa}\cdot\text{s}\)).
-   \(R_{\text{eff}}\) = Hydrodynamic radius derived from total body/appendage surface area (\(A\)):\
    \(R_{\text{eff}}=\sqrt{\frac{A}{4\pi }}\)

Low-Reynolds Creeping/Intrabody Flow (Resistive Force Theory)

When navigating highly viscous environments (where flow regime exponent \(n = 1.0\)), inertial forces collapse. Locomotion scales inversely and linearly with the host tissue's dynamic viscosity (\(\mu _{\text{host}}\)):

\(v_{\text{host}}=\frac{P_{\text{propulsive}}\cdot A_{\text{contact}}}{b\cdot \mu _{\text{host}}}\)

Where:

-   \(P_{\text{propulsive}}\) = Constant muscular force per unit area.
-   \(b\) = Mechanical damping factor governed by the leg section size ratio (\(R_{\text{leg}}\)):\
    \(b=\alpha \cdot R_{\text{leg}}\)

* * * * *

🧪 2. Multi-Substrate Extraintestinal Digestion

The agent utilizes pre-oral digestion by secreting salivary enzymes onto targeted invertebrate tissues. The structural liquefaction rate (\(R_{\text{liq}}\)) relies on an integrated, multi-substrate Michaelis-Menten kinetic model.

Liquefaction Kinetic Equation

\(R_{\text{liq}}=\sum _{e=1}^{E}\left(\frac{V_{\max ,e}\cdot [S]}{K_{m,e}\cdot (1+\rho _{\text{tissue}})+[S]}\right)\cdot \alpha _{e,S}\)

Where:

-   \([S]\) = Available concentration or structural density of the specific target protein (\(\text{mg}/\text{mm}^3\)).
-   \(V_{\max ,e}\) = Maximum substrate conversion velocity of enzyme \(e\) (\(\text{moles}/\text{sec}\cdot\text{mg}\)).
-   \(K_{m,e}\) = Michaelis constant representing substrate binding affinity.
-   \(\rho _{\text{tissue}}\) = Mechanical density modifier of the tissue layer acting as an enzymatic diffusion barrier.
-   \(\alpha _{e,S}\) = Binding affinity coefficient cross-referencing enzyme \(e\) with protein target \(S\).

* * * * *

📈 3. Bioenergetic Growth Model

The absolute physical growth of individual larval and juvenile stages follows a modified Von Bertalanffy growth function, which accounts for parasitic extraction costs and environmental habitat fitness.

Growth Scaling Equation

\(L(t)=L_{\infty }\cdot \left(1-e^{-k_{\text{current}}\cdot (t-t_{0})}\right)-\epsilon \)

Where:

-   \(L_{\infty }\) = Theoretical asymptotic maximum length of the species segment.
-   \(t_{0}\) = Theoretical age at zero length.
-   \(\epsilon \) = Parasitic resource allocation penalty, bounded by available nutritional transfer.
-   \(k_{\text{current}}\) = Globally adjusted growth coefficient tied directly to raw nutrient ingestion volume (\(V_{\text{chyme}}\)) and local environmental comfort:

\(k_{\text{current}}=k_{\text{baseline}}\cdot \left(\frac{dV_{\text{chyme}}}{dt}\right)\cdot HSI\)

* * * * *

🧫 4. Stage-Structured Demographic Projections

Long-term population tensors are calculated at every generational tick using a 4x4 Lefkovitch stage-structured matrix (\(\mathbf{L}\)) multiplied against the population vector (\(\mathbf{n}_{t}\)).

Matrix Matrix Projection Architecture

\(\mathbf{n}_{t+1}=\mathbf{L}\times \mathbf{n}_{t}\)

\(\left[\begin{matrix}n_{\text{larva}}\\ n_{\text{juvenile}}\\ n_{\text{adult}}\\ n_{\text{brooding}}\end{matrix}\right]_{t+1}=\left[\begin{matrix}0&0&F_{\text{adult}}&F_{\text{brooding}}\\ P_{\text{larva}\rightarrow \text{juv}}&0&0&0\\ 0&P_{\text{juv}\rightarrow \text{adult}}&P_{\text{adult}\rightarrow \text{adult}}&0\\ 0&0&0.15&0\end{matrix}\right]\times \left[\begin{matrix}n_{\text{larva}}\\ n_{\text{juvenile}}\\ n_{\text{adult}}\\ n_{\text{brooding}}\end{matrix}\right]_{t}\)

Environmental Scaling Functions

The parameters \(F\) (Fecundity) and \(P_{\text{larva}\rightarrow \text{juv}}\) (Larval Transition Probability) update dynamically during simulation loops using three non-linear environmental constraints:

1.  **Thermal Multiplier (Arrhenius \(Q_{10}\))**:\
    \(f(T)=Q_{10}^{\frac{T-T_{\text{optimal}}}{10}}\)
2.  **Turbulence Mating Penalty**:\
    \(f(\text{Turb})=1.0-\text{Turbulence}^{\lambda }\)
3.  **pH Environmental Stress Curve**:\
    \(f(\text{pH})=\exp \left(-\frac{(\text{pH}-\text{pH}_{\text{optimal}})^{2}}{2\sigma _{\text{pH}}^{2}}\right)\)

Combined, these yield the dynamic entries used to calculate the population tensor step:\
\(F_{\text{actual}}=F_{\text{baseline}}\cdot f(T)\cdot f(\text{Turb})\cdot f(\text{pH})\)\
\(P_{\text{larva}\rightarrow \text{juv\ (actual)}}=P_{\text{larva}\rightarrow \text{juv\ (baseline)}}\cdot f(\text{pH})\)

* * * * *
