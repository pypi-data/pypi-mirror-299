import marimo

__generated_with = "0.8.22"
app = marimo.App(width="medium")


@app.cell
def __():
    import sudachi_sentence_splitter
    return (sudachi_sentence_splitter,)


@app.cell
def __(sudachi_sentence_splitter):
    sudachi_sentence_splitter.split_sentences("ペンギンは飛べない鳥であり、主に南半球に生息しています。中でも皇帝ペンギンは最も背が高い種で 、その高さは約120センチメートルにもなります。彼らは寒さから身を守るために厚い脂肪層を持ち、また密集した羽毛が体温を保つのに役立っています。 ペンギンは優れた泳ぎ手で、水中での速度は時速15キロメートルにも達します。さらに、彼らは社会的な動物であり、大きなコロニーを形成して生活しています。")

    return


if __name__ == "__main__":
    app.run()
