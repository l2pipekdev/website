import streamlit as st

# ===== Lista duchow =====
ghosts = {
    "Spirit": {"evidence": {"EMF 5", "Spirit Box", "Ghost Writing"},
               "info": "Brak unikalnych zachowan. Krucyfiks dziala dluzej."},
    "Wraith": {"evidence": {"EMF 5", "Spirit Box", "D.O.T.S"},
               "info": "Nie zostawia sladow w soli. Moze teleportowac sie do gracza."},
    "Phantom": {"evidence": {"Spirit Box", "Fingerprints", "D.O.T.S"},
                "info": "Znika na zdjeciach. Obniza sanity szybciej przy patrzeniu."},
    "Poltergeist": {"evidence": {"Spirit Box", "Fingerprints", "Ghost Writing"},
                    "info": "Rzuca wieloma przedmiotami naraz."},
    "Banshee": {"evidence": {"Fingerprints", "Ghost Orb", "D.O.T.S"},
                "info": "Skupia sie na jednym graczu. Krzyk przez mikrofon paraboliczny."},
    "Jinn": {"evidence": {"EMF 5", "Fingerprints", "Freezing Temps"},
             "info": "Szybszy przy wlaczonym pradzie. Nie wylacza glownego bezpiecznika."},
    "Mare": {"evidence": {"Spirit Box", "Ghost Orb", "Ghost Writing"},
             "info": "Czesciej gasi swiatla. Huntuje czesciej w ciemnosci."},
    "Revenant": {"evidence": {"Ghost Orb", "Ghost Writing", "Freezing Temps"},
                 "info": "Bardzo szybki gdy widzi gracza, wolny gdy nie."},
    "Shade": {"evidence": {"EMF 5", "Ghost Writing", "Freezing Temps"},
              "info": "Malo aktywny. Nie huntuje przy wielu graczach."},
    "Demon": {"evidence": {"Fingerprints", "Ghost Writing", "Freezing Temps"},
              "info": "Moze huntowac wczesnie. Silniejszy wobec krucyfiksu."},
    "Yurei": {"evidence": {"Ghost Orb", "Freezing Temps", "D.O.T.S"},
              "info": "Mocniej obniza sanity. Moze zamknac drzwi calkowicie."},
    "Oni": {"evidence": {"EMF 5", "Freezing Temps", "D.O.T.S"},
            "info": "Czesciej sie pokazuje. Rzuca mocniej przedmiotami."},
    "Hantu": {"evidence": {"Fingerprints", "Ghost Orb", "Freezing Temps"},
              "info": "Szybszy w zimnie, wolniejszy w cieple. Oddycha zimnym powietrzem."},
    "Goryo": {"evidence": {"EMF 5", "Fingerprints", "D.O.T.S"},
              "info": "DOTS widoczne tylko przez kamere i bez gracza w pokoju."},
    "Myling": {"evidence": {"EMF 5", "Fingerprints", "Ghost Writing"},
               "info": "Cichy podczas krokow. Czesciej slychac przez mikrofon paraboliczny."},
    "Onryo": {"evidence": {"Spirit Box", "Ghost Orb", "Freezing Temps"},
              "info": "Moze huntowac po zgaszeniu swieczki. Duch plomieni."},
    "The Twins": {"evidence": {"EMF 5", "Spirit Box", "Freezing Temps"},
                  "info": "Atakuja z dwoch miejsc. Moga miec rozna predkosc."},
    "Raiju": {"evidence": {"EMF 5", "Ghost Orb", "D.O.T.S"},
              "info": "Szybszy przy elektronice. Zakloca sprzet z wiekszej odleglosci."},
    "Obake": {"evidence": {"EMF 5", "Fingerprints", "Ghost Orb"},
              "info": "Rzadkie odciski palcow (6 palcow). Moga szybko znikac."},
    "The Mimic": {"evidence": {"Spirit Box", "Fingerprints", "Freezing Temps", "Ghost Orb"},
                  "info": "Nasladuje inne duchy. Zawsze ma dodatkowo Ghost Orb."},
    "Moroi": {"evidence": {"Spirit Box", "Ghost Writing", "Freezing Temps"},
              "info": "Przyspiesza w hunty. Spirit Box oslabia sanity mocniej."},
    "Deogen": {"evidence": {"Spirit Box", "Ghost Writing", "D.O.T.S"},
               "info": "Bardzo szybki z daleka, ale spowalnia blisko gracza."},
    "Thaye": {"evidence": {"Ghost Orb", "Ghost Writing", "D.O.T.S"},
              "info": "Bardzo aktywny na poczatku, starzeje sie i slabnie."}
}

all_evidence = ["EMF 5", "Spirit Box", "Ghost Writing",
                "Ghost Orb", "Fingerprints", "Freezing Temps", "D.O.T.S"]

# ===== Funkcje =====
def possible_ghosts(found):
    results = []
    for ghost, data in ghosts.items():
        evidence = data["evidence"]
        if found.issubset(evidence):
            missing = evidence - found
            results.append((ghost, missing, data["info"]))
    return results

# ===== Streamlit UI =====
st.set_page_config(page_title="Phasmo Assistant", layout="wide")
st.markdown("<h1 style='text-align:center; color: #4CAF50;'>Phasmo Assistant</h1>", unsafe_allow_html=True)

if "found" not in st.session_state:
    st.session_state.found = set()

st.subheader("Wybierz dowody (kliknij aby wlaczyc/odznaczyc):")

cols = st.columns(len(all_evidence))
for i, ev in enumerate(all_evidence):
    color = "#4CAF50" if ev in st.session_state.found else "#FF3333"  # zielony = wybrane, czerwony = nie wybrane
    if cols[i].button(ev, key=ev):
        if ev in st.session_state.found:
            st.session_state.found.remove(ev)
        else:
            st.session_state.found.add(ev)

found = st.session_state.found

# Wybrane dowody
st.subheader("Wybrane dowody:")
st.markdown(f"<span style='color:#4CAF50;'>{', '.join(found)}</span>" if found else "<span style='color:#FF3333;'>Brak dowodow</span>", unsafe_allow_html=True)

# Mozliwe duchy
st.subheader("Mozliwe duchy:")
matches = possible_ghosts(found)
if not found:
    for ghost, data in ghosts.items():
        st.markdown(f"<span style='color:#AAAAAA;'>**{ghost}** - {data['info']}</span>", unsafe_allow_html=True)
else:
    if matches:
        for ghost, missing, info in matches:
            color = "#4CAF50" if not missing else "#FFCC00"
            suffix = " ✅" if not missing else ""
            st.markdown(f"<span style='color:{color};'>**{ghost}{suffix}** (brakuje: {', '.join(missing) if missing else 'pelny zestaw'}) - {info}</span>", unsafe_allow_html=True)
        if len(found) == 1:
            suggestions = set()
            for _, missing, _ in matches:
                suggestions |= missing
            if suggestions:
                st.markdown(f"<span style='color:#FF5733; font-weight:bold;'>Nastepne badania: {', '.join(suggestions)}</span>", unsafe_allow_html=True)
    else:
        st.write("Brak pasujacych duchow.")
