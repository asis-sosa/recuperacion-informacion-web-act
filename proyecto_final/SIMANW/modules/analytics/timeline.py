import pandas as pd
from collections import Counter


class AnalizadorTemporal:

    def __init__(self, noticias):
        self.noticias = noticias

    def construir_timeline(self):

        df = pd.DataFrame(self.noticias)

        if df.empty:
            return pd.DataFrame()

        df["fecha"] = pd.to_datetime(df["fecha"])

        df["periodo"] = df["fecha"].dt.strftime("%Y-%m")

        categoria_col = (
            "categoria_predicha"
            if "categoria_predicha" in df.columns
            else "categoria_original"
        )

        resumen = (
            df.groupby(["periodo", categoria_col])
            .size()
            .reset_index(name="total")
        )

        return resumen

    def detectar_picos(self):

        timeline = self.construir_timeline()

        if timeline.empty:
            return []

        picos = []

        for categoria in timeline.iloc[:, 1].unique():

            datos = timeline[
                timeline.iloc[:, 1] == categoria
            ]

            fila = datos.loc[
                datos["total"].idxmax()
            ]

            picos.append({
                "categoria": categoria,
                "periodo": fila["periodo"],
                "total": int(fila["total"])
            })

        return picos