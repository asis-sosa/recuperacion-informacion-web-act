class EvaluadorIRS:
    @staticmethod
    def precision(recuperados, relevantes):
        recuperados = set(recuperados)
        relevantes = set(relevantes)
        tp = len(recuperados & relevantes)
        return tp / len(recuperados) if recuperados else 0

    @staticmethod
    def recall(recuperados, relevantes):
        recuperados = set(recuperados)
        relevantes = set(relevantes)
        tp = len(recuperados & relevantes)
        return tp / len(relevantes) if relevantes else 0

    @staticmethod
    def f1(precision, recall):
        if precision + recall == 0:
            return 0

        return 2 * precision * recall / (precision + recall)

    @staticmethod
    def precision_at_k(ranking, relevantes, k):
        top_k = set(ranking[:k])
        relevantes = set(relevantes)

        return len(top_k & relevantes) / k

    @staticmethod
    def average_precision(ranking, relevantes):
        relevantes = set(relevantes)
        suma = 0
        encontrados = 0

        for i, doc in enumerate(ranking, 1):
            if doc in relevantes:
                encontrados += 1
                suma += encontrados / i

        return suma / len(relevantes) if relevantes else 0

    def evaluar_consulta(self, recuperados_ids, relevantes_ids):
        p = self.precision(recuperados_ids, relevantes_ids)
        r = self.recall(recuperados_ids, relevantes_ids)
        f = self.f1(p, r)
        ap = self.average_precision(recuperados_ids, relevantes_ids)

        return {
            "precision": p,
            "recall": r,
            "f1": f,
            "average_precision": ap
        }


def evaluar_motor_con_corpus(motor, noticias):
    evaluador = EvaluadorIRS()

    consultas_eval = [
        {
            "consulta": "inteligencia artificial",
            "relevantes_keywords": ["inteligencia artificial", "ia", "software", "tecnología"]
        },
        {
            "consulta": "mercados financieros",
            "relevantes_keywords": ["mercado", "mercados", "finanzas", "economía", "inversión"]
        },
        {
            "consulta": "videojuegos",
            "relevantes_keywords": ["videojuego", "videojuegos", "gaming", "consola", "esports"]
        },
        {
            "consulta": "salud hospital",
            "relevantes_keywords": ["salud", "hospital", "médico", "paciente", "vacuna"]
        }
    ]

    resultados_eval = []
    map_total = 0

    for ev in consultas_eval:
        consulta = ev["consulta"]
        keywords = ev["relevantes_keywords"]

        relevantes = []

        for idx, noticia in enumerate(noticias):
            texto = f"{noticia['titulo']} {noticia['cuerpo']} {noticia.get('categoria_original', '')}".lower()

            if any(k.lower() in texto for k in keywords):
                relevantes.append(idx)

        recuperados = [
            r["doc_id"]
            for r in motor.buscar_vectorial(consulta, top_k=len(noticias))
        ]

        metricas = evaluador.evaluar_consulta(recuperados, relevantes)
        map_total += metricas["average_precision"]

        resultados_eval.append({
            "consulta": consulta,
            "relevantes": relevantes,
            "recuperados": recuperados,
            "precision": metricas["precision"],
            "recall": metricas["recall"],
            "f1": metricas["f1"],
            "average_precision": metricas["average_precision"]
        })

    map_score = map_total / max(len(consultas_eval), 1)

    return resultados_eval, map_score