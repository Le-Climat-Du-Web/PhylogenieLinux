from flask import Flask, render_template, request
from datetime import timedelta
import main

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

@app.route('/')
def mainAcceuil():
    return render_template('Acceuil.html', selectedMenu="Accueil")

@app.route('/infos')
def infos_caract():
    return render_template('infos.html', selectedMenu="Infos")

@app.route('/bdd')
def geneId():
    res = main.id_list
    names = main.name_gene
    return render_template('bdd.html', idlist=res,namegene=names, selectedMenu="Base de données")


@app.route('/bdd',methods=['GET','POST'])
def choixGene():
    if request.method == "POST":
        if request.form["submit"] == 'submit':
            id_list = request.form.getlist('choixGene')
            main.dirName = main.get_fasta(id_list)
    res=main.dirName
    return render_template('Alignement.html', res=res, selectedMenu="Alignement")

@app.route('/Alignement', methods=['POST'])
def Alignement():
    if request.method == "POST":
        if request.form["fAli"] == "Clustal":
            main.clustal_alignment("multifasta.fasta", "obtenu.fasta")
            type = 'clustal'
        elif request.form["fAli"] == "Muscle":
            main.muscle_alignment("multifasta.fasta", "obtenu.fasta")
            type = 'fasta'

        if request.form["tree"] == "Neighbor Joining":
            main.NJ_tree("obtenu.fasta", type)
        elif request.form["tree"] == "Maximum Likelihood":
            main.ML_tree("obtenu.fasta", "msa_muscle", type)
        res=main.dirName
        return render_template('tree.html', res=res, selectedMenu="Phylogénie")

if __name__ == '__main__':
    app.run(debug=True)
