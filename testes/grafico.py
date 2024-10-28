import matplotlib.pyplot as plt

# Dados para o gráfico
categorias = ['Categoria A', 'Categoria B', 'Categoria C']
valores = [10, 20, 15]

# Criar o gráfico de barras
plt.bar(categorias, valores, color=['red', 'green', 'blue'])
plt.title('Gráfico de Barras de Teste')  # Título do gráfico
plt.xlabel('Categorias')  # Rótulo do eixo X
plt.ylabel('Valores')  # Rótulo do eixo Y

# Exibir o gráfico
plt.show()
