# usipipo-telegram-bot

> Bot de Telegram para interacción con usuarios del ecosistema uSipipo

## Estado

- [ ] En desarrollo
- [ ] Alpha
- [ ] Beta
- [x] Producción

## Versión

**v0.2.0** - VPN Key Management (En desarrollo)

**v0.1.0** - Invisible Authentication (Estable)

## Documentación

- [CHANGELOG](CHANGELOG.md)
- [Integration Tests](INTEGRATION-TEST-SUMMARY.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Commands](docs/COMMANDS.md)
- [Deployment](docs/DEPLOYMENT.md)

## Desarrollo

```bash
# Clonar
git clone https://github.com/uSipipo-Team/usipipo-telegram-bot.git
cd usipipo-telegram-bot

# Instalar dependencias
uv sync --dev

# Configurar entorno
cp example.env .env

# Ejecutar tests
uv run pytest

# Ejecutar bot
uv run python -m src
```

## Docker

```bash
# Build
docker build -t usipipo-telegram-bot .

# Ejecutar
docker run --env-file .env usipipo-telegram-bot
```

## License

MIT © uSipipo
