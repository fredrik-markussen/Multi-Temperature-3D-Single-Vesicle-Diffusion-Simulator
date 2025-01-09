# Multi-Temperature 3D Diffusion Simulation

**Disclaimer:**  
This code and simulation model, generated using generative LLMs, are provided for educational and experimental purposes only. The model makes simplified assumptions and is flawed. It is not peer-reviewed by topic experts and should not be cited in academic or public communications. Users are free to modify, experiment, and build upon this code as needed.

## Overview

This repository provides a Python script to simulate the Brownian motion of glutamate molecules in a synaptic cleft across three different temperatures: 310 K, 274 K, and 50 K. The simulation models the diffusion process starting from a single point, representing the instantaneous release of a glutamate vesicle at the presynaptic membrane, to a hypothetical binding region on the opposite side of the cleft. The results are visualized using three separate 3D scatter plots—one for each temperature—and a shared 2D concentration graph that overlays the concentration curves, highlighting the temperature-dependent differences in diffusion.

The goal is to explore how temperature affects diffusion speed and to illustrate that, within the physiological range, diffusion is extremely fast relative to synaptic delays. This work draws inspiration from:

- *Nanoscale diffusion in the synaptic cleft and beyond measured with time-resolved fluorescence anisotropy imaging*, which emphasizes the rapidity of nanoscale diffusion.
- *Phasic secretion of acetylcholine at a mammalian neuromuscular junction* by Datyner & Gage, discussing factors influencing synaptic delay beyond diffusion.
- *The effect of temperature on the synaptic delay at the neuromuscular junction* by B. Katz & R. Miledi, highlighting that diffusion is not the rate-limiting step in synaptic transmission.

**Basic Results and Interpretation:**
- At 310 K, diffusion occurs rapidly, filling a theoretical ligand binding region within nanoseconds (<50 ns).
- At 274 K, diffusion is insignificantly slower, filling a theoretical ligand binding region within nanoseconds (<50 ns)
- Lower temperatures (50 K) show slower diffusion. However, even at 50 K, the diffusion process remains faster than typical temperature-dependent synaptic delays observed by pervious studies.
- These findings support literature suggesting that synaptic delay is governed more by processes other than mere molecular diffusion within the synaptic cleft.

## Features

- **Multi-Temperature Simulation:** Visualizes diffusion at 310 K, 274 K, and 50 K side-by-side.
- **3D Scatter Plots:** Three independent 3D plots display spatial distribution of molecules at different temperatures.
- **Concentration Graph:** A shared 2D graph overlays concentration curves for all temperatures, highlighting changes over time above a specified z-threshold.
- **Adjustable Parameters:** Easily modify simulation settings such as number of particles, simulation duration, temperature, etc.
- **Video Output:** Generates an MP4 video (`Multi_Temperature_Diffusion.mp4`) summarizing the multi-panel simulation.

## Dependencies

- Python 3.x
- NumPy
- Matplotlib
- FFmpeg (for video rendering)

## Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/multi-temperature-diffusion.git
   cd multi-temperature-diffusion

   
2. **Install required Python packages:**
```
pip install numpy matplotlib
```

Ensure that FFmpeg is installed on your system and is accessible from the command line, as Matplotlib uses it to render videos.

## Usage

To run the simulation and generate the multi-temperature video:

```bash
python multi_temperature_diffusion.py
```

**The script will:**

 - Perform separate simulations for 310 K, 274 K, and 50 K.
 - Store simulation data for each temperature.
 - Create a multi-panel animation with three 3D scatter plots and one shared concentration graph.
 - Save the final video as Multi_Temperature_Diffusion.mp4.

**Adjusting Parameters**
You can modify parameters at the top of the script to change simulation conditions:

 - num_particles: Number of glutamate molecules.
 - fps, duration: Frame rate and simulation duration.
 - temperatures: List of temperatures to simulate (default [310, 274, 50]).
 - Other parameters like reflective_floor, reflective_roof, and spatial limits can also be adjusted.
 - After modifying parameters, re-run the script to generate updated simulation results and video.

**Simulation Details**
<h2>Verification of Brownian Motion Mathematics</h2>

<p>The mathematics used in the simulation is based on principles of Brownian motion, derived from the Einstein relation and diffusion theory. Below is a step-by-step verification of the calculations for Brownian displacement and diffusion:</p>

<h3>1. Diffusion Constant Calculation</h3>

<p>The diffusion constant D is adjusted for each temperature using the equation:</p>
<pre><code>D = D_base * (T / T_ref)</code></pre>
<p>
- D_base = 0.46 x 10^-9 m²/s (for 310 K).<br>
- T is the simulation temperature (e.g., 310, 274, or 50 K).<br>
- T_ref = 310 K.
</p>
<p>This calculation assumes diffusion scales linearly with temperature, a reasonable approximation for small molecules in a liquid.</p>
<p>The computed diffusion constant is converted to picometers squared per microsecond (pm²/µs) using:</p>
<pre><code>D_pm2_per_us = D_m2_per_s * 1e24 / 1e6</code></pre>
<p>This conversion is consistent, since:</p>
<ul>
  <li>1 m² = 10^24 pm²</li>
  <li>1 s = 10^6 µs</li>
</ul>

<h3>2. Displacement Standard Deviation</h3>

<p>The standard deviation for Brownian displacement is calculated using:</p>
<pre><code>σ = sqrt(2 * D * Δt)</code></pre>
<p>Where:</p>
<ul>
  <li>D is the diffusion constant in pm²/µs.</li>
  <li>Δt = 0.001 µs (1 ns per frame).</li>
</ul>
<p>This formula provides the standard deviation of the random displacement in each spatial dimension, consistent with Brownian motion theory.</p>

<h3>3. Brownian Motion Implementation</h3>

<p>For each frame, random displacements are sampled from a normal distribution:</p>
<pre><code>displacements = np.random.normal(loc=0, scale=sigma, size=(num_particles, 3))
positions += displacements</code></pre>
<p>This uses:</p>
<ul>
  <li>Mean μ = 0 (no net drift).</li>
  <li>Standard deviation σ for each spatial dimension.</li>
</ul>
<p>This approach is consistent with Brownian motion, where displacements in each dimension are independent and normally distributed.</p>

<h3>4. Reflective Boundaries</h3>

<p>The script enforces reflective boundaries on the z-axis:</p>
<pre><code>below_floor = positions[:, 2] &lt; reflective_floor
positions[below_floor, 2] = 2 * reflective_floor - positions[below_floor, 2]

above_roof = positions[:, 2] &gt; reflective_roof
positions[above_roof, 2] = 2 * reflective_roof - positions[above_roof, 2]</code></pre>
<p>This ensures particles remain within the simulation boundaries by reflecting them off the floor and ceiling.</p>

<h3>5. Concentration Calculation</h3>

<p>Concentration above a threshold z is computed as:</p>
<pre><code>particle_counts = np.sum(all_positions[:, :, 2] &gt; threshold_z, axis=1)
concentration = particle_counts / volume</code></pre>
<p>
- Particle counts are obtained by summing particles with z &gt; threshold_z.<br>
- The volume of the region is calculated as Area_xy × Height.<br>
- Concentration C is the number of particles divided by this volume.
</p>

<h3>Key Observations</h3>
<ul>
  <li>The calculations for diffusion, displacement, and boundaries align with Brownian motion theory.</li>
  <li>Unit conversions are correctly handled.</li>
  <li>Reflective boundaries and concentration calculations are logically implemented.</li>
</ul>

<h3>Limitations</h3>
<ul>
  <li><strong>Linear scaling assumption:</strong> The model assumes D ∝ T, which may not hold at extreme temperatures or account for viscosity changes.</li>
  <li><strong>Simplifications:</strong> The simulation omits complex factors like receptor binding, vesicle release dynamics, and detailed synaptic architecture.</li>
  <li><strong>Boundary conditions:</strong> Reflective boundaries are a simplified representation of biological membranes.</li>
</ul>

<p>Overall, the mathematical framework is sound under the given assumptions, making this simulation a useful educational tool despite its simplifications.</p>


## Interpretation and Relevance to Biology

![Simulation Preview](Multi_Temperature_Diffusion.gif)

The simulation provides a visual and quantitative demonstration of how temperature influences the diffusion of neurotransmitters, specifically glutamate, in the synaptic cleft. Diffusion is a fundamental process underlying synaptic transmission, but the rate-limiting steps in synaptic delay is not due to diffusion itself.

**Key Biological Insights:**

- **Rapid Diffusion at Nanoscale:**  
  The simulation underscores findings by Zheng et al. [^3] that diffusion at the nanoscale within the synaptic cleft is extremely fast. Even at extreme and biologically irrelevant temperatures like 50 K, the model predicts that molecules can traverse the synaptic cleft in around 250 nanoseconds, which is orders of magnitude shorter than temperature-dependent synaptic delays observed in biological systems.

- **Temperature Dependence of Synaptic Delay:**  
  Katz and Miledi [^1] demonstrated that synaptic delay at the neuromuscular junction is highly temperature-dependent, but the delay cannot be attributed solely to diffusion because diffusion occurs too rapidly. The simulation aligns with this by showing that even significant changes in temperature primarily affect diffusion speed, while the overall synaptic delay is likely governed by other processes such as vesicle fusion, calcium dynamics, and receptor kinetics.

- **Phasic Secretion Dynamics:**  
  Datyner and Gage [^2] investigated the kinetics of acetylcholine secretion at mammalian neuromuscular junctions, revealing that processes following membrane depolarization (rather than diffusion across the cleft) contribute significantly to synaptic delay. Our simulation reinforces this interpretation by showing that variations in diffusion across a range of temperatures do not account for the millisecond-scale delays observed in synaptic transmission.

**Relevance to Research and Education:**

- The simulation serves as an educational tool to visualize how diffusion behaves under different temperatures, emphasizing that diffusion is not the bottleneck in synaptic signalling.
- It reinforces the concept that synaptic delay is influenced more by complex biochemical and cellular mechanisms than by the mere diffusion of neurotransmitters.
- Researchers can use or adapt this simulation framework to explore other variables affecting synaptic transmission, although they should be cautious due to the model's simplifications and limitations.

## Citations

[^1]: Katz B, Miledi R. The effect of temperature on the synaptic delay at the neuromuscular junction. *J Physiol.* 1965 Dec;181(3):656-70. doi: [10.1113/jphysiol.1965.sp007790](https://doi.org/10.1113/jphysiol.1965.sp007790). PMID: [5880384](https://pubmed.ncbi.nlm.nih.gov/5880384/); PMCID: [PMC1357674](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1357674/).

[^2]: Datyner NB, Gage PW. Phasic secretion of acetylcholine at a mammalian neuromuscular junction. *J Physiol.* 1980 Jun;303:299-314. doi: [10.1113/jphysiol.1980.sp013286](https://doi.org/10.1113/jphysiol.1980.sp013286). PMID: [6253620](https://pubmed.ncbi.nlm.nih.gov/6253620/); PMCID: [PMC1282892](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1282892/).

[^3]: Zheng, K., Jensen, T., Savtchenko, L. et al. Nanoscale diffusion in the synaptic cleft and beyond measured with time-resolved fluorescence anisotropy imaging. *Sci Rep* 7, 42022 (2017). https://doi.org/10.1038/srep42022
