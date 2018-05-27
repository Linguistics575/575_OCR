## Wrapper to do Handwriting Recognition (and also regular OCR) calling the Microsoft Azure Cognitive Services API.
This script will read in a locally stored image, present it to the Microsoft Azure Computer Vision API to do handwriting recognition on it, and retrieve and return the result.  It can also be used to do optical character recognition on typewritten text.
* Images must be less then 4MB and smaller than 3200 pixes x 3200 pixels, in JPEG, PNG, GIF, or BMP formats.
* For handwriting recognition, you'll get 2 output files:
  * A `.recognized.txt` file that has the recognized text
  * An `.annotated.png` file that will consist of the input image with the recognized text superimposed upon it
* For OCR, only the `.recognized.txt` file is output.


### Pre-requisities:
1.  You'll need a subscription key for the "Computer Vision API" key from Microsoft.  At the time of this writing, there is a free version that will get you 5000 transactions per month and allow you a transaction rate of 20 transactions per minute.  There is a paid version for $2.50 per 1000 transactions with a transaction rate of 10 transactions per second.  If you are a student, or have a `.edu` e-mail address, it would be most advantageous to get a student subscription [here](https://azure.microsoft.com/en-us/free/students/).  It will give you $100 in credit, which is plenty to run the recognition software on a host of documents, at a rate of 10 transactions per second!  Additionally, when the credit is exhausted, you can still recognize documents at the 20-transactions-per-minute rate.  If you are not a student, obtain either a free or paid subscription key [here](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/vision-api-how-to-topics/howtosubscribe). 

2.  When you get the subscription key, it will be for a particular region, with a particular URL that has to go into the `config.yml` file.  Have a look at the `config.yml` file for an example.  The URL will be something like `https://<YOUR REGION HERE>.api.cognitive.microsoft.com/vision/v1.0/RecognizeText`

3.  The subscription key itself should go in a file, `key_file.key` might be a handy name.  Then put the path to the key file in the `config.yml`.  (Pardon the extra step.  Just keeps it a little more secure since this is on github.)  See `sample_key_file.key` for an example.


### Installation Instructions
1.  The easiest way to use this tools is to simply download this repository.  TODO: pointer to downloading the repo.)  Experienced git users may find it more convenient to clone it.
1. Our tools are written in Python3; therefore, you will need to have Python installed on your computer.  For experienced pythonistas, simply setup a python3 environment using the `requirements.txt` file.  For everyone else, read on:
   * We recommend the `Miniconda` python distribution.  If you do not already have pythong on your machine, download and install the Python 3.6 version of `Miniconda` for your platform [here](https://conda.io/miniconda.html).  TODO: Walk through installing Miniconda.
   * You will set up a separate "virtual environment" to run our tools in.  "Virtual envrionments" contain all the dependencies and packages required to run our code.  However, you may have other python tools on your system, which may have different dependencies, which may even conflict with those needed here.  To avoid these troubles, we will set up a "virtual environment" for our tools, which must be activated.  This will keep the azure environment separate from the environments you may otherwise need.  Follow the instructions for your platform below:
   * ##### Further instructions for Windows users:
        1. launch the `Anaconda command prompt` from the start menu, or, if you added anaconda to your path in step 2 above, simply start a windows command line.
        2. Navigate to the `azure` directory from the command line.  The easiest way is to copy the path from the address bar in windows explorer to the clipboard.  Then on the command line, type `cd`,  then right-click anywhere in the window, and select `paste`.  (Unfortunately, `ctrl+v` will not work.)
        3. type `install_azure_environment.bat`, and hit `Enter.`  You will see various messages scroll across the screen as the dependencies for the recognizer are installed.  This may take several minutes, and at times, the screen may appear to hang, as if if nothing is happening at all.  Within a few minutes, however, things should get moving again.  If all goes well, the last thing you see should be a message saying that the installation was successful, and the following instructions:
            * `To begin using the azure environment, type "activate".`
            * `When you are finished, type "deactivate" `
        4. to begin using the azure environment, type "activate" as per the instructions.   You are now ready to submit an image containing handwritten text to the Azure recognizer as in the [Usage](#usage) section below.  When you are finished, you can type "deactivate," or simply close the window.

   * ##### Further instructions for *nix and Mac users:
        1. Start a terminal session
        2. Navigate to the `azure directory`. TODO: Find out more about what this looks like on a mac.
        2. Type `install_azure_environment.sh` on the command line and hit `enter`.  You will see various messages scroll across the screen as the dependencies for the recognizer are installed.  This may take several minutes, and at times, the screen may appear to hang, as if if nothing is happening at all.  Within a few minutes, however, things should get moving again.  If all goes well, the last thing you see should be a message saying that the setup of the environment is complete, and the following instructions:
            * `To activate environment, type "source activate"`
            * `to deactivate, type "deactivate"`
            * When you are finished, type "deactivate" 
        4. to begin using the azure environment, type "source activate" as per the instructions.   You are now ready to submit an image containing handwritten text to the Azure recognizer as in the [Usage](#usage) section below.  When you are finished, you can type "deactivate," or simply close the terminal.  

### Usage
You can run this on a single image, or on a file containing the paths to as many images as you like.
The form of the command will be:
`python recognize_text.py config_file (-i INPUT_IMAGE | -f FILE_OF_INPUT_PATHS) [-o OUTPUT_DIRECTORY] [--ocr]`
* `config_file` is the config file containing the API URL and the path to the file containing your subscription key.
* To run recognition on a single image, the next would be `-i INPUT_IMAGE`, or, to run a batch of images, it would be `-f FILE_OF_INPUT_PATHS`.
* If you'd like the output to go anywhere other than the current directory you can pass `-o OUTPUT_DIRECTORY`, or just leave it out for the current directory.
* If you'd like to run optical character recognition for typewritten text as opposed to handwriting, pass `--ocr`. 

#### Examples:
* for Handwriting recognition for a single file:
   * `python recognize_text.py config.yml -i my_image_file.png [-o my_output_directory]`
* for Handwriting recognition for a batch of files:
   * `python recognize_text.py config.yml -f file_with_a_list_paths.txt [-o my_output_directory]`
* for OCR recognition (of printed, typewritten text) for a single file:
   * `python recognize_text.py config.yml -i my_image_file.png [-o my_output_directory] --ocr` 
* for OCR recognition (of printed, typewritten text) for a batch of files:
   * `python recognize_text.py config.yml -f file_with_a_list_paths.txt [-o my_output_directory] --ocr`