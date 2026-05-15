# PROJECT MEMORY - what'shappeing

## Visão Geral do Projeto

Sistema desktop local para controle de atividades em fila, focado em medição precisa de tempos de execução e espera por terceiros.

## Regras de Negócio

- Atividades começam em "Aberta" e nunca pausam tempo total
- Tempo total conta desde criação até finalização/cancelamento
- Tempo aguardando terceiros é separado e cumulativo
- Histórico completo de mudanças de status
- Finalização/cancelamento requer dados específicos

## Estrutura do Projeto

- `app/`: Código fonte modular (main, db, models, repository, services, ui, utils)
- `docs/`: Documentação técnica
- `installer/`: Configurações de empacotamento
- `scripts/`: Automação de build
- Pipeline Jenkins para CI/CD

## Decisões Atuais

- Python 3.12+ com CustomTkinter para UI moderna
- SQLite para persistência local
- PyInstaller para executável
- Inno Setup para instalador
- Estrutura enxuta sem over-engineering

## Estado Atual do Desenvolvimento

- Estrutura de pastas criada
- Documentação completa
- Código fonte implementado e testado:
  - Models: Atividade, HistoricoStatus, PeriodosTerceiros
  - DB: SQLite com criação automática de tabelas
  - Repository: CRUD completo
  - Services: Lógica de negócio e cálculos de tempo
  - UI: Interface completa com CustomTkinter
  - Utils: Funções auxiliares
- Scripts de build testados (executável gerado)
- Pipeline Jenkins configurada
- Instalador Inno Setup pronto (requer Inno Setup instalado)

## Próximos Passos

1. Instalar Inno Setup para gerar instalador
2. Configurar Jenkins com agente Windows
3. Executar pipeline completa
4. Testar instalador final
5. Publicar no GitHub