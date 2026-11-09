# moffee Themes

moffee offers five themes to enhance your presentations. Choose the one that best fits your content and style:

| Theme | Description | Preview |
|-------|-------------|---------|
| default | Clean, versatile look for general use | <img src="https://raw.githubusercontent.com/BMPixel/moffee/main/docs/images/default.png" alt="default theme" width="200"/> |
| beam | Professional theme inspired by LaTeX Beamer | <img src="https://raw.githubusercontent.com/BMPixel/moffee/main/docs/images/beam.png" alt="beam theme" width="200"/> |
| robo | Simple and modern design | <img src="https://raw.githubusercontent.com/BMPixel/moffee/main/docs/images/robo.png" alt="robo theme" width="200"/> |
| blue | Dark blue background for elegance | <img src="https://raw.githubusercontent.com/BMPixel/moffee/main/docs/images/blue.png" alt="blue theme" width="200"/> |
| gaia | Paper and handwriting style for creativity | <img src="https://raw.githubusercontent.com/BMPixel/moffee/main/docs/images/gaia.png" alt="gaia theme" width="200"/> |

To use a theme, specify it in your markdown file's front matter:

```yaml
---
theme: theme_name
---
```

Replace `theme_name` with your chosen theme (default, beam, robo, blue, or gaia).

The default font stack uses Inter if installed, then the viewing system's UI
font. The browser also selects system fallback fonts for characters missing
from the chosen font, including CJK text. This does not download or bundle
fonts; the available fonts depend on the viewing system. Individual themes can
use their own fonts.
