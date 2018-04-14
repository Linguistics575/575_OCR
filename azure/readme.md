## Wrapper to do Handwriting Recognition (and also regular OCR) calling the Microsoft Azure Cognitive Services API.
This script will read in a locally stored image, present it to the Microsoft Azure Computer Vision API to do handwriting recognition on it, and retrieve and return the result.  It can also be used to do optical character recognition on typewritten text.
* Images must be less then 4MB and smaller than 3200 pixes x 32000 pixels, in JPEG, PNG, GIF, or BMP formats.
* For handwriting recognition, you'll get 3 output files:
  * A `.recognized.txt` file that has the recognized text
  * An `.annotated.png` file that will consist of the input image with the recognized text superimposed upon it
  * A `.json` file, which is the raw output of the API, perhaps useful for debugging.
* For OCR, only the `.json` and `.recognized.txt` files are output.

### Installation Instructions

TODO, but basically get anaconda python distro, install envrionment from requirements file, activate environment

### Pre-requisities:
1.  You'll need a subscription key for the "Computer Vision API" key from Microsoft.  At the time of this writing, there is a free version that will get you 5000 transactions per month and allow you a transaction rate of 20 transactions per minute.  There is a paid version for $2.50 per 1000 transactions with a transaction rate of 10 transactions per second.  Obtain the subscription key [here](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/vision-api-how-to-topics/howtosubscribe), and note the URL for your region. 

2.  When you get the subscription key, it will be for a particular region, with a particular URL that has to go into the `config.yml` file.  Have a look at it.  The URL will be something like `https://<YOUR REGION HERE>.api.cognitive.microsoft.com/vision/v1.0/RecognizeText`
3.  The subscription key itself should go in a file, `key_file.key` might be a handy name.  Then put the path to the key file in the `config.yml`.  (Pardon the extra step.  Just keeps it a little more secure since this is on github.)  See `sample_key_file.key` for an example.

### Usage
You can run this on a single image, or on a file containing the paths to as many images as you like.
The form of the command will be:
`python recognize_text.py config_file (-i INPUT_IMAGE | -f FILE_OF_INPUT_PATHS) [-o OUTPUT_DIRECTORY] [--ocr]`
* `config_file` is the config file containing the API URL and the path to the file containing your subscription key.
* To run recognition on a single image, the next would be `-i INPUT_IMAGE`, or, to run a batch of images, it would be `-f FILE_OF_INPUT_PATHS`.
* If you'd like the output to go anywhere other than the current directory you can pass `-o OUTPUT_DIRECTORY`, or just leave it out for the current directory.
* If you'd like to run optical character recognition for typewritten text as opposed to handwriting 

#### Examples:
* for Handwriting recognition for a single file:
   * `python recognize_text.py config.yml -i my_image_file.png [-o my_output_directory]`
* for Handwriting recognition for a batch of files:
   * `python recognize_text.py config.yml -f file_with_a_list_paths.txt [-o my_output_directory]`
* for OCR recognition (of printed, typewritten text) for a single file:
   * `python recognize_text.py config.yml -i my_image_file.png [-o my_output_directory] --ocr` 
* for OCR recognition (of printed, typewritten text) for a batch of files:
   * `python recognize_text.py config.yml -f file_with_a_list_paths.txt [-o my_output_directory] --ocr`