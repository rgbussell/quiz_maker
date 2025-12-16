# quiz_maker
LLM-based Quiz Maker Using Vision, OCR and local LLMs

### Set up the API calls to an LLM
Uses API calls to Grok to generate text.

## setup/install
Install code and dependencies by running install/setup.sh

## API KEY
Your api key needs to be referenced in the .env file
This file is not pushed to repo for security concerns but
the .env.template file will show you the correct format

## Progress
Basic backbone is running. We can input through a camera,
use OCR to interpret and generate quiz questions.

## To Do
Improve the image to text conversion
OCR model does not handle lighting conditions and perspective robustly
Use an image segmentation to detect paper orientation and apply
affine transform prior to OCR.

