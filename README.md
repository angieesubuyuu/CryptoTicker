Parar conectar MySQL con el proyecto:

```bash
docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=Admin2025 -e MYSQL_DATABASE=crypto_umg_db -p 3306:3306 -d mysql:8
```


Correr proyecto:

1. Abrir Docker (Ballena azul)
2. Selecionar 'Containers' del panel izquierdo
3. Click en |> play para encender la db
4. Correr el proyecto:

```bash
source venv/bin/activate && python3 -m lib.presentation.order_ui
```

Para acceder a la db:

1. Abrir terminal
2. Correr comando:

```bash
docker exec -it my-mysql mysql -u root -p
```

3. Ingresar contrasena (Es normal que no se vea que escribes ningun caracter. Solo escribe la contrasena y luego enter)

```bash
Enter password: Admin2025
```

4. Si ingresaste correctamente la contrasena te debe aparecer esto:

```bash
mysql>
```

5. Eliminar todos los datos:

```sql
DELETE from orders;
```


# Como funciona el proyecto

lib/
// Carpeta principal
- core/
    // En entidades se definen las clases del sistema
    - entities/
    // En use_cases se definen las operaciones del sistema
    - use_cases/
    // En interfaces se definen las interfaces del sistema
    - interfaces/
// En infrastructure se definen las implementaciones de las interfaces
- infrastructure/
    // En repositories se definen las implementaciones de las interfaces
    - repositories/
    // En services se definen las implementaciones de las interfaces
    - services/
// En presentation se definen las interfaces de usuario
- presentation/
    - order_ui.py