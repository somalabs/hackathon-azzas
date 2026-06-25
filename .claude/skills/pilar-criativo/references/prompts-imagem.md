# Biblioteca de Prompts de Imagem — Estilo (Workshop SomaLabs / Farm)

> Prompts em inglês (funcionam melhor nos modelos). Substitua `[garment]`, `[cor]`, `[tecido]`,
> `[forma]`, `[categoria]`, `[detalhe]`, `[textura]` pelo valor desejado. `@IMG1`/`@IMG2` (ou
> `image 1`/`image 2`) referenciam as imagens de entrada na ordem do prompt.

## Estrutura
`[VERBO] + [O QUÊ] + de @IMG1 + em @IMG2` · rode **4 variações** · 1K de resolução na maioria.
Aspect ratio: **3:4** produto · **9:16** look · **2:3** vistas · **1:1** detalhe.

## Modelos
- **Nano Banana** — remix, blend, variações, inserção, style (principal).
- **Flux Kontext Pro** — sketches técnicos, vistas, close-ups.
- **GPT Image High** — tecidos manuais, bordados, display.

---

## (1) EXPLORE — do real ao desenho / remix / blend

| Objetivo | Prompt | Modelo |
|---|---|---|
| Sketch técnico | `Convert to a technical vector sketch. Black and White.` | GPT High |
| Sketch com sombra/cor | `Convert to a technical vector sketch with soft shadows, colored` | GPT High / Flux |
| Flat product (sketch) | `convert to a flat product in technical vector sketch. Black and White` | Nano Banana |
| Ficha técnica / fitting board | `Extract the garment to a flat product and transform it into a stylized fitting board. Generate three consistent views of the same garment: full front, profile side, and back view. Overlay: hand-drawn scribble annotations in red marker with arrows to details (seams, sleeves, collar, hem, vents, fabric texture, length). Sticky notes, tape, paper collage in blue/yellow/pink, placed casually. Handwriting rough and spontaneous, not digital. Clean white background.` | — |
| Remix p/ outra peça | `Inspired by this [garment] change to a [categoria] based on the shape of @img2. White background` | Nano Banana |
| Remix múltiplas peças | `Inspired by this [garment] change to [peça A], [peça B], [peça C]. White background. No model` | Nano Banana |

## (2) EXTRACT — peça → still, vistas, detalhes

| Objetivo | Prompt | Modelo |
|---|---|---|
| E-commerce/piloto → still | `Extract the garment to a flat product, neutral background.` | Nano Banana |
| Extrair estampa | `Extract the print from this image, generating a closeup allover print image` | Nano Banana |
| Vista de costas | `Generate the back view of the [garment].` | Flux Kontext Pro |
| Vista lateral | `Generate the side view of the [garment].` | Flux Kontext Pro |
| Close de detalhe | `Generate a close up of the [detalhe]` | Flux Kontext Pro |
| Detalhes ampliados | `Generate an enlarged image of the collar, hem, and cuff detail on a single page.` | Flux Kontext Pro |

## (3) VARIATIONS — cor, forma, material

| Objetivo | Prompt | Modelo |
|---|---|---|
| Variação de cor | `Turn the colors of the [garment] into [cor].` / `Change the color of the [garment] to new combination of pastel colors` | Nano Banana |
| Cor de uma referência | `Insert the color of img2 into the [garment] from img1. Keep print color.` | Nano Banana |
| Coleção em paleta Pantone | `Develop a collection of garment img1 into each pantone color of img2` | Nano Banana |
| Variação de forma | `Change to [forma].` (ex.: balloon sleeves, halter neck, mini) | Nano Banana |
| Variação de material | `Change the materials into [tecido].` (ex.: chiffon, waffle cotton, broderie anglaise) | Nano Banana |
| Material híbrido | `Change the [garment] into a crochet-macramé hybrid piece.` | Nano Banana |

**Biblioteca de shapes** — Mangas: balloon sleeve, cold shoulder, exaggerated shoulder, ruffled,
bell, tulip, halter neck, one shoulder. Silhueta: mini, midi dress, A-line, bodycon, balloon
dress, corset dress, cut out. Combinar dois: `Change to long sleeve and balloon sleeve`.

## (4) INSERT + STYLE — inserir tecido/detalhe/estampa, transferir estilo, peça na modelo

| Objetivo | Prompt | Modelo |
|---|---|---|
| Inserir material | `Insert the material from img1 into the whole garment of image2` / `Apply the material of the garment in img2 to the garment in img1` | Nano Banana |
| Inserir detalhe | `Insert the details of image 2 into the product of image 1. White background.` | Nano Banana |
| Inserir detalhe específico | `Insert the details of collar in image 2 into the collar of image 1. White background.` | Nano Banana |
| Inserir estampa posicional | `Insert the positional print of IMG2 as a placement print of the exact garment of IMG1. Keep the natural flow and effect of fabric and print. White background.` | Nano Banana |
| Transferir estilo | `Transfer the style of image 2 to the [garment] of image 1. White background.` | Nano Banana |
| Reinterpretar (editorial) | `Reinterpret the style of the image in an editorial fashion photo of a female model wearing [peça].` | Nano Banana |
| Produto na modelo | `Insert the garments of IMG1 into the model of IMG2.` (variações: `Maintain the pants` / `Change the shoes to yellow jelly sandal`) | Nano Banana |
