import streamlit as st
import py3Dmol
from stmol import showmol
import requests
import biotite.structure.io as bsio

st.set_page_config(layout = 'wide')
st.sidebar.title('🧪 ProteinWise')
st.sidebar.write('ProteinWise is an end-to-end single sequence protein structure predictor based on the [*ESM-2*](https://esmatlas.com/about) language model. For more information, read the [research article](https://www.biorxiv.org/content/10.1101/2022.07.20.500902v2) and the [news article](https://www.nature.com/articles/d41586-022-03539-1) published in *Nature*.')

def render_mol(protein):
    proteinView = py3Dmol.view()
    proteinView.addModel(protein, 'pdb')
    proteinView.setStyle({'cartoon':{'color':'spectrum'}})
    proteinView.setBackgroundColor('white')
    proteinView.zoomTo()
    proteinView.zoom(2, 800)
    proteinView.spin(True)
    showmol(proteinView, height = 500, width = 800)

DEFAULT_SEQ = "MGSSHHHHHHSSGLVPRGSHMRGPNPTAASLEASAGPFTVRSFTVSRPSGYGAGTVYYPTNAGGTVGAIAIVPGYTARQSSIKWWGPRLASHGFVVITIDTNSTLDQPSSRSSQQMAALRQVASLNGTSSSPIYGKVDTARMGVMGWSMGGGGSLISAANNPSLKAAAPQAPWDSSTNFSSVTVPTLIFACENDSIAPVNSSALPIYDSMSRNAKQFLEINGGSHSCANSGNSNQALIGKKGVAWMKRFMDNDTRYSTFACENPNSTRVSDFRTANCSLEDPAANKARKEAELAAATAEQ"
txt = st.sidebar.text_area('Input sequence', DEFAULT_SEQ, height=275)

def update(seq = txt):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.post('https://api.esmatlas.com/foldSequence/v1/pdb/', headers=headers, data=seq)
    name = seq[:3] + seq[-3:]
    protein_String = response.content.decode('utf-8')
    
    with open('predicted.pdb', 'w') as f:
        f.write(protein_String)   

    struct = bsio.load_structure('predicted.pdb', extra_fields =  ["b_factor"])
    b_value = round(struct.b_factor.mean(), 4)

    st.subheader("Visualization of the Predicted Protein Structure")
    render_mol(protein_String)

    st.subheader('plDDT')
    st.write('plDDT is a per-residue estimate of the confidence in prediction, ranging from 0-100')
    st.info(f'plDDT: {b_value}')

    st.download_button(
        label= "Download PDB",
        data = protein_String,
        file_name='predicted.pdb',
        mime= 'text/plain'
    )

predict = st.sidebar.button('Predict', on_click=update)

if not predict:
    st.warning('Enter Protein Sequence Data!')
