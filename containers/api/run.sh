curl -v \
   -H 'content-Type: application/json' \
   -d '{"smiles":"CC(=O)OC1=CC=CC=C1C(=O)O",
        "scoreId": "42",
        "modelPath":"76/effe61bfaa14418cb3f606c2a7edf0d4/artifacts/model/Random_Forest_Ensemble.pkl"}' \
   http://10.100.181.26:8080