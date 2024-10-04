import os, sys
import json

import torch
import numpy as np

from transformers import AutoModelForSequenceClassification, AutoTokenizer, BitsAndBytesConfig, pipeline
from accelerate import init_empty_weights, infer_auto_device_map

LOCAL_DIR = os.path.dirname(__file__)
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(LOCAL_DIR)))

from .LLM import LLM


class LLMBARTLargeMNLI(LLM):
    """
    An implementation of the HuggingFace facebook/bart-large-mnli transformer.
    """
    def __init__(self, weights_path: str = None) -> None:
        """
        Initializes the model with ``'facebook/bart-large-mnli'`` for zero-shot classification.

        Args
        ----
        weights_path: str, None
            The path to the folder where the models weights should be saved. If None, the current working 
            directory path will be used instead.

        Note
        ----
        - For the full float32 model, requires 1Go of RAM/VRAM. 
        - Multiple encoding tasks may be supported. See ``load_model()``.
        """
        super().__init__(model_name="facebook/bart-large-mnli", weights_path=weights_path)

        return None


    def load_model(self, task: str = "zero-shot-classification"):
        """
        Loads the facebook/bart-large-mnli model for zero-shot classification.

        Args
        ----
        task: str, 'zero-shot-classification'
            The task to use this encoder for. Default is zero-shoot-classification.
        
        Note
        ----
        - Quantization is not available.
        """
        supported_tasks = ["zero-shot-classification"]
        if task not in supported_tasks:
            print("LLMEncoderBARTLargeMNLI >> Task not supported, the pipeline will likely break."
                  "Supported tasks are:", *supported_tasks)

        # MODEL SETUP (loading)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_folder, 
            trust_remote_code=True, 
            quantization_config=None, 
            # device_map=device_map
        )

        # TOKENIZER SETUP (loading)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_folder, clean_up_tokenization_spaces=True)

        # PIPELINE SETUP (init)
        self.pipe = pipeline(task, 
                             model=self.model,
                             tokenizer=self.tokenizer)
        
        return True

    def sample_model(self):
        pass

    def train_model(self):
        pass

    def test_model(self):
        pass

    def evaluate_model(self, 
                    prompt: str, 
                    candidate_labels: list[str], 
                    hypothesis_template: str = "This text is about {}.", 
                    multi_label: bool = False,
                    display: bool = False) -> dict:
        """
        Classifies the prompt using zero-shot classification.

        Args
        ----
            prompt: str
                The prompt to classify.
            candidate_labels: list[str] 
                The list of candidate labels for classification.
            hypothesis_template: str, 'This text is about {}.'
                The template for hypothesis generation. Default is "This text is about {}."
            multi_label: bool
                Whether to perform multi-label classification. Default is False.
                If ``multi_label==True``, returns every label logit, otherwise returns the most likely label.
            display: bool
                Whether to print the model output. Default is True.

        Returns
        -------
            classification_result: dict
                The classification results as a sorted dictionnary. Dictionnary structure is {label: prob} where label is a string, prob is a float between 0 and 1.
                If ``multi_label==False`` returns a one element list
        """

        result = self.pipe(prompt, candidate_labels=candidate_labels, multi_label=multi_label, hypothesis_template=hypothesis_template)
        
        scores = result["scores"]
        labels = result["labels"]

        classification_result = dict(sorted(dict(zip(labels, scores)).items(), key=lambda item: item[1], reverse=True)) # ensures output is sorted
        if not multi_label:
            key = next(iter(classification_result)) # retreives first key
            classification_result = {key: classification_result[key]} # 'truncates' the dictionnary to keep the first key/value pair only

        if display:
            print("LLMBARTLargeMNLI >> Model output:", json.dumps(result, indent=4))

        return classification_result



