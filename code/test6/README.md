# test6

adding configence interval from test5 code.
(last part of the tutorial from 
https://machinelearningmastery.com/machine-learning-in-python-step-by-step/)

model evaluation: (evaluate.py)
use test5 code to test multiple models and evaluate them.  
From results and box and whiskers plot: LDA and CART seems to be the best models 
for the problem. (test.png)  

Evaluate predictions of lda and cart algorithm: (lda_eval.py / cart_eval.py)  
create a confusion matrix:  
```
  			event			no-event
event		true positive		false positive
no-event	false negative		true negative
```

