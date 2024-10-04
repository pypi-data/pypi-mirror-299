# PG2S
*A full Python library for the PG2S metric [(paper)](https://arxiv.org/abs/2408.05478).*


## Quickstart
#### Clone & Install
```shell
git clone https://github.com/Lab-RoCoCo-Sapienza/pg2s
cd pg2s
pip install .
```
or from pip:
```
pip install pg2s
```
#### Usage
To use the pg2s_score, you need to define:

1. a tuple of list tuples, containing the tasks and for each of them the truth and prediction actions;
2. an hyperparameter alpha that can be tuned to give more importance to 
    the goal-wise similarity or to the sentence-wise similarity. Default value is 0.5
Here is how to call the function in your Python code:

```
from pg2s.metric import pg2s_score

plans = {
    "name-task-1": {
        'truth':[
            'Action 1',
            'Action 2',
            ...
            'Action N'
                    ],
        'predict':[
            'Action 1',
            'Action 2',
            ...
            'Action M'
        ]
    },
}

# Calculate the similarity score with a custom alpha value
score = pg2s_score(plans, alpha=0.7)
print(f"PG2S Score: {score}")
```