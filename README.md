# what'shappeing

Sistema desktop local para controle de atividades em fila, medindo tempos de execução e espera.

## Visão Geral

Aplicação desktop Windows para gerenciar atividades com controle preciso de tempos, incluindo tempo total, tempo aguardando terceiros e tempo operacional interno.

## Funcionalidades

- Criar, editar e gerenciar atividades
- Controle de status: Aberta, Em andamento, Aguardando terceiros, Finalizada, Cancelada
- Histórico de mudanças de status
- Cálculo automático de tempos
- Relatórios simples
- Interface limpa e profissional

## Estrutura do Projeto

```
whatshappeing/
├── app/                 # Código fonte
├── docs/                # Documentação
├── installer/           # Configurações de instalação
├── scripts/             # Scripts de build
├── Jenkinsfile          # Pipeline CI/CD
├── requirements.txt     # Dependências Python
├── README.md            # Este arquivo
├── .gitignore           # Arquivos ignorados
└── run.py               # Ponto de entrada
```

## Como Rodar Localmente

1. Instale Python 3.12+
2. Clone o repositório
3. Instale dependências: `pip install -r requirements.txt`
4. Execute: `python run.py`

## Como Gerar Executável

1. Execute o script: `powershell scripts/build_exe.ps1`
2. O executável será gerado em `dist/whatshappeing.exe`

## Como Gerar Instalador

1. Instale Inno Setup 6
2. Execute: `powershell scripts/build_installer.ps1`
3. O instalador será gerado como `installer/whatshappeingSetup-1.0.0.exe`

## Pipeline Jenkins

### Preparar Agente Windows

1. Instale Jenkins
2. Configure agente Windows com:
   - Python 3.12+
   - Inno Setup 6 em `C:\Program Files (x86)\Inno Setup 6\ISCC.exe`
   - Git

### Executar Pipeline

1. Crie um job pipeline no Jenkins
2. Configure SCM para este repositório
3. Execute o build
4. Baixe o artefato `whatshappeingSetup-1.0.0.exe`

## Troubleshooting

- **Erro de dependências**: Execute `pip install --upgrade pip` e reinstale
- **PyInstaller falha**: Limpe `build/` e `dist/` e tente novamente
- **Inno Setup não encontrado**: Verifique o caminho em `build_installer.ps1`
- **Tempos incorretos**: Verifique se o banco SQLite não foi corrompido

## Publicar no GitHub

1. Crie repositório no GitHub
2. Push do código
3. Configure webhook para Jenkins (opcional)