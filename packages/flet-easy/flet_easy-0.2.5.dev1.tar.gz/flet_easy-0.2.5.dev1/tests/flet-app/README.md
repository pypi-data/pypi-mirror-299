# Publishing Flet app to multiple platforms

## Installation requirements

> [!NOTE]
   For local testing or web use

* flet
* flet-easy
* peewee

## Packaging app for Android

Route where it should be located in the project: `./flet-app`

```bash
cd flet
```

### APK

```bash
flet build apk -vv
```

### WINDOWS

```bash
flet build windows -vv
```

### WEB

> [!NOTE]
> If there are problems in `build web`, use:
>
> ```python
> import flet as ft   
> ft.app(app.run(fastapi=True))
>  ```

```bash
flet run main.py -w -d -r
```

## 🎬 **Demo apk**

![app example](https://github.com/Jviduz/flet-easy/blob/main/media/apk-demo-fs.mp4?raw=true "app example")
