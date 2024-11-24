Sistema de Consulta para Investimentos:
Este projeto é um sistema de consulta voltado para investidores que desejam monitorar indicadores econômicos, acompanhar ativos e estimar o preço teto de Fundos Imobiliários (FIIs) utilizando o modelo de Gordon. A aplicação foi desenvolvida com Streamlit para interface frontend e utiliza a biblioteca python-bcb para recuperar dados financeiros atualizados como IPCA, CDI e SELIC.

Funcionalidades:
📊 Indicadores Econômicos
Consulta automática de indicadores como IPCA, CDI e SELIC, diretamente da base do Banco Central utilizando a biblioteca python-bcb.
Exibição clara e organizada dos dados econômicos para auxiliar na tomada de decisão.

📈 Acompanhamento de Ativos
Monitoramento de Fundos Imobiliários (FIIs) e outros ativos financeiros.
Integração simples para acompanhar as variações de preços e rendimento.

💡 Estimativa de Preço Teto
Implementação do Modelo de Gordon para calcular o preço teto de FIIs, baseado em:
Dividendos esperados
Taxa de crescimento
Taxa de desconto

🖥️ Interface Intuitiva
Desenvolvido com Streamlit, oferecendo uma interface fácil de usar, interativa e responsiva.
Possibilidade de entrada de dados personalizada para os usuários, como o ticker do ativo (ex.: HGLG11.SA).

Tecnologias Utilizadas
-Streamlit: Interface frontend para exibição e interação com o usuário.
-Python: Lógica principal e cálculos.
-python-bcb: Recuperação de dados financeiros do Banco Central do Brasil.
-Modelo de Gordon: Fórmula aplicada para estimar o preço teto de FIIs.

Como Executar o Projeto
Clone o Repositório:
git clone https://github.com/seu-usuario/sistema-consulta-investimentos.git
cd sistema-consulta-investimentos
Crie um Ambiente Virtual e Ative-o:

python -m venv venv
source venv/bin/activate  # Para Linux/MacOS
venv\Scripts\activate     # Para Windows
Instale as Dependências:

pip install -r requirements.txt
Execute a Aplicação:

streamlit run app.py
Acesse no Navegador:

O Streamlit abrirá automaticamente no navegador ou estará disponível em http://localhost:8501.
Estrutura do Projeto

📂 sistema-consulta-investimentos
├── 📂 img              # Imagens
├── 📂 modulos          # Módulos python
├── 📂 pages            # Organização de links para funções
    └── 📜 Calculadora.py
    └── 📜 De_olho.py
    └── 📜 Índices_e_Títulos.py
    └── 📜 Preço teto_-_FIIs_de_Papel.py
    └── 📜 Preço_teto_-_FIIs de tijolo.py
├── 📜 requirements.txt # Dependências do projeto
├── 📜 config.py        # Formatação de moedas e porcentagem  

Como Contribuir
Faça um fork do projeto.
Crie uma nova branch para sua funcionalidade: git checkout -b feature/nome-da-funcionalidade.
Realize as alterações e faça commit: git commit -m 'Adiciona nova funcionalidade X'.
Envie suas alterações: git push origin feature/nome-da-funcionalidade.
Abra um pull request explicando suas contribuições.
