# Libro de gramática — conjugación española

Manual de referencia para las reglas de conjugación, organizado en el mismo
orden que las 17 unidades (*tiers*) del programa de ejercicios. Cada capítulo
explica la regla y muestra ejemplos generados directamente por el motor de
conjugación (`conj_engine/`) — así que nunca hay desincronización entre lo
que lees aquí y lo que te pregunta la aplicación.

## Capítulos

01. [Presente de indicativo — verbos regulares](01_presente_regular.md)
02. [Presente de indicativo — verbos con cambio de raíz](02_presente_cambio_raiz.md)
03. [Presente de indicativo — cambios ortográficos](03_presente_ortografico.md)
04. [Presente de indicativo — verbos irregulares](04_presente_irregular.md)
05. [Pretérito — verbos regulares](05_preterito_regular.md)
06. [Pretérito — cambios ortográficos y de raíz](06_preterito_ortografico_raiz.md)
07. [Pretérito — verbos irregulares](07_preterito_irregular.md)
08. [Imperfecto de indicativo](08_imperfecto.md)
09. [Futuro y condicional](09_futuro_condicional.md)
10. [Gerundio y participio pasado](10_gerundio_participio.md)
11. [Pretérito perfecto compuesto](11_preterito_perfecto.md)
12. [Pluscuamperfecto, futuro perfecto, condicional perfecto](12_tiempos_compuestos.md)
13. [Presente de subjuntivo](13_subjuntivo_presente.md)
14. [Imperfecto de subjuntivo (-ra / -se)](14_subjuntivo_imperfecto.md)
15. [Subjuntivo compuesto](15_subjuntivo_compuesto.md)
16. [Imperativo](16_imperativo.md)
17. [Verbos reflexivos](17_reflexivos.md)

## Cómo usar este libro

- Lee el capítulo antes de empezar la unidad correspondiente en `python3 cli.py`.
- Vuelve aquí cuando falles un ítem repetidamente — normalmente la regla
  explica por qué.
- Las tablas de ejemplo están generadas con `book/generate_tables.py`, que
  llama directamente al motor de conjugación. Si quieres ver la conjugación
  completa de cualquier verbo del registro, ejecuta:
  ```
  python3 book/generate_tables.py <infinitivo> <tiempo>
  ```
