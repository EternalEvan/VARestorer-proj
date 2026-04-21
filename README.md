# VARestorer-project

Project page for **VARestorer: One-Step VAR Distillation for Real-World Image Super-Resolution** (ICLR 2026).

- Paper: [OpenReview](https://openreview.net/pdf?id=T2Oihh7zN8)
- Code:  [EternalEvan/VARestorer](https://github.com/EternalEvan/VARestorer)
- Model: [HuggingFace](https://huggingface.co/EternalEvan/VARestorer)

## Local preview

Open `index.html` directly in a browser, or serve the folder:

```bash
python3 -m http.server 8000
# then visit http://localhost:8000
```

## Layout

```
VARestorer-proj/
├── index.html            # main project page
└── static/
    ├── css/              # Bulma + FontAwesome + custom styles
    ├── js/               # Bulma carousel/slider + site js
    └── images/           # figures rendered from the paper + logo/pipeline
```

## Credit

Page template adapted from the [Nerfies](https://nerfies.github.io) project page.
