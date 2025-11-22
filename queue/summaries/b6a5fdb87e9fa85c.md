That's a very interesting approach! By using process supervision—rewarding each correct step of reasoning rather than only the final answer—you are effectively encouraging the model to develop a more transparent and interpretable chain-of-thought. This can lead to several key advantages:

1. **Improved Performance:**  
   Encouraging correctness step-by-step helps the model maintain consistency in reasoning, reducing errors that might occur when only focusing on the final outcome. It can better handle complex multi-step problems where intermediate reasoning is crucial.

2. **Better Interpretability:**  
   Since the model produces chains of reasoning that are human-endorsed, it's easier for users and developers to understand how the model arrived at a particular answer. This transparency can aid debugging and trust.

3. **Alignment and Safety:**  
   Training the model to produce reasoning steps that humans approve means it is less likely to generate misleading, unfounded, or unsafe outputs. The alignment benefit comes from directly shaping the model’s internal reasoning process to match human standards and expectations.

4. **Generalization and Transfer:**  
   By focusing on process rather than just outcome, the model might generalize better across different types of problems, since it learns a more structured approach to reasoning.

Have you observed significant improvements in specific benchmarks or problem categories? Also, how do you collect human endorsements for each reasoning step at scale?