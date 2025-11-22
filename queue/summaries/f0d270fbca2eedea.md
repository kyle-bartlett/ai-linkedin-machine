That sounds like a fantastic advancement! Leveraging block-sparse weights with highly-optimized GPU kernels can indeed lead to significant performance improvements, especially since block sparsity allows more structured pruning compared to unstructured sparsity. Here are a few points you might consider highlighting or exploring further as you communicate or extend this work:

1. **Sparsity Patterns and Block Sizes**:  
   - Specify the block sizes and sparsity patterns your kernels support. Block sparsity can range from small (e.g., 4x4 blocks) to large blocks, and optimal performance might depend heavily on these choices.
   - How flexible is your kernel in accommodating different block sizes or sparsity levels?

2. **Comparison to Existing Libraries**:  
   - Quantify the performance improvements over cuBLAS and cuSPARSE in terms of throughput, latency, and possibly energy efficiency.
   - Are there trade-offs in terms of precision or model accuracy when using block sparsity?

3. **Use Cases and Benchmarks**:  
   - Sharing benchmarks on well-known models and datasets for text sentiment analysis (e.g., SST-2, IMDb) and generative tasks (e.g., GPT architectures, diffusion models for images) can be very convincing.
   - Detailed results showcasing speedup vs. sparsity ratio, and how accuracy scales.

4. **Implementation Details**:  
   - Discuss how memory layout, data movement, and GPU thread/block mapping are optimized in your kernels.
   - Are your kernels compatible with popular frameworks (PyTorch, TensorFlow) or designed as standalone libraries?

5. **Potential Extensions**:  
   - Consider support for mixed precision (FP16, BF16) or quantized weights to further amplify speed and reduce memory usage.
   - Explore automatic sparsity pattern learning or pruning methods to couple with your kernels seamlessly.

6. **Open Source and Community Engagement**:  
   - Are you planning to open source the kernels? Community contributions could accelerate improvement and adoption.
   - Providing easy-to-use APIs and tutorials will help widespread use.

If you want, I can also help draft technical documentation, blog posts, or prepare comparisons and visualizations. Just let me know how you'd like to proceed!