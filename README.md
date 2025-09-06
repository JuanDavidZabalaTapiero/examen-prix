# Cambios en la BD

Si no está la carpeta migrations/ (iniciar por primera vez):
```bash
flask db init
```

Si hay cambios en los modelos:
```bash
flask db migrate -m "mensaje describiendo el cambio"
```

Actualizar la BD
```bash
flask db upgrade
```