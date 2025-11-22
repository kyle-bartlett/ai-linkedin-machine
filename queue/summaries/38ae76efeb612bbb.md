Thank you for the clear and concise summary! This paper indeed presents an interesting direction to improve structured pruning by leveraging symmetry and invariant properties in network activations. Here's a bit more elaboration and some context to deepen the understanding:

---

### More Detailed Explanation

1. **Why structured pruning matters?**  
   Structured pruning impacts entire neurons, channels, or convolutional filters, which leads to smaller, faster models that are easier to deploy on hardware (compared to unstructured pruning, which often leads to sparse but irregular parameter layouts). However, structured pruning's effectiveness highly depends on identifying which units are “important” — a nontrivial problem because importance can be entangled or distributed unevenly across the representation.

2. **Role of Change-of-Basis (CoB) in pruning**  
   By applying an orthogonal transformation (essentially a rotation) on the activation space, the hope is to **concentrate the important information into fewer dimensions**. Then pruning out less important dimensions is more effective since dimensions are better aligned with “importance axes”. This theoretically allows pruning more aggressively without hurting performance.

3. **The invariance challenge**  
   Standard architectures with usual nonlinearities like ReLU are **not invariant** to orthogonal transforms. For example, a ReLU applied elementwise on an activation vector behaves differently when the vector is rotated. Because of this, the CoB transformation cannot be absorbed simply into preceding or following weight layers without changing the network’s function — which means the CoB layer adds complexity or breaks the model.

4. **Two-Subspace Radial Activations (TSRAs)**  
   To address this, TSRAs partition the activation vector into two subspaces and apply a **radial function in each subspace** that is **invariant to orthogonal rotations within the subspace**. In other words, the activation depends only on the norm (radius) of each sub-vector, not on the direction, ensuring invariance.

   This design allows CoB transformations to be **absorbed or “folded” into linear layers** without changing the network behavior, enabling the CoB pruning strategy to function seamlessly within standard training/inference pipelines.

5. **Empirical results**  
   Applied to VGG-16 on CIFAR-10, CoB pruning + TSRA enables significantly heavier pruning (up to 70% without fine-tuning and ~90-96% with fine-tuning) than baseline ReLU networks, implying that the model focuses on meaningful directions better.

---

### Implications and Future Directions

- **Bringing symmetry/invariance principles to network design:**  
  The use of rotational invariance here mirrors a broader trend of injecting geometric or algebraic symmetries in neural nets (e.g., group equivariant CNNs). This work shows such invariances can also be exploited for **model compression and pruning**, not just robustness or generalization.

- **Potential for other activation designs:**  
  The paper explores only one form of TSRA; exploring other forms of nonlinearities invariant under different groups or subspace divisions could lead to better tradeoffs between accuracy and pruning capacity.

- **Limits due to accuracy drop:**  
  The ~4.5% accuracy drop without fine-tuning suggests some expressivity may be lost by forcing rotational invariance. Future research can explore smarter initialization, more flexible activations, or hybrid approaches.

- **Broader pruning frameworks:**  
  Integrating CoB pruning with complementary techniques like knowledge distillation, quantization, or structured sparsity regularizers could yield even more efficient compressed models.

---

If you want, I can also help with:  
- A step-by-step explanation of how TSRAs are mathematically defined and implemented  
- Connections to related works on invariant/equivariant networks and pruning methods  
- Ideas on practical considerations for implementing CoB pruning and TSRAs in your codebase  

Just let me know!