That sounds like an exciting contest! Transfer learning in reinforcement learning (RL) is a rapidly growing area with many impactful applications. To help you further, here are some suggestions and considerations for organizing your transfer learning RL contest:

### 1. Define the Contest Goals Clearly
- **Generalization:** Emphasize that the goal is for algorithms to leverage knowledge from source tasks to perform well on related but different target tasks.
- **Sample Efficiency:** Potentially measure how quickly methods adapt (e.g., few-shot adaptation).
- **Robustness:** Assess performance across a variety of environments or perturbations.

### 2. Dataset / Environment Suite
- Prepare a diverse set of source and target environments.
- Consider popular RL benchmarks that support transfer:
  - **Procgen Benchmark:** Procedurally generated environments designed for generalization.
  - **Meta-World:** Suite of robotic manipulation tasks.
  - **Atari with modified parameters:** E.g., change colors, dynamics.
  - **Custom environments:** Ensure tasks have varying degrees of domain shift.
- Provide clear splits: which environments/tasks are for pretraining, which for evaluation.

### 3. Evaluation Metrics
- **Transfer Efficiency:** Improvement on target tasks relative to learning from scratch.
- **Final Performance:** Absolute performance on target tasks after transfer.
- **Adaptation Speed:** Number of interactions required to achieve a threshold performance.
- **Generalization Gap:** Drop between performance on source vs. target.

### 4. Rules and Constraints
- Define what constitutes “previous experience” — pretraining data, offline datasets, etc.
- Limit total environment interactions if sample efficiency is important.
- Restrict architecture/compute, if you want a level playing field.

### 5. Baselines
- Provide baseline implementations for:
  - Training from scratch on targets.
  - Common transfer RL algorithms (e.g., fine-tuning, policy distillation, multi-task RL).
- This helps participants to benchmark their methods.

### 6. Submission Format and Infrastructure
- Specify if participants submit code, trained models, or just results.
- Consider building a leaderboard with automatic evaluation.
- Use cloud environments or sandboxed containers to run participant submissions.

### 7. Additional Considerations
- Encourage participants to submit writeups explaining their approach.
- Consider including a few “surprise” target tasks revealed only at evaluation time.
- Provide clear documentation on how to run and evaluate algorithms.

---

If you'd like, I can help you draft example rules, propose evaluation pipelines, or define specific environments and baselines. Let me know how you'd like to proceed!