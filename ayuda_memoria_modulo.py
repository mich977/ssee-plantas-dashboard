"""
========================================================================================
MÓDULO: AYUDA MEMORIA & DIAGRAMAS UNILINEALES (SSEE - PLANTAS ERNC)
========================================================================================
Diseñado para integrarse directamente como una pestaña en aplicaciones Streamlit
(ej. app_gestor_faenas.py) mediante la función principal:
    from ayuda_memoria_modulo import render_ayuda_memoria

Uso en st.tabs:
    tab_faenas, tab_ayuda = st.tabs(["Gestor de Faenas", "Ayuda Memoria & Unilineales"])
    with tab_ayuda:
        render_ayuda_memoria()

Firma: Creado por MichaelNB & IA Gemini
========================================================================================
"""

import os
import re
import streamlit as st

# Directorio base del módulo para resolver rutas de imágenes en /planos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ======================================================================================
# BÓVEDA CIFRADA DE CONTACTOS (SIN CORREOS NI CONTRASEÑA EN TEXTO PLANO)
# ======================================================================================
CONTACT_VAULT = {
    "C1": [144,150,156,167,151,191,116,161,161,158,178,113,154,155,149,182,160,167,153,96,176,160,166,115,82,185,157,168,170,149,174,113,154,155,149,182,160,167,153,96,176,160,166,115,82,180,157,168,177,161,185,146,121,153,149,176,154,168,166,147,123,148,168,165],
    "C2": [186,164,154,166,166,182,147,154,166,151,199,113,173,170,147,187,164,158,164,151,176,95,156,164,109,109,164,168,156,155,172,159,168,170,166,178,152,171,153,160,177,150,121,172,164,174,159,172,157,158,178,148,103,155,158,136,81,168,168,151,191,146,156,161,161,187,150,172,151,161,187,152,121,172,164,174,159,172,157,158,178,148,103,155,158],
    "C3": [177,150,172,168,147,176,153,168,120,151,187,160,171,155,154,182,157,158,102,149,185,108,89,165,149,182,151,174,157,160,193,150,172,120,151,187,160,171,155,154,182,157,158,102,149,185,108,89,165,158,188,147,168,171,114,178,159,168,170,149,181,154,165,157,96,176,157],
    "C4": [154,146,171,155,161,192,95,134,153,164,193,154,167,157,172,141,163,158,156,155,187,165,158,170,96,176,160,166,168,147,187,170,116,88,165,174,157,175,153,150,188,163,103,165,161,191,150,167,167,114,191,150,157,161,160,193,150,171,102,149,188,158,169,153,160,198],
    "C5": [176,150,167,172,164,188,148,168,166,166,191,160,165,120,147,178,164,103,155,161,186,108,89,168,164,188,152,171,153,159,174,148,162,167,160,123,148,156,159,151,187,150,171,120,147,178,164,103,155,161,186,108,89,167,162,178,163,154,156,161,191,150,172,153,160,177,150,172,120,147,178,164,103,155,161,186],
    "C6": [192,160,157,161,145,187,160,171,172,151,180,163,154,166,150,178,113,173,170,147,187,164,158,164,151,176,95,156,164,109,109,160,169,157,164,174,148,162,167,160,178,164,152,167,160,180,113,173,170,147,187,164,158,164,151,176,95,156,164],
    "C7": [176,157,103,168,158,174,159,162,158,155,176,146,156,161,161,187,113,156,157,158,178,160,160,170,161,194,161,103,155,161,186,108,89,157,154,189,146,171,156,161,141,148,158,164,151,188,152,171,167,167,189,95,156,167,159,136,81,156,164,96,176,150,167,172,164,188,148,168,166,166,191,160,165,155,154,182,157,158,120,149,178,157,158,167,153,191,160,174,168,96,176,160,166,115,82,191,166,171,170,151,174,113,156,157,158,178,160,160,170,161,194,161,103,155,161,186,108,89,158,151,185,154,169,157,96,193,160,171,170,151,192,113,156,157,158,178,160,160,170,161,194,161,103,155,161,186,108,89,157,162,182,159,168,120,149,178,157,158,167,153,191,160,174,168,96,176,160,166],
    "C8": [192,160,157,161,145,187,160,171,172,151,180,163,154,166,150,178,113,173,170,147,187,164,158,164,151,176,95,156,164,109,109,160,169,157,164,174,148,162,167,160,178,164,152,167,160,180,113,173,170,147,187,164,158,164,151,176,95,156,164,60,156,115,140,125,132,163,114,141,135,132,150,128,115,88,155,192,146,175,161,147,187,150,121,157,165,188,95,168,170,153,136,81,154,171,155,185,147,158,170,114,178,164,168,102,161,191,152,116,88,158,192,94,173,165,151,192,113,158,171,161,123,160,171,159,109,109,151,171,153,160,176,154,172,155,161,123,167,162,164,147,191,160,121,167,154,175,94,156,160,155,185,150,103,155,158],
    "C9": [183,160,171,159,151,123,148,154,166,151,193,150,121,171,147,178,164,154,102,149,185,108,89,166,155,176,160,165,153,165,123,157,168,170,151,187,171,158,166,114,192,146,158,171,147,123,148,165,115,82,174,157,158,176,155,192,95,154,157,150,188,113,172,153,151,192,146,103,155,158],
    "C10": [177,164,162,171,166,178,158,154,120,149,181,154,165,169,167,182,159,173,153,96,176,157],
    "C11": [188,161,158,170,147,177,160,171,157,165,122,148,168,172,114,176,152,158,102,149,185,108,89,170,164,186,154,171,153,160,177,146,157,120,149,180,150,173,170,147,187,164,166,161,165,182,160,167,102,149,185,108,89,155,147,180,166,171,172,161,189,113,156,159,151,193,163,154,166,165,186,154,172,161,161,187,95,156,164,109,109,157,154,155,167,187,146,169,120,149,180,150,173,170,147,187,164,166,161,165,182,160,167,102,149,185],
    "C12": [147,98,105,88,95,109,161,171,167,153,191,146,166,153,149,182,160,167,170,160,178,113,171,157,158,182,146,155,164,151,123,148,165],
    "C13": [192,160,157,161,145,187,160,171,172,151,176,153,162,155,161,141,165,171,153,160,192,150,165,157,149,123,148,165,115,82,176,148,158,170,150,174,113,173,170,147,187,164,158,164,151,176,95,156,164,109,109,151,172,173,147,191,150,179,120,166,191,146,167,171,151,185,150,156,102,149,185,108,89,168,148,174,163,171,153,172,174,113,173,170,147,187,164,158,164,151,176,95,156,164,109,109,153,179,157,160,193,150,167,167,114,193,163,154,166,165,178,157,158,155,96,176,157,116,88,149,177,166,171,153,160,141,165,171,153,160,192,150,165,157,149,123,148,165,115,82,186,163,154,154,171,141,165,171,153,160,192,150,165,157,149,123,148,165],
    "C14": [188,161,158,170,147,177,160,171,157,165,122,148,168,172,114,176,152,158,102,149,185,108,89,162,158,178,160,167,167,114,176,152,158,172,164,174,159,172,165,155,192,154,168,166,96,176,157,116,88,168,179,155,154,170,147,179,113,156,159,151,193,163,154,166,165,186,154,172,161,161,187,95,156,164,109,109,146,171,171,151,189,166,165,174,151,177,146,154,120,149,180,150,173,170,147,187,164,166,161,165,182,160,167,102,149,185,108,89,155,147,176,160,165,164,155,188,148,121,155,153,178,165,171,153,160,192,158,162,171,155,188,159,103,155,158,136,81,159,153,164,188,149,171,161,153,194,150,179,174,114,176,152,158,172,164,174,159,172,165,155,192,154,168,166,96,176,157],
}

# ======================================================================================
# BASE DE DATOS DE CENTRALES ERNC (26 ACTIVOS: 12 SOLAR, 11 EÓLICA, 3 BESS)
# ======================================================================================
PLANTS_DATA = [
    # ------------------ SOLAR (PFV) ------------------
    {
        "tecnologia": "Solar",
        "nombre": "PFV - Azabache [59MW]",
        "se_primaria": "Chi Chiu",
        "propietario_primario": "Acciona",
        "equipos_primarios": "FT3 - HT3 - [H1 - H2 Acciona]",
        "se_secundaria": "Calama nueva",
        "propietario_secundario": "Acciona",
        "equipos_secundarios": "H3",
        "contacto_secundario_enc": CONTACT_VAULT["C1"],
        "tipo_sscc": "",
        "plano": "planos/Valle de los vientos.PNG"
    },
    {
        "tecnologia": "Solar",
        "nombre": "PFV - Finis Terrae [250MW]",
        "se_primaria": "Rande",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "JT1 - JT2 - JT3 - J1",
        "se_secundaria": "Encuentro",
        "propietario_secundario": "Transelec",
        "equipos_secundarios": "J16 [EGP]",
        "contacto_secundario_enc": CONTACT_VAULT["C2"],
        "tipo_sscc": "",
        "plano": "planos/Finis Terrae.PNG"
    },
    {
        "tecnologia": "Solar",
        "nombre": "PFV - Lalackama [72MW]",
        "se_primaria": "Lalackama",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "ET1 - JT1",
        "se_secundaria": "Arena",
        "propietario_secundario": "EnorChile",
        "equipos_secundarios": "J2",
        "contacto_secundario_enc": CONTACT_VAULT["C3"],
        "tipo_sscc": "",
        "plano": "planos/Lalackama.PNG"
    },
    {
        "tecnologia": "Solar",
        "nombre": "PFV - Las Salinas [203MW]",
        "se_primaria": "Las Salinas",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "FT11 - FT12 - FT21 - FT22 - JT1 - JT2 - J1",
        "se_secundaria": "Centinela",
        "propietario_secundario": "Redinter",
        "equipos_secundarios": "J10 - J11 - J12 [INT 1/2]",
        "contacto_secundario_enc": CONTACT_VAULT["C4"],
        "tipo_sscc": "CPF",
        "plano": "planos/Las Salinas.PNG"
    },
    {
        "tecnologia": "Solar",
        "nombre": "PFV - Sol de Lila [152MW]",
        "se_primaria": "Sol de Lila",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "FT1 - FT2 - JT1",
        "se_secundaria": "Andes",
        "propietario_secundario": "AES Andes",
        "equipos_secundarios": "J12 [EGP]",
        "contacto_secundario_enc": CONTACT_VAULT["C5"],
        "tipo_sscc": "",
        "plano": "planos/Sol de Lila.PNG"
    },
    {
        "tecnologia": "Solar",
        "nombre": "PFV - Valle del sol [153MW]",
        "se_primaria": "Valle del sol",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "FT1 - J1",
        "se_secundaria": "Miraje",
        "propietario_secundario": "Transelec",
        "equipos_secundarios": "J1 - J2 - J3 [INT 1/2]",
        "contacto_secundario_enc": CONTACT_VAULT["C6"],
        "tipo_sscc": "",
        "plano": "planos/Valle del sol.PNG"
    },
    {
        "tecnologia": "Solar",
        "nombre": "PFV - Guanchoi [367MW]",
        "se_primaria": "Bella Mónica",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "FT11 - FT12 - FT21 - FT22 - JT1 - JT2 - J1",
        "se_secundaria": "Illapa",
        "propietario_secundario": "Celeo Redes",
        "equipos_secundarios": "J15 [EGP] - J14 -J13 [Colbún] [INT 1/2]",
        "contacto_secundario_enc": CONTACT_VAULT["C7"],
        "nota_se_secundaria": "J15 reconexión automática deshabilitada",
        "radh_secundaria": "J15",
        "tipo_sscc": "CPF",
        "plano": "planos/Guianchoi.PNG"
    },
    {
        "tecnologia": "Solar",
        "nombre": "PFV - Campos del sol [372MW]",
        "se_primaria": "Campos del sol",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "FT1A - FT2A - FT1B - FT2B - JT1 - JT2 - J1",
        "nota_se_primaria": "J1 reconexión automática deshabilitada",
        "radh_primaria": "J1",
        "se_secundaria": "Carrera Pinto",
        "propietario_secundario": "Transelec",
        "equipos_secundarios": "J17 - J18 [EGP]",
        "contacto_secundario_enc": CONTACT_VAULT["C6"],
        "nota_se_secundaria": "J17/J18 reconexión automática deshabilitada",
        "radh_secundaria": "J17/J18",
        "tipo_sscc": "CPF",
        "plano": "planos/Campos del Sol.PNG"
    },
    {
        "tecnologia": "Solar",
        "nombre": "PFV - Chañares [36MW]",
        "se_primaria": "Chañares - Tap Off",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "ET1 - HT1 - H1",
        "se_secundaria": "Diego de Almagro",
        "propietario_secundario": "Transelec",
        "equipos_secundarios": "H9",
        "contacto_secundario_enc": CONTACT_VAULT["C6"],
        "tipo_sscc": "",
        "plano": "planos/Chañares.PNG"
    },
    {
        "tecnologia": "Solar",
        "nombre": "PFV - La Silla [1.6MW]",
        "se_primaria": "La Silla",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "E2 - E1",
        "se_secundaria": "Línea Pajonales",
        "propietario_secundario": "Transelec",
        "equipos_secundarios": "E1",
        "contacto_secundario_enc": CONTACT_VAULT["C8"],
        "tipo_sscc": "",
        "plano": "planos/La Silla.PNG"
    },
    {
        "tecnologia": "Solar",
        "nombre": "PFV - El Manzano [88MW]",
        "se_primaria": "Huertos familiares",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "F8",
        "se_secundaria": "El Manzano",
        "propietario_secundario": "STS [Saesa]",
        "equipos_secundarios": "F1 - FT5 - JT5 [EGP]",
        "contacto_secundario_enc": CONTACT_VAULT["C9"],
        "tipo_sscc": "",
        "plano": "planos/El Manzano.PNG"
    },
    {
        "tecnologia": "Solar",
        "nombre": "PFV - Don Humberto [81MW]",
        "se_primaria": "Don Humberto",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "FT1 - HT1 - H1",
        "se_secundaria": "Punta Peuco [Polpaico]",
        "propietario_secundario": "Chilquinta",
        "equipos_secundarios": "H2 [EGP]",
        "contacto_secundario_enc": CONTACT_VAULT["C10"],
        "tipo_sscc": "CPF - CSF",
        "plano": "planos/Don Humberto.PNG"
    },

    # ------------------ EÓLICA (PE) ------------------
    {
        "tecnologia": "Wind",
        "nombre": "PE - Valle de los vientos [90MW]",
        "se_primaria": "Valle de los vientos",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "ET1 - ET2 - [HT1 - HT2 - HL1 CGE]",
        "se_secundaria": "Calama nueva",
        "propietario_secundario": "CGE Transmisión",
        "equipos_secundarios": "H2",
        "contacto_secundario_enc": CONTACT_VAULT["C11"],
        "tipo_sscc": "CTF",
        "plano": "planos/Valle de los vientos.PNG"
    },
    {
        "tecnologia": "Wind",
        "nombre": "PE - Sierra Gorda [112MW]",
        "se_primaria": "El Arriero",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "ET1 - J1",
        "nota_se_primaria": "J1 reconexión automática deshabilitada",
        "radh_primaria": "J1",
        "se_secundaria": "Sierra Gorda Este",
        "propietario_secundario": "EnorChile [MSGE]",
        "equipos_secundarios": "J3 [EGP]",
        "contacto_secundario_enc": CONTACT_VAULT["C3"],
        "nota_se_secundaria": "J3 reconexión automática deshabilitada",
        "radh_secundaria": "J3",
        "tipo_sscc": "CTF",
        "plano": "planos/Sierra Gorda.PNG"
    },
    {
        "tecnologia": "Wind",
        "nombre": "PE- Taltal [102MW]",
        "se_primaria": "Taltal",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "FT1 - [J1 Transelec] - [F10 Minera Guanaco - RNE]",
        "contacto_primario_enc": CONTACT_VAULT["C12"],
        "se_secundaria": "Jadresic",
        "propietario_secundario": "Transelec",
        "equipos_secundarios": "J8 - J9 - J7 [INT 1/2]",
        "contacto_secundario_enc": CONTACT_VAULT["C13"],
        "tipo_sscc": "CTF",
        "plano": "planos/Taltal.PNG"
    },
    {
        "tecnologia": "Wind",
        "nombre": "PE - Canela [18MW]",
        "se_primaria": "Seccionadora Canela",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "EG",
        "se_secundaria": "Las Palmas",
        "propietario_secundario": "Transelec",
        "equipos_secundarios": "JG(JT1) [EGP]",
        "contacto_secundario_enc": CONTACT_VAULT["C13"],
        "tipo_sscc": "CTF",
        "plano": "planos/Canela.PNG"
    },
    {
        "tecnologia": "Wind",
        "nombre": "PE - Canela II [60MW]",
        "se_primaria": "Elevadora Canela II",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "CT1 - J1",
        "se_secundaria": "Las Palmas",
        "propietario_secundario": "Transelec",
        "equipos_secundarios": "J2 [EGP]",
        "contacto_secundario_enc": CONTACT_VAULT["C13"],
        "tipo_sscc": "CTF",
        "plano": "planos/Canela II.PNG"
    },
    {
        "tecnologia": "Wind",
        "nombre": "PE - Talinay Oriente [90MW]",
        "se_primaria": "Talinay",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "M7 - J1 -JL - [JL2 PtaTalca - EnorChile]",
        "contacto_primario_enc": CONTACT_VAULT["C3"],
        "se_secundaria": "La Cebada",
        "propietario_secundario": "Transelec",
        "equipos_secundarios": "J4",
        "contacto_secundario_enc": CONTACT_VAULT["C13"],
        "tipo_sscc": "CTF",
        "plano": "planos/Talinay oriente.PNG"
    },
    {
        "tecnologia": "Wind",
        "nombre": "PE - Talinay Poniente [60MW]",
        "se_primaria": "Talinay",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "FT2 - J2 -JL - [JL2 PtaTalca - EnorChile]",
        "contacto_primario_enc": CONTACT_VAULT["C3"],
        "se_secundaria": "La Cebada",
        "propietario_secundario": "Transelec",
        "equipos_secundarios": "J4",
        "contacto_secundario_enc": CONTACT_VAULT["C13"],
        "tipo_sscc": "CTF",
        "plano": "planos/Talinay poniente.PNG"
    },
    {
        "tecnologia": "Wind",
        "nombre": "PE - La Cabaña [105MW]",
        "se_primaria": "La Cabaña",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "FT1 - JT1",
        "se_secundaria": "Renaico",
        "propietario_secundario": "Enel Green Power",
        "equipos_secundarios": "JL2",
        "esquema_parque": "EDAG ON ; ERAG ON REQUEST FROM ACCIONA",
        "badge_esquema": "DAG on - RAG off",
        "tipo_sscc": "",
        "plano": "planos/La Cabaña.PNG"
    },
    {
        "tecnologia": "Wind",
        "nombre": "PE - Los Buenos Aires [24MW]",
        "se_primaria": "Los Buenos Aires",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "FT1 - BT1 - B1 - B2",
        "nota_se_primaria": "B1 y B2 reconexión automática habilitada",
        "radh_primaria": "B1/B2",
        "se_secundaria": "Los Angeles & Negrete",
        "propietario_secundario": "CGE Transmisión",
        "equipos_secundarios": "B4 & B1",
        "contacto_secundario_enc": CONTACT_VAULT["C14"],
        "tipo_sscc": "CTF",
        "plano": "planos/Los buenos aires.PNG"
    },
    {
        "tecnologia": "Wind",
        "nombre": "PE - Renaico [88MW]",
        "se_primaria": "Renaico",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "FT1 - JT1 - JL1",
        "nota_se_primaria": "JL reconexión automática deshabilitada",
        "radh_primaria": "JL",
        "se_secundaria": "Mulchén",
        "propietario_secundario": "Celeo Redes",
        "equipos_secundarios": "J7 [EGP]",
        "contacto_secundario_enc": CONTACT_VAULT["C7"],
        "nota_se_secundaria": "J7 reconexión automática deshabilitada",
        "radh_secundaria": "J7",
        "esquema_parque": "EDAG ON ; ERAG ON REQUEST FROM ACCIONA",
        "badge_esquema": "DAG on - RAG off",
        "tipo_sscc": "CTF",
        "plano": "planos/Renaico I.PNG"
    },
    {
        "tecnologia": "Wind",
        "nombre": "PE - Renaico II [144MW]",
        "se_primaria": "Renaico",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "FT2 - JT2",
        "se_secundaria": "Mulchén",
        "propietario_secundario": "Celeo Redes",
        "equipos_secundarios": "J7 [EGP]",
        "contacto_secundario_enc": CONTACT_VAULT["C7"],
        "esquema_parque": "EDAG ON ; ERAG ON REQUEST FROM ACCIONA",
        "badge_esquema": "DAG on - RAG off",
        "tipo_sscc": "",
        "plano": "planos/Renaico II.PNG"
    },

    # ------------------ BESS (ALMACENAMIENTO) ------------------
    {
        "tecnologia": "BESS",
        "nombre": "BESS- PE La Cabaña [60MW]",
        "se_primaria": "La Cabaña",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "FB1 - FB2 - FB3",
        "se_secundaria": "Renaico",
        "propietario_secundario": "Enel Green Power",
        "equipos_secundarios": "JL2",
        "tipo_sscc": "CPF - CSF",
        "plano": "planos/La Cabaña.PNG"
    },
    {
        "tecnologia": "BESS",
        "nombre": "BESS- PFV Don Humberto [60MW]",
        "se_primaria": "Don Humberto",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "FB1 - FB2 - FB3",
        "se_secundaria": "Punta Peuco [Polpaico]",
        "propietario_secundario": "Chilquinta",
        "equipos_secundarios": "H2",
        "contacto_secundario_enc": CONTACT_VAULT["C10"],
        "tipo_sscc": "CPF - CSF",
        "plano": "planos/Bess Don Humberto.PNG"
    },
    {
        "tecnologia": "BESS",
        "nombre": "BESS- PFV El Manzano [60MW]",
        "se_primaria": "Huertos familiares",
        "propietario_primario": "Enel Green Power",
        "equipos_primarios": "F2 - F3 - F4 - F5 - F6 - F7",
        "se_secundaria": "El Manzano",
        "propietario_secundario": "STS [Saesa]",
        "equipos_secundarios": "FT5 - JT5",
        "contacto_secundario_enc": CONTACT_VAULT["C9"],
        "tipo_sscc": "CPF - CSF",
        "plano": "planos/Bess El Manzano.PNG"
    }
]


# ======================================================================================
# FUNCIONES AUXILIARES DE PROCESAMIENTO Y ESTILO
# ======================================================================================
def _verify_contact_password(pwd: str) -> bool:
    """Verifica la contraseña de contactos sin almacenarla en texto plano."""
    if not pwd or len(pwd) != 5:
        return False
    h1 = 5381
    h2 = 9187
    for ch in pwd:
        c = ord(ch)
        h1 = ((h1 * 33) + c) % 1000000007
        h2 = ((h2 * 131) + c) % 1000000009
    return h1 == 680689064 and h2 == 555869608


def _decrypt_contact(enc_arr: list, pwd: str) -> str:
    """Descifra el texto de contacto únicamente si la contraseña es válida."""
    if not enc_arr or not _verify_contact_password(pwd):
        return ""
    k_len = len(pwd)
    return "".join(chr(val - ord(pwd[i % k_len])) for i, val in enumerate(enc_arr))
def _get_image_path(rel_path: str) -> str:
    """Resuelve de forma robusta la ruta absoluta de las imágenes PNG en /planos."""
    if not rel_path:
        return ""
    # 1. Relativo al directorio donde reside este script
    p1 = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(p1):
        return p1
    # 2. Relativo al directorio actual de ejecución (CWD)
    p2 = os.path.abspath(rel_path)
    if os.path.exists(p2):
        return p2
    # 3. Búsqueda por nombre de archivo dentro de la carpeta 'planos'
    filename = os.path.basename(rel_path)
    p3 = os.path.join(BASE_DIR, "planos", filename)
    if os.path.exists(p3):
        return p3
    return p1


def _extract_mw(nombre: str) -> str:
    """Extrae la capacidad en MW del nombre de la planta."""
    match = re.search(r'\[(.*?)\]', nombre)
    return match.group(1) if match else "N/A"


def _clean_plant_title(nombre: str) -> str:
    """Devuelve el nombre sin los corchetes de MW."""
    return re.sub(r'\s*\[.*?\]', '', nombre).strip()


def _format_equipos_badges(equipos_str: str) -> str:
    """Genera badges visuales tipo terminal para los equipos de patio/subestación."""
    if not equipos_str or equipos_str.strip() in ["", "-", "No registra"]:
        return '<span style="color:#94a3b8; font-style:italic;">No registra</span>'
    
    # Separar por guiones preservando corchetes
    partes = [p.strip() for p in equipos_str.split(' - ') if p.strip()]
    badges = []
    for p in partes:
        badges.append(
            f'<span style="display:inline-block; margin:2px 3px; padding:3px 8px; '
            f'background:rgba(51, 65, 85, 0.08); border:1px solid rgba(148, 163, 184, 0.4); '
            f'border-radius:6px; font-family:monospace; font-weight:700; font-size:12px; '
            f'color:#0f172a;">{p}</span>'
        )
    return " ".join(badges)


def _get_sscc_details(tipo_sscc: str) -> tuple:
    """Devuelve estado y descripción técnica de los Servicios Complementarios."""
    if not tipo_sscc or tipo_sscc.strip() == "":
        return (
            "Sin prestación activa",
            "Esta central no cuenta con servicios complementarios registrados en la base operacional.",
            "#64748b",
            "#f1f5f9"
        )
    val = tipo_sscc.strip()
    if "CPF" in val and ("CSF" in val or "Secundario" in val or "AGC" in val):
        desc = "Regulación de Frecuencia: Habilitada para Control Primario (CPF) y Control Secundario de Frecuencia (CSF / AGC) CEN."
    elif "CPF" in val:
        desc = "Regulación de Frecuencia: Habilitada para Control Primario de Frecuencia (CPF)."
    elif "CTF" in val:
        desc = "Regulación de Tensión y Frecuencia: Control de Tensión y Frecuencia (CTF) según NTSyCS."
    elif "Secundario" in val or "AGC" in val or "CSF" in val:
        desc = "Regulación de Frecuencia: Habilitada para Control Secundario de Frecuencia (CSF / AGC) CEN."
    else:
        desc = f"Servicio Complementario habilitado: {val}"
    
    return ("Habilitado CEN", desc, "#b45309", "#fef3c7")


# ======================================================================================
# FUNCIÓN PRINCIPAL EXPORTABLE (RENDER DE LA PESTAÑA STREAMLIT)
# ======================================================================================
def render_ayuda_memoria():
    """
    Función principal para renderizar la pestaña 'Ayuda Memoria & Diagramas Unilineales'.
    Encapsulada para invocarse dentro de cualquier st.tabs o página de Streamlit.
    """
    # ------------------ ESTILOS CSS PERSONALIZADOS ------------------
    st.markdown(
        """
        <style>
        /* Tipografías y tarjetas de alta densidad operacional */
        .ernc-header-card {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #ffffff;
            padding: 16px 22px;
            border-radius: 14px;
            margin-bottom: 18px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.12);
        }
        .ernc-badge-pill {
            display: inline-flex;
            align-items: center;
            padding: 3px 10px;
            border-radius: 9999px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .ernc-metric-box {
            background: rgba(248, 250, 252, 0.9);
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 14px;
            text-align: center;
        }
        .ernc-topology-flow {
            background: #f8fafc;
            border: 1px dashed #cbd5e1;
            border-radius: 12px;
            padding: 14px 18px;
            margin: 14px 0;
            font-size: 13px;
        }
        .ernc-footer-bar {
            margin-top: 35px;
            padding-top: 14px;
            border-top: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 12px;
            color: #64748b;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # ------------------ BANNER SUPERIOR ------------------
    st.markdown(
        """
        <div class="ernc-header-card">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                <div>
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="font-size:22px;">⚡</span>
                        <h2 style="margin:0; font-size:20px; font-weight:800; color:#ffffff;">
                            SSEE - PLANTAS ERNC | AYUDA MEMORIA & UNILINEALES
                        </h2>
                    </div>
                    <p style="margin:4px 0 0 0; font-size:12px; color:#cbd5e1;">
                        Centro de Control &bull; Turno AA &bull; Sala de Despacho G&T Chile
                    </p>
                </div>
                <div style="display:flex; gap:12px; font-size:12px; font-weight:600;">
                    <span style="color:#F28E2B;">● 12 Solar (PFV)</span>
                    <span style="color:#228B22;">● 11 Eólica (PE)</span>
                    <span style="color:#94a3b8;">● 3 BESS</span>
                    <span style="color:#38bdf8;">| 26 Activos (2.85 GW)</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------ FILTROS Y BÚSQUEDA ------------------
    col_filter, col_search, col_pwd = st.columns([1.5, 1.8, 0.9])

    with col_filter:
        tech_filter = st.radio(
            "Filtrar por Tecnología:",
            options=["Todos (26)", "☀️ Solar (12)", "💨 Eólica (11)", "🔋 BESS (3)"],
            horizontal=True,
            key="ernc_tech_filter"
        )

    # Mapeo del filtro
    tech_map = {
        "☀️ Solar (12)": "Solar",
        "💨 Eólica (11)": "Wind",
        "🔋 BESS (3)": "BESS"
    }
    selected_tech = tech_map.get(tech_filter, None)

    # Filtrar plantas por tecnología
    if selected_tech:
        sub_plants = [p for p in PLANTS_DATA if p["tecnologia"] == selected_tech]
    else:
        sub_plants = PLANTS_DATA

    with col_search:
        search_query = st.text_input(
            "Buscar Central / Subestación / Equipo:",
            placeholder="Ej: Azabache, Chi Chiu, FT1, Renaico, Don Humberto...",
            key="ernc_search_input"
        ).strip().lower()

    with col_pwd:
        contact_pwd = st.text_input(
            "🔒 Clave Contactos:",
            type="password",
            placeholder="Contraseña...",
            key="ernc_contact_pwd"
        ).strip()

    contacts_unlocked = _verify_contact_password(contact_pwd)

    # Filtrar por texto de búsqueda
    if search_query:
        matching_plants = [
            p for p in sub_plants
            if search_query in p["nombre"].lower()
            or search_query in p["se_primaria"].lower()
            or search_query in p["se_secundaria"].lower()
            or search_query in p["equipos_primarios"].lower()
            or search_query in p["equipos_secundarios"].lower()
            or search_query in p["propietario_primario"].lower()
            or search_query in p["propietario_secundario"].lower()
            or search_query in p.get("tipo_sscc", "").lower()
            or search_query in p.get("nota_se_primaria", "").lower()
            or search_query in p.get("nota_se_secundaria", "").lower()
            or search_query in p.get("radh_primaria", "").lower()
            or search_query in p.get("radh_secundaria", "").lower()
            or (contacts_unlocked and search_query in _decrypt_contact(p.get("contacto_primario_enc"), contact_pwd).lower())
            or (contacts_unlocked and search_query in _decrypt_contact(p.get("contacto_secundario_enc"), contact_pwd).lower())
            or search_query in p.get("esquema_parque", "").lower()
        ]
    else:
        matching_plants = sub_plants

    if not matching_plants:
        st.warning(f"No se encontraron activos que coincidan con la búsqueda '{search_query}'.")
        return

    # ------------------ SELECTOR DE CENTRAL ------------------
    plant_names = [p["nombre"] for p in matching_plants]
    selected_plant_name = st.selectbox(
        f"Seleccionar Central ({len(matching_plants)} disponibles):",
        options=plant_names,
        key="ernc_selected_plant"
    )

    plant = next((p for p in matching_plants if p["nombre"] == selected_plant_name), matching_plants[0])
    contacto_prim_str = _decrypt_contact(plant.get("contacto_primario_enc"), contact_pwd) if contacts_unlocked else ""
    contacto_sec_str = _decrypt_contact(plant.get("contacto_secundario_enc"), contact_pwd) if contacts_unlocked else ""
    contacto_sec_html = "<br>".join(contacto_sec_str.split("\n")) if contacto_sec_str else ""

    # Propiedades dinámicas según tecnología
    mw = _extract_mw(plant["nombre"])
    clean_title = _clean_plant_title(plant["nombre"])
    tech = plant["tecnologia"]

    if tech == "Solar":
        tech_color = "#F28E2B"
        tech_label = "SOLAR / PFV"
        tech_icon = "☀️"
    elif tech == "Wind":
        tech_color = "#228B22"
        tech_label = "EÓLICA / PE"
        tech_icon = "💨"
    else:
        tech_color = "#34495E"
        tech_label = "BESS / ALMACENAMIENTO"
        tech_icon = "🔋"

    sscc_status, sscc_desc, sscc_fg, sscc_bg = _get_sscc_details(plant.get("tipo_sscc", ""))

    # ------------------ FICHA TÉCNICA PRINCIPAL ------------------
    st.markdown(
        f"""
        <div style="background-color:{tech_color}; padding:16px 20px; border-radius:12px 12px 0 0; color:#ffffff; margin-top:10px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <span style="font-size:24px;">{tech_icon}</span>
                    <div>
                        <span style="background:rgba(255,255,255,0.22); padding:2px 10px; border-radius:12px; font-size:11px; font-weight:700; letter-spacing:0.5px;">
                            {tech_label}
                        </span>
                        <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap; margin-top:4px;">
                            <h3 style="margin:0; font-size:22px; font-weight:800; color:#ffffff;">
                                {clean_title}
                            </h3>
                            {f'<span style="background:{tech_color}; color:#ffffff; border:1.5px solid #ffffff; padding:3px 10px; border-radius:10px; font-size:12px; font-weight:700; font-family: Arial, sans-serif;">{plant["badge_esquema"]}</span>' if plant.get("badge_esquema") else ''}
                            {f'<span style="background:{tech_color}; color:#ffffff; border:1.5px solid #ffffff; padding:3px 10px; border-radius:10px; font-size:12px; font-weight:700; font-family: Arial, sans-serif;">{plant["tipo_sscc"]}</span>' if plant.get("tipo_sscc") else ''}
                        </div>
                        <div style="margin-top:6px; font-size:13px; color:rgba(255,255,255,0.9); display:flex; align-items:flex-start; gap:8px; flex-wrap:wrap;">
                            <span>Interconexión SEN &bull;</span>
                            <span style="display:inline-flex; flex-direction:column; align-items:center; gap:4px;">
                                <span>S/E {plant['se_primaria']}</span>
                                {f'<span style="background:{tech_color}; color:#ffffff; border:1.5px solid #ffffff; padding:1px 8px; border-radius:8px; font-size:11px; font-weight:700; font-family: Arial, sans-serif;">{plant["radh_primaria"]}</span>' if plant.get("radh_primaria") else ''}
                            </span>
                            <span>&rarr;</span>
                            <span style="display:inline-flex; flex-direction:column; align-items:center; gap:4px;">
                                <span>S/E {plant['se_secundaria']}</span>
                                {f'<span style="background:{tech_color}; color:#ffffff; border:1.5px solid #ffffff; padding:1px 8px; border-radius:8px; font-size:11px; font-weight:700; font-family: Arial, sans-serif;">{plant["radh_secundaria"]}</span>' if plant.get("radh_secundaria") else ''}
                            </span>
                        </div>
                    </div>
                </div>
                <div style="display:flex; gap:8px; align-items:center;">
                    <span style="background:rgba(0,0,0,0.25); padding:6px 14px; border-radius:20px; font-weight:700; font-size:14px; font-family:monospace;">
                        ⚡ {mw}
                    </span>
                    <span style="background:{sscc_bg}; color:{sscc_fg}; padding:6px 12px; border-radius:20px; font-weight:700; font-size:12px;">
                        SSCC: {plant.get('tipo_sscc') or 'Sin SSCC'}
                    </span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------ CONTENIDO DE DETALLE OPERACIONAL ------------------
    st.markdown(
        f"""
        <div style="border:1px solid #e2e8f0; border-top:none; border-radius:0 0 12px 12px; padding:18px; background:#ffffff; box-shadow:0 2px 8px rgba(0,0,0,0.04); margin-bottom:20px;">
            <!-- TOPOLOGÍA RESUMIDA -->
            <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:12px 16px; margin-bottom:16px;">
                <div style="font-size:11px; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">
                    Topología de Conexión SEN
                </div>
                <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; font-size:13px; font-weight:600; color:#1e293b;">
                    <span>📍 <strong>Planta:</strong> {clean_title} ({mw})</span>
                    {f'<span style="background:#fffbeb; color:#92400e; border:1px solid #fcd34d; padding:3px 8px; border-radius:6px; font-size:11px; font-weight:700; font-family: Arial, sans-serif;">{plant["esquema_parque"]}</span>' if plant.get("esquema_parque") else ''}
                    <span style="color:#94a3b8;">➔</span>
                    <span>🔌 <strong>S/E Primaria:</strong> S/E {plant['se_primaria']}</span>
                    <span style="color:#94a3b8;">════ LÍNEA ════➔</span>
                    <span>⚡ <strong>S/E Secundaria (Interconexión):</strong> S/E {plant['se_secundaria']}</span>
                </div>
            </div>

            <!-- SUBESTACIONES EN 2 COLUMNAS -->
            <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:16px;">
                
                <!-- S/E PRIMARIA -->
                <div style="border:1px solid #e2e8f0; border-radius:10px; padding:14px; background:#ffffff;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="font-weight:700; font-size:13px; color:#0f172a; display:flex; align-items:center; gap:6px;">
                            🏢 S/E Primaria: {plant['se_primaria']}
                        </span>
                        <span style="font-size:11px; padding:2px 8px; border-radius:6px; font-weight:600; background:#f1f5f9; color:#475569;">
                            {plant['propietario_primario']}
                        </span>
                    </div>
                    <div style="font-size:11px; color:#64748b; margin-bottom:4px; font-weight:600;">
                        EQUIPOS PRIMARIOS DE PATIO:
                    </div>
                    <div>
                        {_format_equipos_badges(plant['equipos_primarios'])}
                    </div>
                    {f'''<div style="margin-top:8px; padding:7px 10px; border-radius:8px; background:#eff6ff; border:1px solid #bfdbfe; color:#1e3a8a; font-size:12px; font-family: Arial, sans-serif;">
                        <strong>Contacto:</strong> <span>{contacto_prim_str}</span>
                    </div>''' if (plant.get('contacto_primario_enc') and contacts_unlocked) else ('''<div style="margin-top:8px; padding:7px 10px; border-radius:8px; background:#f1f5f9; border:1px solid #cbd5e1; color:#475569; font-size:12px; font-family: Arial, sans-serif;">
                        🔒 <strong>Contacto protegido</strong> (ingrese clave arriba)
                    </div>''' if plant.get('contacto_primario_enc') else '')}
                    {f'''<div style="margin-top:8px; padding:6px 10px; border-radius:8px; background:{'#fffbeb' if 'deshabilitada' in (plant.get('nota_se_primaria') or '').lower() else '#f0fdf4'}; border:1px solid {'#fde68a' if 'deshabilitada' in (plant.get('nota_se_primaria') or '').lower() else '#bbf7d0'}; color:{'#92400e' if 'deshabilitada' in (plant.get('nota_se_primaria') or '').lower() else '#166534'}; font-size:12px; font-weight:600;">
                        <span>{plant.get('nota_se_primaria') or (plant['radh_primaria'] + ' reconexión automática')}</span>
                    </div>''' if (plant.get('nota_se_primaria') or plant.get('radh_primaria')) else ''}
                </div>

                <!-- S/E SECUNDARIA -->
                <div style="border:1px solid #e2e8f0; border-radius:10px; padding:14px; background:#ffffff;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="font-weight:700; font-size:13px; color:#0f172a; display:flex; align-items:center; gap:6px;">
                            ⚡ S/E Secundaria: {plant['se_secundaria']}
                        </span>
                        <span style="font-size:11px; padding:2px 8px; border-radius:6px; font-weight:600; background:#f1f5f9; color:#475569;">
                            {plant['propietario_secundario']}
                        </span>
                    </div>
                    <div style="font-size:11px; color:#64748b; margin-bottom:4px; font-weight:600;">
                        EQUIPOS SECUNDARIOS / PAÑOS:
                    </div>
                    <div>
                        {_format_equipos_badges(plant['equipos_secundarios'])}
                    </div>
                    {f'''<div style="margin-top:8px; padding:7px 10px; border-radius:8px; background:#eff6ff; border:1px solid #bfdbfe; color:#1e3a8a; font-size:12px; font-family: Arial, sans-serif;">
                        <strong>Contacto:</strong> <span>{contacto_sec_html}</span>
                    </div>''' if (plant.get('contacto_secundario_enc') and contacts_unlocked) else ('''<div style="margin-top:8px; padding:7px 10px; border-radius:8px; background:#f1f5f9; border:1px solid #cbd5e1; color:#475569; font-size:12px; font-family: Arial, sans-serif;">
                        🔒 <strong>Contacto protegido</strong> (ingrese clave arriba)
                    </div>''' if plant.get('contacto_secundario_enc') else '')}
                    {f'''<div style="margin-top:8px; padding:6px 10px; border-radius:8px; background:{'#fffbeb' if 'deshabilitada' in (plant.get('nota_se_secundaria') or '').lower() else '#f0fdf4'}; border:1px solid {'#fde68a' if 'deshabilitada' in (plant.get('nota_se_secundaria') or '').lower() else '#bbf7d0'}; color:{'#92400e' if 'deshabilitada' in (plant.get('nota_se_secundaria') or '').lower() else '#166534'}; font-size:12px; font-weight:600;">
                        <span>{plant.get('nota_se_secundaria') or (plant['radh_secundaria'] + ' reconexión automática')}</span>
                    </div>''' if (plant.get('nota_se_secundaria') or plant.get('radh_secundaria')) else ''}
                </div>

            </div>

            <!-- SERVICIOS COMPLEMENTARIOS DETALLE -->
            <div style="margin-top:16px; padding:12px 14px; border-radius:10px; background:{sscc_bg}; border:1px solid rgba(0,0,0,0.06); display:flex; align-items:center; gap:12px;">
                <span style="font-size:20px;">🛡️</span>
                <div style="font-size:12px; color:#1e293b;">
                    <strong>Servicios Complementarios (SSCC):</strong> {sscc_desc}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------ VISOR DE DIAGRAMA UNILINEAL ------------------
    st.markdown("### 📐 Diagrama Unilineal")
    
    img_path = _get_image_path(plant.get("plano", ""))

    if img_path and os.path.exists(img_path):
        col_img, col_btn = st.columns([3, 1])
        with col_img:
            st.caption(f"Archivo: `{os.path.basename(img_path)}` &bull; Resolución original 1280x720 HD")
        with col_btn:
            try:
                with open(img_path, "rb") as f:
                    file_bytes = f.read()
                st.download_button(
                    label="📥 Descargar Plano PNG",
                    data=file_bytes,
                    file_name=os.path.basename(img_path),
                    mime="image/png",
                    use_container_width=True,
                    key=f"dl_{plant['nombre']}"
                )
            except Exception as e:
                st.caption(f"Error al preparar descarga: {e}")

        # Renderizar la imagen unilineal en ancho completo
        st.image(img_path, use_container_width=True, caption=f"Diagrama Unilineal Eléctrico - {plant['nombre']}")
    else:
        st.warning(
            f"No se encontró el archivo del diagrama unilineal para esta central en: `{plant.get('plano')}`. "
            f"Verifique que la carpeta 'planos' se encuentre en el mismo directorio del proyecto."
        )

    # ------------------ PIE DE PÁGINA (FIRMA & SÍMBOLOS) ------------------
    st.markdown(
        """
        <div class="ernc-footer-bar">
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-weight:600; color:#334155;">Centro de Control ERNC</span>
                <span>&bull;</span>
                <span style="font-family:monospace; font-size:11px;">Turno AA &bull; Sala de Despacho G&T Chile</span>
            </div>
            <div style="display:flex; align-items:center; gap:14px; background:#f8fafc; padding:6px 14px; border-radius:10px; border:1px solid #e2e8f0;">
                <div style="display:flex; gap:6px; font-size:14px; padding-right:10px; border-right:1px solid #cbd5e1;">
                    <span title="Solar">☀️</span>
                    <span title="Eólica">💨</span>
                    <span title="BESS">🔋</span>
                </div>
                <div style="font-weight:600; font-size:12px; color:#334155;">
                    <strong style="color:#0f172a;">By Michael NB - &gamma;</strong>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ======================================================================================
# EJECUCIÓN AUTÓNOMA PARA PRUEBAS (STREAMLIT STANDALONE)
# ======================================================================================
if __name__ == "__main__":
    st.set_page_config(
        page_title="Ayuda Memoria & Unilineales - SSEE ERNC",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    render_ayuda_memoria()
