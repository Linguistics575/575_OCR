# Evaluation of MS Handwriting Recognizer on sample from IAM Handwriting database.

### Procedure:
1. Pulled sample of 100 forms from IAM database, using [take_evaluation_sample.py](https://github.com/Linguistics575/575_OCR/blob/master/evaluation/IAM-evaluation-sample/take_evaluation_sample.py).  Identfiers for the sample are in [sample_forms.ls](https://github.com/Linguistics575/575_OCR/blob/master/evaluation/IAM-evaluation-sample/sample_forms.ls).

2. Manually cropped images so that they only contained the handwritten portion (and not the printed text at the top of the page) and so that they conformed with the size requirements of the API. The cropped images are in the `sample_png_files` directory.

3. Created gold-standard transcription files by parsing the `lines.txt` file from the IAM database.  (It does not offer a transcription, but rather a tagged, tokenized version of the text.  (I did not "untokenize" the text.  Used [this script](https://github.com/Linguistics575/575_OCR/blob/master/evaluation/IAM-evaluation-sample/create_IAM_gold_standards.py).  The gold-standard transcriptions are in the `sample_gold_standards` directory.

3. Ran the images through the Azure API and capured the output.  The output is in the `sample_output`.

4. Calculated WER for the sample [script](https://github.com/Linguistics575/unlocking-text-main/tree/master/evaluation/WER)]

5. *The WER was 13.64% !!!!*

### Full evaluation results in `evaluation_results.txt`
