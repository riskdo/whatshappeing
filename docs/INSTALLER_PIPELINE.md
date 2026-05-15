# INSTALLER PIPELINE - what'shappeing

## Fluxo GitHub → Jenkins → PyInstaller → Inno Setup → Instalador

1. **GitHub**: Código fonte versionado
2. **Jenkins**: Pipeline automatizada
   - Checkout do código
   - Setup Python e dependências
   - Build do executável com PyInstaller
   - Build do instalador com Inno Setup
   - Arquivamento do artefato final

## Ferramentas Necessárias no Agente Jenkins

- **Python 3.12+**: Ambiente de execução
- **Git**: Para checkout do código
- **Inno Setup 6**: Compilador de instaladores
  - Instalado em `C:\Program Files (x86)\Inno Setup 6\ISCC.exe`
- **PowerShell**: Para execução de scripts

## Configuração do Job Jenkins

- **Tipo**: Pipeline
- **SCM**: Git (URL do repositório)
- **Script Path**: `Jenkinsfile`
- **Agente**: Windows com label 'windows'

## Problemas Comuns

- **Python não encontrado**: Verificar PATH do sistema
- **Inno Setup falha**: Confirmar instalação e caminho
- **Dependências faltando**: Pipeline instala automaticamente
- **Artefato não gerado**: Verificar logs de build
- **Permissões**: Agente deve ter acesso a pastas de build