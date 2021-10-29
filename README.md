# ENEAYTScript
## Summary
* [System information](https://github.com/Neagu-Andrei/ENEAYTScript/new/main?readme=1#system-information-and-configuration)
* [Pip](https://github.com/Neagu-Andrei/ENEAYTScript/new/main?readme=1#pip)
* [Selenium 4.0.0](https://github.com/Neagu-Andrei/ENEAYTScript/new/main?readme=1#selenium-400)
* [SciPy](https://github.com/Neagu-Andrei/ENEAYTScript/new/main?readme=1#scipy)
* [PyAudio](https://github.com/Neagu-Andrei/ENEAYTScript/new/main?readme=1#pyaudio)
* [Pydub](https://github.com/Neagu-Andrei/ENEAYTScript/new/main?readme=1#pydub)
* [PyAutoGUI](https://github.com/Neagu-Andrei/ENEAYTScript/new/main?readme=1#pyautogui)
* [Usage](https://github.com/Neagu-Andrei/ENEAYTScript/new/main?readme=1#usage)

### System information
***
##### OS: Windows 10 Version 20H2
##### IDE: PyCharm 2019.2.3 (Community Edition)
##### Running Python 3.7


### Pip
***
Pip is used to fetch packages from Python Package Index
##### Check if we have pip installed
In command prompt run  
`py -m pip --version`
##### Install pip
Run  
`py -m ensurepip --upgrade`
##### Upgrade pip
`py -m pip install --upgrade pip`
 

### Selenium 4.0.0
***
##### Install Selenium
To install Selenium 4.0.0 run in command prompt:  
`pip install -U selenium`
##### Drivers  
Now that we have Selenium installed we need to get the driver for our browser. In my case, that is the [Chrome Driver](https://chromedriver.chromium.org/downloads).  
To check which version of Chrome you are using follow this path:  
_Customize and control Google Chrome > Help > About Google Chrome_  
Once we have our driver downloaded, we should extract the driver in our project file.  


### SciPy
***
Scipy is a python library used for scientific computing. Though not used in this project as of now, it is extremely useful in dealing with sound waves.
##### Install Scipy
In command prompt run:  
`pip install scipy`

### PyAudio
***
PyAudio is an audio I/0 library. We will be using it to record and write audio files.
Here PyAudio gets a bit more tricky:  
Since PyAudio wheels are not **officially** compatible with Python 3.7 we have to find a work around.  
For that we will need to install **pipwin**.
##### What is pipwin?
Pipwin is a tool for pip that allows the installation of unofficial python packages.  
To install it, simply run `pip install pipwin`
##### Install PyAudio
Once we have pipwin installed, we can use it to install our PyAudio library.  
`pipwin install pyaudio`

### PyDub
***
PyDub is another library that handles audio files. It is extremely useful in Signal Processing, as well as, playing, merging, splitting audio files
##### Install PyDub
Like we did before, in the command prompts run:  
`pip install pydub`

### PyAutoGUI
***
PyAutoGUI is a library that let's you control the mouse and keyboard, display alerts, locate an application window and to take screenshots. The 
last part is what we will need for our project.  
##### Install PyAutoGui
Run command: `pip install pyautogui`

### Socket
***
A Python Interface that allows us to deal with various socket system calls. We will be using it to check our Internet connection throughout our project.  
The socket module is found in the Python Standard Library thus it does not require any kind of installation.


### Usage
***
Our Project uses Selenium to open YouTube, agree to cookies, search or select a recommended video and to skip the ad, if it's possible.
With Socket we constantly check to see if we have a network connection and while the clip is running we use libaries like PyAutoGui (to take screenshots that will be later
converted to a video) and PyAudio (to record the sound from the Stereo Mix) to create a screen recording. Once we compile both files we look at the intensity of the sound
wave to determmine the "loudness" of the sound in dB and write the output in a csv file.
