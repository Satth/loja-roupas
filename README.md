<div align="center">

# Loja de Roupas

**Sistema de domínio para uma loja de roupas desenvolvido em Python, com foco em orientação a objetos, regras de negócio, estratégias de promoção, testes automatizados e integração contínua.**

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat-square\&logo=python\&logoColor=white)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Testes-pytest-0A9EDC?style=flat-square\&logo=pytest\&logoColor=white)](https://docs.pytest.org/)
[![Git](https://img.shields.io/badge/Versionamento-Git-F05032?style=flat-square\&logo=git\&logoColor=white)](https://git-scm.com/)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?style=flat-square\&logo=githubactions\&logoColor=white)](https://github.com/features/actions)
[![Tests](https://img.shields.io/badge/Tests-30-2EA44F?style=flat-square)](#testes)

</div>

---

## Sobre

A **Loja de Roupas** é uma aplicação de pequeno porte que modela algumas das principais regras de um domínio de comércio de roupas.

O projeto trabalha com produtos, carrinho de compras, cálculo de subtotal, frete, promoções e especializações de produtos. A estrutura foi organizada para manter responsabilidades separadas e permitir que as regras de negócio sejam verificadas por testes automatizados.

O domínio atual utiliza conceitos de orientação a objetos como:

* composição entre objetos;
* encapsulamento;
* herança;
* sobrescrita de métodos;
* polimorfismo;
* classes abstratas;
* contratos de comportamento;
* tratamento de exceções.

Além da execução local, o projeto possui uma suíte automatizada com **30 testes** e um workflow de **GitHub Actions** para validar as alterações do repositório.

---

## Funcionalidades

### Produtos

O sistema possui uma classe base `Produto` responsável por representar itens da loja.

Cada produto possui:

* nome;
* preço;
* tamanho;
* descrição formatada.

As validações garantem que:

* o nome não seja vazio;
* o preço seja maior que zero;
* o tamanho pertença à tabela permitida.

Tamanhos disponíveis:

```text
PP
P
M
G
GG
```

O domínio também possui especializações de `Produto`, como:

* `Camiseta`
* `Calca`

Essas classes reutilizam as validações da classe base e podem sobrescrever comportamentos específicos.

---

## Carrinho

A classe `Carrinho` concentra as operações relacionadas à compra.

Os produtos são armazenados internamente como pares:

```text
(produto, quantidade)
```

O carrinho fornece:

* adição de produtos;
* validação de quantidade;
* cálculo de quantidade de peças;
* cálculo de subtotal;
* aplicação de promoção;
* cálculo do frete;
* finalização do carrinho.

O acesso aos itens utiliza uma cópia da coleção interna para evitar alterações externas no estado do objeto.

Um carrinho finalizado também não pode receber novos produtos.

---

## Promoções

As promoções seguem um contrato definido pela classe abstrata `Promocao`.

```python
from abc import ABC, abstractmethod


class Promocao(ABC):

    @abstractmethod
    def aplicar(self, subtotal):
        ...
```

O método `aplicar()` define o comportamento esperado pelas diferentes estratégias de desconto.

Implementações disponíveis:

```text
SemPromocao
Percentual
Cupom
```

### `SemPromocao`

Mantém o subtotal original.

### `Percentual`

Aplica um desconto percentual entre `0` e `100`.

Exemplo:

```text
Subtotal:       R$ 249,60
Desconto: 10%
Após desconto:  R$ 224,64
```

### `Cupom`

Aplica um desconto de valor fixo, sem permitir que o resultado fique negativo.

Exemplo:

```text
Subtotal:       R$ 249,60
Cupom:          R$ 100,00
Após desconto:  R$ 149,60
```

A validação do contrato impede que objetos incompatíveis sejam utilizados como promoção.

---

## Regras de negócio

### Subtotal

O subtotal é calculado a partir da relação entre preço e quantidade:

```text
subtotal = preço × quantidade
```

Exemplo:

```text
3 × Camiseta básica = R$ 119,70
1 × Calça jeans     = R$ 129,90
--------------------------------
Subtotal             = R$ 249,60
```

### Frete

O cálculo utiliza uma regra simples:

| Valor da compra       |    Frete |
| --------------------- | -------: |
| Abaixo de R$ 200,00   | R$ 15,00 |
| A partir de R$ 200,00 |   Grátis |

A fronteira é inclusiva: uma compra de exatamente **R$ 200,00** não paga frete.

O frete é calculado sobre o valor após a aplicação da promoção.

---

## Arquitetura

A estrutura do domínio é dividida em módulos com responsabilidades específicas:

```text
                    +------------------+
                    |     vitrine.py   |
                    +--------+---------+
                             |
                             v
+----------------+   +------------------+   +------------------+
|  produto.py    |<--|   carrinho.py    |-->|   promocao.py    |
|                |   |                  |   |                  |
| Produto        |   | Carrinho         |   | Promocao (ABC)   |
| Camiseta       |   | Itens            |   | SemPromocao      |
| Calca          |   | Subtotal         |   | Percentual       |
| Validações     |   | Total            |   | Cupom            |
+----------------+   | Finalização      |   +------------------+
                     +---------+--------+
                               |
                               v
                     +------------------+
                     |   calculos.py    |
                     |                  |
                     | total_carrinho() |
                     | frete()          |
                     +------------------+

                         tests/
                            |
                            v
                    Validação das regras
```

A separação permite que os cálculos básicos permaneçam independentes enquanto o `Carrinho` coordena os diferentes componentes do domínio.

---

## Estrutura do projeto

```text
loja-roupas/
├── .github/
│   └── workflows/
│       └── testes.yml
│
├── loja/
│   ├── __init__.py
│   ├── calculos.py
│   ├── carrinho.py
│   ├── produto.py
│   └── promocao.py
│
├── tests/
│   ├── __init__.py
│   ├── test_calculos.py
│   ├── test_carrinho.py
│   ├── test_contrato.py
│   ├── test_heranca.py
│   ├── test_produto.py
│   └── test_promocao.py
│
├── .gitignore
├── experimento.py
├── pytest.ini
├── requirements.txt
├── vitrine.py
└── README.md
```

### Responsabilidades

| Arquivo                        | Responsabilidade                                |
| ------------------------------ | ----------------------------------------------- |
| `loja/calculos.py`             | Cálculo do subtotal e frete                     |
| `loja/produto.py`              | Produtos, validações e especializações          |
| `loja/carrinho.py`             | Estado e regras do carrinho                     |
| `loja/promocao.py`             | Contrato e estratégias de promoção              |
| `vitrine.py`                   | Exemplo inicial de utilização dos dados da loja |
| `tests/`                       | Validação automatizada do domínio               |
| `.github/workflows/testes.yml` | Execução automática da suíte de testes          |

---

## Exemplo de uso

Um carrinho pode ser criado e utilizado da seguinte forma:

```python
from loja.carrinho import Carrinho
from loja.produto import Produto
from loja.promocao import Percentual

carrinho = Carrinho(Percentual(10))

carrinho.adicionar(
    Produto("Camiseta básica", 39.90, "M"),
    3
)

carrinho.adicionar(
    Produto("Calça jeans", 129.90, "G")
)

print(carrinho.quantidade_de_pecas)
print(carrinho.subtotal)
print(carrinho.total)
```

Para o exemplo acima:

```text
Quantidade de peças: 4
Subtotal:            R$ 249,60
Promoção:            10%
Após desconto:       R$ 224,64
Frete:               R$   0,00
Total:               R$ 224,64
```

---

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/Satth/loja-roupas.git
cd loja-roupas
```

### 2. Criar o ambiente virtual

```bash
python -m venv .venv
```

No Git Bash:

```bash
source .venv/Scripts/activate
```

No PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

## Testes

O projeto utiliza **pytest** para validar as regras do domínio.

A suíte atual possui **30 testes** distribuídos entre cálculos, carrinho, produtos, herança, promoções e contratos.

### Executar toda a suíte

```bash
pytest
```

### Executar com detalhes

```bash
pytest -v
```

### Executar um arquivo específico

```bash
pytest tests/test_carrinho.py
```

### Áreas cobertas

Os testes verificam, entre outras regras:

* cálculo de subtotal;
* cálculo de frete;
* frete grátis a partir de R$ 200,00;
* validações de produtos;
* quantidade de itens;
* proteção da coleção interna;
* finalização do carrinho;
* comportamento de promoções;
* limites de percentual;
* cupons que não resultam em valores negativos;
* herança e sobrescrita;
* contrato abstrato de `Promocao`;
* rejeição de objetos que não implementam o contrato esperado.

---

## Integração contínua

O projeto possui um workflow de GitHub Actions em:

```text
.github/workflows/testes.yml
```

O workflow é executado em `push` e `pull_request` e realiza:

```text
Checkout do repositório
        |
        v
Configuração do Python
        |
        v
Instalação das dependências
        |
        v
Execução do pytest
        |
        v
Resultado da suíte
```

Isso permite verificar automaticamente se as alterações continuam compatíveis com as regras existentes.

---

## Desenvolvimento

O projeto utiliza Git para versionamento e trabalha com alterações incrementais.

Um fluxo básico de desenvolvimento:

```bash
git status
git add .
git commit -m "Describe the change"
git push
```

Antes de publicar uma alteração:

```bash
pytest
```

A intenção é manter cada mudança pequena, verificável e relacionada a uma responsabilidade específica.

---

## Tecnologias

| Tecnologia     | Utilização                |
| -------------- | ------------------------- |
| Python 3.14    | Linguagem principal       |
| pytest         | Testes automatizados      |
| Git            | Controle de versão        |
| GitHub         | Hospedagem do repositório |
| GitHub Actions | Integração contínua       |

---

## Origem

Este projeto foi desenvolvido originalmente como uma atividade prática da disciplina **Coding — Linguagens e Técnicas**.

---

<div align="center">

<sub>Python · OOP · Pytest · Git · GitHub Actions</sub>

</div>
