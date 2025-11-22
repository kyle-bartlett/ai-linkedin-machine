The paper (arXiv:2511.16476v1) investigates the limitations of scalarisation functions commonly used in Multi-Objective Reinforcement Learning (MORL) for decision-making. Here is a concise summary of the key points:

- **Context:** Scalarisation functions (like linear and Chebyshev scalarisation) are popular in MORL to reduce multiple objectives into a single scalar value, making the learning process more straightforward.
- **Problem:** These scalarisation functions often struggle to approximate the Pareto front (set of optimal trade-offs between objectives) accurately, especially in complex environments with discrete action and observation spaces.
- **Methodology:**  
  - The study uses an outer-loop multi-policy approach to evaluate MO Q-Learning (a classic single-policy MORL method) with scalarisation functions.  
  - It also evaluates Pareto Q-Learning, an inner-loop multi-policy algorithm that explicitly aims to approximate the Pareto front.
- **Findings:**  
  - Scalarisation functions are sensitive to the environment and the shape of the Pareto front.  
  - They tend to miss parts of the Pareto front and favor solutions in particular regions, leading to incomplete approximations.  
  - Finding appropriate weights to cover the entire Pareto front is challenging, limiting their effectiveness in uncertain or dynamic environments.  
  - Pareto Q-Learning, which maintains multiple policies to better approximate the full Pareto front, is a more robust and generalizable approach, better suited for uncertain and dynamic settings.
  
**Implications:**  
The study suggests that inner-loop multi-policy algorithms like Pareto Q-Learning may offer improved decision-making capabilities in MORL, especially when the environment is complex and uncertain, potentially advancing intelligent agents capable of handling multiple competing objectives more effectively.

If you want, I can help you with more details on the concepts, methodology, or implications!