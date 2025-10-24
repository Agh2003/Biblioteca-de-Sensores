#!/bin/bash

# Script para gerar a documentação da Biblioteca de Sensores
# Uso: ./build_docs.sh

echo "🔧 Configurando ambiente para documentação..."

# Verificar se estamos no diretório correto
if [ ! -f "docs/source/conf.py" ]; then
    echo "❌ Erro: Execute este script no diretório raiz da Biblioteca de Sensores"
    exit 1
fi

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual e instalar dependências
echo "📥 Instalando dependências..."
source venv/bin/activate
pip install -q sphinx sphinx-rtd-theme

# Gerar documentação
echo "📚 Gerando documentação HTML..."
sphinx-build -b html docs/source docs/build

if [ $? -eq 0 ]; then
    echo "✅ Documentação gerada com sucesso!"
    echo "📖 Abra docs/build/index.html no seu navegador para visualizar"
    echo ""
    echo "📁 Arquivos gerados em: docs/build/"
    echo "🌐 Para servir localmente: cd docs/build && python3 -m http.server 8000"
else
    echo "❌ Erro ao gerar documentação"
    exit 1
fi
