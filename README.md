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

*Menendez, Hector D. (2022). Measuring Machine Learning Robustness in front of Static and Dynamic Adversaries. In Measuring Machine Learning Robustness in front of Static and Dynamic Adversaries. IEEE 34th International Conference on Tools with Artificial Intelligence (ICTAI).*

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

In order to run the code testing, you will need to install mlighter-utils, which can be done with:
```bash
./mlighter/utils/install.sh
```


## Running Docker

If you want to create and run the docker file, you should use:
```
docker build . --network=host --tag=mlighter
```

If you need to run it use:
```
docker run --network host -it mlighter:latest
```

There are four options for running the container: Deploy, Develop, debug and model. To use them open the container directly and run the app, use deploy:
```
sudo docker run -it --rm -p 8888:8888 mlighter:latest deploy 
```

If you want to activate it as a library, use develop and this will activate a Jupyter notebook. Debug will open a bash to access the container. Finally, model will allow to use ollama models.

However, if you need to take outputs form the testing code section, you can use a local folder with 

```
docker run --network host -v ~/outputs_test:/home/advml/outputs \
  -it mlighter:latest deploy
```

If you need to run docker with GPU support you just need to include your graphics information on the command. This is important if you want to test PyTorch or TensorFlow models / implementations:

```
docker run --network host --runtime=nvidia --gpus all -v ~/outputs_test:/home/advml/outputs  -it mlighter:latest deploy
```

If you do not have docker-Nvidia working, please check the end of this README.

Once docker is running, it will activate the GUI, you can access through the browser in: localhost:8888

## Running MLigther as a library

Please check the tests to see some examples.

## Troubleshooting

Some of the common problems with the system are:

### Docker and NVidia are not compatible

This is an example about how to install docker-nvidia in Ubuntu. You need to start by adding the apt sources of NVidia:

```
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
            sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

Then you can install it and restart docker. Be careful, all of your containers will be restarted.
```
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo apt-get install nvidia-container-toolkit-base
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## Pending Tasks

We have a lists of pending task that we are aware. Some examples are:

* We need to improve the parametrization of the GA adversary in the GUI.
* Automate the instrumentation of the testing phase.
* Automate the selection of the fuzzer.
* Include images and audios as inputs.
* Include NLP based inputs and transformations.
* Extend the interface to TensorFlow and PyTorch.

We aim to cover some of these tasks during 2023. 

## Developers

The repository aims to follow a Gitflow approach. Please use the dev branch instead of main for branching and create new features. The branches are organised as follow:
- main: deployment branch should be always functional.
- dev: for development, for new features create a new branch from dev.
- hotfix-*: for fixing specific bugs found in main, make a pull request once merge.
- feature-*: for new features. Please derive from dev.
- release-*: for new releases. Please derive from dev.

