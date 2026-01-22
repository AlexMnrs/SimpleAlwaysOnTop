# 📌 SimpleAlwaysOnTop

**Tu control total sobre las ventanas de Windows: fija lo importante, ignora el resto.**

SimpleAlwaysOnTop es una aplicación de escritorio moderna y elegante diseñada para darte el superpoder de mantener cualquier ventana siempre visible ("Always on Top") en tu sistema Windows. Olvídate de scripts complejos o herramientas obsoletas; con una interfaz visual intuitiva y un diseño oscuro profesional, puedes gestionar tu productividad sin interrupciones.

Ideal para:
- 👨‍💻 **Programadores**: Mantén tu documentación o terminal visible mientras codificas.
- 📺 **Streaming**: Fija tu chat o monitor de OBS sobre tu juego o aplicación.
- 📊 **Multitasking**: Ten siempre a la vista videos, calculadoras o notas mientras trabajas en otras ventanas.

---

## ✨ Características

- 🎨 **Interfaz Moderna**: Diseño limpio y atractivo con modo oscuro nativo gracias a CustomTkinter.
- 🚀 **Detección Automática**: Lista todas tus ventanas visibles al instante.
- 🔘 **Switch On/Off**: Activa o desactiva el modo "Siempre Visible" con un solo clic.
- 🔍 **Filtrado Inteligente**: Muestra solo las ventanas relevantes, ignorando procesos en segundo plano.
- 🛡️ **No Intrusivo**: Ligero y rápido, sin instalaciones complejas ni anuncios.

## 🛠️ Requisitos

- **Sistema Operativo**: Windows 10 / 11
- **Lenguaje**: Python 3.8+
- **Dependencias**: `customtkinter`, `pywin32`, `pillow`

## 📥 Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/AlexMnrs/SimpleAlwaysOnTop.git
   ```
2. **Navega al directorio**:
   ```bash
   cd SimpleAlwaysOnTop
   ```
3. **Instala dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Uso

1. **Ejecuta la aplicación**:
   ```bash
   python app.py
   ```

2. **Gestiona tus ventanas**:
   - Pulsa el botón **"Refrescar Lista"** si has abierto nuevas ventanas.
   - Busca la ventana que deseas en la lista.
   - Activa el **interruptor (Switch)** a la derecha para fijarla.
   - Desactívalo para devolverla a la normalidad.

### ⚡ Atajos de Teclado (Hotkeys)

- **`Ctrl + Space`**: Fija/Desfija la ventana que tengas activa en ese momento.
- **`Ctrl + Shift + U`**: **EMERGENCIA**. Desfija TODAS las ventanas del sistema. Útil si has fijado algo encima de todo y no puedes ver nada.

### 📝 Ejemplo de Salida

Al iniciar, verás una ventana oscura con el título **"Gestor de Ventanas"** y una lista desplazable similar a:

```text
[ Bloc de notas               ]  ( O ) Fijar
[ Google Chrome               ]  (   ) Fijar
[ Calculadora                 ]  ( O ) Fijar
```

## ⚠️ Notas Importantes

- **Permisos**: En algunos casos, si intentas fijar una ventana de administrador sin ejecutar el script como administrador, podría no funcionar (limitación de Windows).
- **Persistencia**: El estado "Always on Top" se pierde si cierras la ventana objetivo completamente.

## 👨💻 Autor

**Alex Monrás**
*Desarrollador de Software & Entusiasta de la Automatización*

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---
© 2026 Alex Monrás.