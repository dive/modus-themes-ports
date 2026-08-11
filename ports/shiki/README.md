# Shiki Modus Themes

Standalone TextMate themes for [Shiki](https://shiki.style/), generated from
the Modus palette snapshots in this repository.

## Use

Shiki themes are source artifacts rather than files installed into a global
configuration directory. Load one of the JSON files as a custom theme:

```js
import { createHighlighter } from "shiki"
import modusVivendi from "./modus-vivendi.json" with { type: "json" }

const highlighter = await createHighlighter({
  langs: ["javascript"],
  themes: [modusVivendi],
})
```

The generated files are intended to be registered with
[`textmate-grammars-themes`](https://github.com/shikijs/textmate-grammars-themes)
and distributed by `tm-themes` and `@shikijs/themes`.

## Maintain

Render and validate the source themes with:

```sh
python3 scripts/modus.py render --tool shiki
python3 scripts/modus.py validate --tool shiki
```

`python3 scripts/modus.py sync-upstream` updates the palette snapshots and
regenerates these files together with the other ports.
