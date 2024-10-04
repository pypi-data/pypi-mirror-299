sites_colors = {
    "capegrim-medusa": "grey",
    "macehead-medusa": "green",
    "samoa-medusa": "mediumblue",
    "trinidadhead-medusa": "gold",
    "gosan-medusa": "darkred",
    "zeppelin-medusa": "lightskyblue",
    "jungfraujoch-medusa": "mediumorchid",
    "mtecimone-medusa": "dodgerblue",
    "taunus-medusa": "mediumslateblue",
    "sio-medusa": "darkorange",
    "sio-medusa7": "darkorange",
    "tacolneston-medusa": "darkgreen",
    "empa-medusa": "darkviolet",
    "empa-aprecon": "teal",
    #'ASA': "",
    "CGO": "grey",
    "CMN": "dodgerblue",
    "GSN": "darkred",
    "JFJ": "mediumorchid",
    "MHD": "green",
    #'RPB': "",
    "SIO": "darkorange",
    "SMO": "mediumblue",
    "TAC": "darkgreen",
    "THD": "gold",
    #'TOB': "",
    "ZEP": "lightskyblue",
}
# Add lowercase keys
sites_colors.update({key.lower(): value for key, value in sites_colors.items()})

# Default sites
sites = ["GSN", "JFJ", "gsn", "jfj"]


conc_name = "Mole fraction"
