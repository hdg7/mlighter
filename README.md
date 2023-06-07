# MLighter

<br />
<img align="left" src="http://mlighter.freedevelop.org/wp-content/uploads/2022/02/cropped-logo5.png" width="140" height="160"/>

MLighter is a tool for machine learning testing that aims to integrate three testing levels: performance, security and reliability. The tool can be used as a library although it also contains a graphical user interface that aims to connect all the different levels.

The tool also comes with a Docker container to make your life easier. If you want to install it, please follow the instructions underneath.

<br />

## History

MLighter comes from an Innovate UK project funded under the CyberASAP programme. To get more information about the project, you can visit the presentation website from Innovate UK:

https://iuk.ktn-uk.org/projects/cyberasap/mlighter/

Also, you can visit our official demo video here:

https://vimeo.com/678127987?embedded=true&source=vimeo_logo&owner=4798738

## Citation

If you use MLighter, please cite the paper:

*Menendez, Hector D. (2022). Measuring Machine Learning Robustness in front of Static and Dynamic Adversaries. In Measuring Machine Learning Robustness in front of Static and Dynamic Adversaries. IEEE 34rd International Conference on Tools with Artificial Intelligence (ICTAI).*

```
@incollection{menendez2022measuring,
  title={Measuring Machine Learning Robustness in front of Static and Dynamic Adversaries},
  author={Menendez, Hector D.},
  booktitle={Measuring Machine Learning Robustness in front of Static and Dynamic Adversaries},
  year={2022},
  publisher={IEEE 34rd International Conference on Tools with Artificial Intelligence (ICTAI)}
}
```

## Testing Models Reliability.

This section allows to use a model and test its reliability under adversarial conditions. Currently, we allow only models in SKlearn. You just need to include an instance of your input data and test your model directly. Remember that the input needs to respect the models feature space. If you want to see how to use it via the interface, check the manual. 

## Testing Bugs in Code.

This part of the tool in based on fuzzing and aims to identify crashes in the code. To run this part you need to create a parametrized template of your code so the fuzzer can start applying different strategies to it. We use afl-based fuzzers so you need to prepare your code in a way that is compatible. Our system uses afl-init as a starting point for the testing. For an example, check the tests folder. The tester will create a screen instance running the fuzzer so you do not need to worry if you have to close your interface.

## Identifying Performance Issues.

The part extends the previous one to also identify hangs in the code depending on the parameters.

## Graphical User Interface

The User Interface is based on Vue and Voila. It is performed in top of a dashboard to make it more flexible for visualization porposes. 

## Installing MLighter

Please check the docker file if you want to see the specific libraries that you need to install. We have tested the system in 8064 architectures, but we are aware that Arm64 architectures are not compatible with the libraries of the Docker file.

## Running Docker

If you want to create and run the docker file, you should use:
```
docker build . --network=host --tag=mlighter
```

If you need to run it use:
```
docker run --cpus="1.0" --network host -it mlighter:latest
```

However, if you need to take outputs form the testing code section, you can use a local folder with 

```
docker run --cpus="1.0" --network host -v ~/outputs_test:/home/advml/outputs -it mlighter:latest
```

Feel free to replace the CPUs by the number of CPUs you want to use.

Once docker is running, it will activate the GUI, you can access through the browser in: localhost:8888

## Running MLigther as a library

Please check the tests to see some examples.

## Pending Tasks

We have a lists of pending task that we are aware. Some examples are:

* We need to improve the parametrization of the GA adversary in the GUI.
* Automate the instrumentation of the testing phase.
* Automate the selection of the fuzzer.
* Include images and audios as inputs.
* Include NLP based inputs and transformations.
* Extend the interface to TensorFlow and PyTorch.

We aim to cover some of these tasks during 2023. 
