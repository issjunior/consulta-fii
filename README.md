<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Consulta para Investimentos</title>
</head>
<body>
    <h1>Sistema de Consulta para Investimentos</h1>
    <p>
        Este projeto é um sistema de consulta voltado para investidores que desejam monitorar indicadores econômicos, 
        acompanhar ativos e estimar o preço teto de Fundos Imobiliários (FIIs) utilizando o modelo de Gordon. 
        A aplicação foi desenvolvida com <strong>Streamlit</strong> para interface frontend e utiliza a biblioteca 
        <strong>python-bcb</strong> para recuperar dados financeiros atualizados como <strong>IPCA</strong>, <strong>CDI</strong> e <strong>SELIC</strong>.
    </p>

    <h2>Funcionalidades</h2>
    <h3>📊 Indicadores Econômicos</h3>
    <ul>
        <li>Consulta automática de indicadores como <strong>IPCA</strong>, <strong>CDI</strong> e <strong>SELIC</strong>, diretamente da base do Banco Central utilizando a biblioteca <code>python-bcb</code>.</li>
        <li>Exibição clara e organizada dos dados econômicos para auxiliar na tomada de decisão.</li>
    </ul>

    <h3>📈 Acompanhamento de Ativos</h3>
    <ul>
        <li>Monitoramento de Fundos Imobiliários (FIIs) e outros ativos financeiros.</li>
        <li>Integração simples para acompanhar as variações de preços e rendimento.</li>
    </ul>

    <h3>💡 Estimativa de Preço Teto</h3>
    <p>Implementação do <em>Modelo de Gordon</em> para calcular o preço teto de FIIs, baseado em:</p>
    <ul>
        <li>Dividendos esperados</li>
        <li>Taxa de crescimento</li>
        <li>Taxa de desconto</li>
    </ul>

    <h3>🖥️ Interface Intuitiva</h3>
    <ul>
        <li>Desenvolvido com <strong>Streamlit</strong>, oferecendo uma interface fácil de usar, interativa e responsiva.</li>
        <li>Possibilidade de entrada de dados personalizada para os usuários, como o ticker do ativo (ex.: <code>HGLG11.SA</code>).</li>
    </ul>

    <h2>Tecnologias Utilizadas</h2>
    <ul>
        <li><strong>Streamlit:</strong> Interface frontend para exibição e interação com o usuário.</li>
        <li><strong>Python:</strong> Lógica principal e cálculos.</li>
        <li><strong>python-bcb:</strong> Recuperação de dados financeiros do Banco Central do Brasil.</li>
        <li><strong>Modelo de Gordon:</strong> Fórmula aplicada para estimar o preço teto de FIIs.</li>
    </ul>

    <h2>Como Executar o Projeto</h2>
    <h3>Clone o Repositório:</h3>
    <pre>
git clone https://github.com/issjunior/consulta-fii.git
cd sistema-consulta-investimentos
    </pre>

    <h3>Crie um Ambiente Virtual e Ative-o:</h3>
    <pre>
python -m venv venv
source venv/bin/activate  # Para Linux/MacOS
venv\Scripts\activate     # Para Windows
    </pre>

    <h3>Instale as Dependências:</h3>
    <pre>pip install -r requirements.txt</pre>

    <h3>Execute a Aplicação:</h3>
    <pre>streamlit run Home.py</pre>

    <h3>Acesse no Navegador:</h3>
    <p>O Streamlit abrirá automaticamente no navegador ou estará disponível em <a href="http://localhost:8501" target="_blank">http://localhost:8501</a>.</p>

    <h2>Estrutura do Projeto</h2>
    <pre>
📂 sistema-consulta-investimentos
├── 📂 img              # Imagens
├── 📂 modulos          # Módulos python
├── 📂 pages            # Organização de links para funções
    └── 📜 Calculadora.py
    └── 📜 De_olho.py
    └── 📜 Índices_e_Títulos.py
    └── 📜 Preço teto_-_FIIs_de_Papel.py
    └── 📜 Preço_teto_-_FIIs de tijolo.py
├── 📜 Home.py          # Página inicial
├── 📜 requirements.txt # Dependências do projeto
├── 📜 config.py        # Formatação de moedas e porcentagem  
    </pre>

    <h2>Como Contribuir</h2>
    <ol>
        <li>Faça um fork do projeto.</li>
        <li>Crie uma nova branch para sua funcionalidade:
            <pre>git checkout -b feature/nome-da-funcionalidade</pre>
        </li>
        <li>Realize as alterações e faça commit:
            <pre>git commit -m 'Adiciona nova funcionalidade X'</pre>
        </li>
        <li>Envie suas alterações:
            <pre>git push origin feature/nome-da-funcionalidade</pre>
        </li>
        <li>Abra um pull request explicando suas contribuições.</li>
    </ol>
</body>
</html>
