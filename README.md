# Sistema de Consulta para Investimentos

Este projeto é um sistema de consulta voltado para investidores que desejam monitorar indicadores econômicos, acompanhar ativos e estimar o preço teto de Fundos Imobiliários (FIIs) utilizando o modelo de Gordon. A aplicação foi desenvolvida com **Streamlit** para interface frontend e utiliza a biblioteca **python-bcb** para recuperar dados financeiros atualizados como **IPCA**, **CDI** e **SELIC**.

---

## Funcionalidades

### 📊 Indicadores Econômicos
- Consulta automática de indicadores como **IPCA**, **CDI** e **SELIC**, diretamente da base do Banco Central utilizando a biblioteca `python-bcb`.
- Exibição clara e organizada dos dados econômicos para auxiliar na tomada de decisão.

### 📈 Acompanhamento de Ativos
- Monitoramento de Fundos Imobiliários (FIIs) e outros ativos financeiros.
- Integração simples para acompanhar as variações de preços e rendimento.

### 💡 Estimativa de Preço Teto
Implementação do _Modelo de Gordon_ para calcular o preço teto de FIIs, baseado em:
- Dividendos esperados
- Taxa de crescimento
- Taxa de desconto

### 🖥️ Interface Intuitiva
- Desenvolvido com **Streamlit**, oferecendo uma interface fácil de usar, interativa e responsiva.
- Possibilidade de entrada de dados personalizada para os usuários, como o ticker do ativo (ex.: `HGLG11.SA`).

---

## Tecnologias Utilizadas

- **Streamlit**: Interface frontend para exibição e interação com o usuário.
- **Python**: Lógica principal e cálculos.
- **python-bcb**: Recuperação de dados financeiros do Banco Central do Brasil.
- **Modelo de Gordon**: Fórmula aplicada para estimar o preço teto de FIIs.

---

## Como Executar o Projeto

### Clone o Repositório:
```bash
git clone https://github.com/issjunior/consulta-fii.git
```
---

## Instale as Dependências:
```bash
pip install -r requirements.txt
```

---

Execute a Aplicação:
```bash
streamlit run Home.py
```

---

## Acesse no Navegador:
O Streamlit abrirá automaticamente no navegador ou estará disponível em http://localhost:8501.

