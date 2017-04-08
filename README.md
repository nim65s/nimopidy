# NiMoPiDy

## Quick deploy with docker:

```bash
docker build -t nimopidy .
docker run -p 8000:8000 --name nimopidy -t nimopidy python manage.py runserver 0.0.0.0:8000
```
