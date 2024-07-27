import numpy as np

# Caminho do arquivo de embedding
embedding_file_path = 'C:/Users/HeannarReis/Documents/bsa_atacadao/myenv/data/dados.npy'

# Carregar o embedding
embedding = np.load(embedding_file_path)

# Exibir o conteúdo do embedding
print("Embedding carregado:")
print(embedding)
print("Dimensões do embedding:", embedding.shape)