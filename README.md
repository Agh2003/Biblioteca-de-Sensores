# Biblioteca de Sensores

Uma biblioteca Python completa para controle de sensores e dispositivos eletrônicos, especialmente projetada para projetos de robótica e automação.

##  Gerando a Documentação

A biblioteca inclui documentação completa gerada com Sphinx. Para visualizá-la, siga estes passos:

### Script Automático

```bash
# Torne o script executável (apenas na primeira vez)
chmod +x build_docs.sh

# Execute o script para gerar a documentação
./build_docs.sh
```

### Visualizando a Documentação

Após gerar a documentação, você pode visualizá-la desta forma:

```bash
cd docs/build
python3 -m http.server 8000
```
Depois acesse: **http://localhost:8000**
