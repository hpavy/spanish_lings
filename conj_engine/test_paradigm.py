from conj_engine.verbs_registry import BY_INFINITIVE
from conj_engine.paradigm import conjugate, gerund, past_participle

EXPECTED = {
    ("hablar", "present_indicative"): ["hablo", "hablas", "habla", "hablamos", "habláis", "hablan"],
    ("hablar", "preterite"): ["hablé", "hablaste", "habló", "hablamos", "hablasteis", "hablaron"],
    ("querer", "present_indicative"): ["quiero", "quieres", "quiere", "queremos", "queréis", "quieren"],
    ("querer", "preterite"): ["quise", "quisiste", "quiso", "quisimos", "quisisteis", "quisieron"],
    ("sentir", "present_indicative"): ["siento", "sientes", "siente", "sentimos", "sentís", "sienten"],
    ("sentir", "preterite"): ["sentí", "sentiste", "sintió", "sentimos", "sentisteis", "sintieron"],
    ("sentir", "present_subjunctive"): ["sienta", "sientas", "sienta", "sintamos", "sintáis", "sientan"],
    ("dormir", "present_indicative"): ["duermo", "duermes", "duerme", "dormimos", "dormís", "duermen"],
    ("dormir", "preterite"): ["dormí", "dormiste", "durmió", "dormimos", "dormisteis", "durmieron"],
    ("pedir", "present_indicative"): ["pido", "pides", "pide", "pedimos", "pedís", "piden"],
    ("pedir", "preterite"): ["pedí", "pediste", "pidió", "pedimos", "pedisteis", "pidieron"],
    ("jugar", "present_indicative"): ["juego", "juegas", "juega", "jugamos", "jugáis", "juegan"],
    ("buscar", "present_subjunctive"): ["busque", "busques", "busque", "busquemos", "busquéis", "busquen"],
    ("buscar", "preterite"): ["busqué", "buscaste", "buscó", "buscamos", "buscasteis", "buscaron"],
    ("llegar", "present_subjunctive"): ["llegue", "llegues", "llegue", "lleguemos", "lleguéis", "lleguen"],
    ("empezar", "present_indicative"): ["empiezo", "empiezas", "empieza", "empezamos", "empezáis", "empiezan"],
    ("empezar", "present_subjunctive"): ["empiece", "empieces", "empiece", "empecemos", "empecéis", "empiecen"],
    ("empezar", "preterite"): ["empecé", "empezaste", "empezó", "empezamos", "empezasteis", "empezaron"],
    ("conocer", "present_indicative"): ["conozco", "conoces", "conoce", "conocemos", "conocéis", "conocen"],
    ("seguir", "present_indicative"): ["sigo", "sigues", "sigue", "seguimos", "seguís", "siguen"],
    ("seguir", "present_subjunctive"): ["siga", "sigas", "siga", "sigamos", "sigáis", "sigan"],
    ("seguir", "preterite"): ["seguí", "seguiste", "siguió", "seguimos", "seguisteis", "siguieron"],
    ("coger", "present_indicative"): ["cojo", "coges", "coge", "cogemos", "cogéis", "cogen"],
    ("elegir", "present_indicative"): ["elijo", "eliges", "elige", "elegimos", "elegís", "eligen"],
    ("elegir", "present_subjunctive"): ["elija", "elijas", "elija", "elijamos", "elijáis", "elijan"],
    ("construir", "present_indicative"): ["construyo", "construyes", "construye", "construimos", "construís", "construyen"],
    ("construir", "preterite"): ["construí", "construiste", "construyó", "construimos", "construisteis", "construyeron"],
    ("construir", "present_subjunctive"): ["construya", "construyas", "construya", "construyamos", "construyáis", "construyan"],
    ("ser", "present_indicative"): ["soy", "eres", "es", "somos", "sois", "son"],
    ("ir", "present_indicative"): ["voy", "vas", "va", "vamos", "vais", "van"],
    ("tener", "future"): ["tendré", "tendrás", "tendrá", "tendremos", "tendréis", "tendrán"],
    ("decir", "conditional"): ["diría", "dirías", "diría", "diríamos", "diríais", "dirían"],
    ("hacer", "present_subjunctive"): ["haga", "hagas", "haga", "hagamos", "hagáis", "hagan"],
    ("tener", "imperfect_subjunctive_ra"): ["tuviera", "tuvieras", "tuviera", "tuviéramos", "tuvierais", "tuvieran"],
}

PERSONS = ["yo", "tu", "el", "nosotros", "vosotros", "ellos"]


def run():
    failures = []
    for (infinitive, tense), expected in EXPECTED.items():
        entry = BY_INFINITIVE[infinitive]
        result = conjugate(entry, tense)
        actual = [result[p] for p in PERSONS]
        if actual != expected:
            failures.append((infinitive, tense, expected, actual))

    gerund_checks = [
        ("dormir", "durmiendo"), ("pedir", "pidiendo"), ("construir", "construyendo"),
        ("ir", "yendo"), ("decir", "diciendo"), ("seguir", "siguiendo"),
    ]
    for infinitive, expected in gerund_checks:
        entry = BY_INFINITIVE[infinitive]
        actual = gerund(entry)
        if actual != expected:
            failures.append((infinitive, "gerund", expected, actual))

    participle_checks = [
        ("hablar", "hablado"), ("vivir", "vivido"), ("hacer", "hecho"),
        ("escribir", "escrito"), ("romper", "roto"), ("resolver", "resuelto"),
        ("ver", "visto"), ("construir", "construido"),
    ]
    for infinitive, expected in participle_checks:
        entry = BY_INFINITIVE[infinitive]
        actual = past_participle(entry)
        if actual != expected:
            failures.append((infinitive, "past_participle", expected, actual))

    if failures:
        print(f"{len(failures)} FAILURES:")
        for infinitive, tense, expected, actual in failures:
            print(f"  {infinitive}/{tense}: expected {expected}, got {actual}")
    else:
        print(f"all {len(EXPECTED) + len(gerund_checks) + len(participle_checks)} checks passed")


if __name__ == "__main__":
    run()
