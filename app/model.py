from functools import lru_cache
import logging

import torch
from langchain_core.language_models.llms import LLM
from pydantic import PrivateAttr
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

LOGGER = logging.getLogger("app.model")


class LocalFlanT5(LLM):
    model_name: str = "google/flan-t5-base"
    max_new_tokens: int = 256
    _model = PrivateAttr()
    _tokenizer = PrivateAttr()

    def model_post_init(self, __context) -> None:
        LOGGER.info("Carregando tokenizer do modelo %s", self.model_name)
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        LOGGER.info("Carregando pesos do modelo %s", self.model_name)
        self._model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
        self._model.eval()
        LOGGER.debug("Modelo pronto para inferencia")

    @property
    def _llm_type(self) -> str:
        return "local_flan_t5"

    def _call(self, prompt: str, stop=None, run_manager=None, **kwargs) -> str:
        if stop:
            raise ValueError("Stop sequences are not supported by LocalFlanT5.")

        LOGGER.info("Gerando resposta para prompt com %s caracteres", len(prompt))
        LOGGER.debug("Preview do prompt: %s", prompt[:400].replace("\n", " "))
        inputs = self._tokenizer(prompt, return_tensors="pt", truncation=True)
        LOGGER.debug("Prompt tokenizado em %s tokens", inputs["input_ids"].shape[-1])

        with torch.no_grad():
            output_ids = self._model.generate(
                **inputs,
                max_new_tokens=kwargs.get("max_new_tokens", self.max_new_tokens)
            )

        output = self._tokenizer.decode(output_ids[0], skip_special_tokens=True)
        LOGGER.info("Resposta gerada com %s caracteres", len(output))
        LOGGER.debug("Resposta do modelo: %s", output)
        return output


@lru_cache(maxsize=1)
def get_llm():
    LOGGER.info("Inicializando LLM local")
    return LocalFlanT5()
