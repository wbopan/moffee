# Configuration

## Front Matter Options

moffee's behavior can be customized using front matter at the beginning of your document. Here's a comprehensive table of available options:

| Option | Description | Default Value | Available Options |
|--------|-------------|---------------|-------------------|
| [theme](theme.md) | Visual theme for the presentation | default | default, beam, robo, blue, gaia |
| layout | HTML template for slide layout | content | content, centered |
| lang | Document language (front matter only) | en | BCP 47 language tag, e.g. zh-Hans, ja, ko |
| resource_dir | Base directory for relative URLs | . (current directory) | Any valid directory path |
| default_h1 | Inherit H1 from previous slides if not defined | false | true, false |
| default_h2 | Inherit H2 from previous slides if not defined | true | true, false |
| default_h3 | Inherit H3 from previous slides if not defined | true | true, false |
| aspect_ratio | Aspect ratio of the slides | "16:9" | "16:9", "4:3" |
| slide_width | Width of the slides | 720 | Any number |
| slide_height | Height of the slides | 405 | Any number |

### Default Front Matter

```yaml
---
theme: default
lang: en
layout: content
resource_dir: "."
default_h1: false
default_h2: true
default_h3: true
aspect_ratio: "16:9"
slide_width: 720
slide_height: 405
---
```

## Custom CSS Properties

You can set any CSS property in the front matter to apply it globally to all slides. For example:

```yaml
---
layout: content
background-color: darkgray
color: white
---
```

## Local Style Decorators

moffee supports local style decorators for individual slides using the syntax `@(property=value)`. These can be used within the document to set attributes for specific slides.

### Example:

```markdown
# A refined landing page
Our journey begins here
@(layout=content, background-image='url("https://placehold.co/600x400")')
```
