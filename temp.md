# CLI

Passo a passo para teste das novas funcionalidades da CLI entregues até a R1.

- **F1**: Comando _get_ -> ```measuresoftgram get --help```

![Imagem do comando measuresoftgram get --help](https://media.discordapp.net/attachments/1005091228544684153/1006585817633919007/Captura_de_tela_de_2022-08-09_12-31-47.png)
<figcaption style="text-align: center">Imagem 1. Exemplo do helper do comando 'get' da CLI</figcaption>

- **F2**: Comando _import_ -> ```measuresoftgram import --help```

![Imagem do comando measuresoftgram import --help](https://media.discordapp.net/attachments/1005091228544684153/1006585818019799060/Captura_de_tela_de_2022-08-09_12-32-17.png)
<figcaption style="text-align: center">Imagem 2. Exemplo do helper do comando 'import' da CLI</figcaption>

## Antes de começar

- Rode o comando via terminal com o python e o pip instalados:

```bash
pip install measuresoftgram
```

#### Passo 1

- Visualizar a página de help descrita na imagem 2.
- Nela você pode observar que o comando _import_ aceita somente um **output_origin**, que é o _sonarqube_.
- Um parâmetro chamado _dir path_, para endereçar o caminho relativo do diretório que contém os arquivos de output do sonar para serem coletados.
- Um parâmetro chamado _language extension_, para especificar a extensão dos arquivos a serem analisados dentro do projeto (Uma das melhorias previstas é a passagem de uma lista de extensão de arquivos a serem analisados pelo _measuresoftgram_).
- Alguns parâmetros opcionais como:
  - _--host_: O host do service, caso seja necessário.
  - _--organization-id_: Para especificar de qual organização está sendo buscado os dados.
  - _--repository-id_:  Para especificar de qual repositório está sendo buscado os dados.

#### Passo 2

- Rodar o comando:
```bash
measuresoftgram import sonarqube
```

![Imagem do comando measuresoftgram get measures](https://media.discordapp.net/attachments/1005091228544684153/1006590337541738546/Captura_de_tela_de_2022-08-09_12-49-58.png)
<figcaption style="text-align: center">Imagem 3. Exemplo do comando 'get measures' da CLI</figcaption>

#### Passo 3

- Rodar o comando passando um diretório com arquivos json válidos de output do sonar:
```bash
measuresoftgram import sonarqube <DIR PATH>
```

![Imagem do comando measuresoftgram get metrics](https://media.discordapp.net/attachments/1005091228544684153/1006590337919238265/Captura_de_tela_de_2022-08-09_12-50-16.png?width=1287&height=660)
<figcaption style="text-align: center">Imagem 4. Exemplo do comando 'get metrics' da CLI</figcaption>