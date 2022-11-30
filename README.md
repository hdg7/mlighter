# MLighter

MLighter is a tool for machine learning testing that aims to integrate three testing levels: performance, security and reliability. The tool can be used as a library although it also contains a graphical user interface that aims to connect all the different levels.

The tool also comes with a Docker container to make your life easier. If you want to install it, please follow the instructions underneath.

If you use MLighter, please cite the paper:

Menendez, Hector D. (2022). Measuring Machine Learning Robustness in front of Static and Dynamic Adversaries. In Measuring Machine Learning Robustness in front of Static and Dynamic Adversaries. IEEE 34rd International Conference on Tools with Artificial Intelligence (ICTAI).

@incollection{menendez2022measuring,
  title={Measuring Machine Learning Robustness in front of Static and Dynamic Adversaries},
  author={Menendez, Hector D.},
  booktitle={Measuring Machine Learning Robustness in front of Static and Dynamic Adversaries},
  year={2022},
  publisher={IEEE 34rd International Conference on Tools with Artificial Intelligence (ICTAI)}
}


## Testing Models Reliability.

This section allows to use a model and test its reliability under adversarial conditions. Currently, we allow only models in SKlearn. You just need to include an instance of your input data and test your model directly. Remember that the model needs to respect the 

## Testing Bugs in Code.

## Identifying Performance Issues.

## Graphical User Interface

The User Interface is based on Vue and it is perform in top of a dashboard to make it more flexible for visualization porposes. 
