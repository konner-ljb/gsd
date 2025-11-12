import marimo

__generated_with = "0.17.7"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt
    import marimo as mo
    import io

    uploaded_file = mo.ui.file(filetypes=['.csv'],kind="area")

    mo.vstack([uploaded_file])
    return io, mo, pd, plt, uploaded_file


@app.cell
def _(io, mo, pd, uploaded_file):
    file_bytes = uploaded_file.contents(index=0)
    if file_bytes:
        file_string = file_bytes.decode('utf-8')
        df = pd.read_csv(io.StringIO(file_string))
    else:
        df = pd.read_csv('examples/example.csv')
    samples_selector = mo.ui.multiselect.from_series(df["SampleID"], label='Select samples to plot')

    mo.vstack([samples_selector])
    return df, samples_selector


@app.cell
def _(df, plt, samples_selector):

    fig, ax = plt.subplots()
    ax.set(xlabel='Particle Size', ylabel='% Passing', title='Particle Size Distribution',xlim=(0, 8), ylim=(0, 100))
    ax.set_xlim(0.001, 100)
    ax.set_xscale('log')
    ax.grid(True, which='both')

    for sample in samples_selector.value:
        dfx = df[df['SampleID']==sample]
        x = dfx['Particle_Size']
        y = dfx['Percent_Finer']
        ax.plot(x,y)
    ax.legend(samples_selector.value)
    fig
    return


if __name__ == "__main__":
    app.run()
