# analisador_texto_pt_br_e_eng

Description. 
The package analisador_texto_pt_br_e_eng is used to:
	-Analisa os textos em português ou em inglês, identificando palavras mais comuns, removendo stopwords e realizando outras análises de texto.
	-Usa a biblioteca spaCy para processamento de linguagem natural em ambas as línguas.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install package_name

```bash
pip install analisador_texto_pt_br_e_eng
```

## Usage

```python
from analisador_texto_pt_br_e_eng.analisador_texto_pt_br import pt_br
pt_br.analisar_texto("Seu texto em português aqui.")
```

```
from analisador_texto_pt_br_e_eng.analisador_texto_eng import eng
eng.analyze_text("Your English text here.")
```
## Author
Alexsandro

## License
[MIT](https://choosealicense.com/licenses/mit/)