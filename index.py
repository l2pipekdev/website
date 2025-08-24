import streamlit as st
import streamlit.components.v1 as components

# ===== Lista duchow z predkoscia =====
ghosts = {
    "Spirit": {"evidence": {"EMF 5", "Spirit Box", "Ghost Writing"},
               "info": "Brak unikalnych zachowan. Krucyfiks dziala dluzej.", "speed":"Normalna"},
    "Wraith": {"evidence": {"EMF 5", "Spirit Box", "D.O.T.S"},
               "info": "Nie zostawia sladow w soli. Moze teleportowac sie do gracza.", "speed":"Szybka"},
    "Phantom": {"evidence": {"Spirit Box", "Fingerprints", "D.O.T.S"},
                "info": "Znika na zdjeciach. Obniza sanity szybciej przy patrzeniu.", "speed":"Srednia"},
    "Poltergeist": {"evidence": {"Spirit Box", "Fingerprints", "Ghost Writing"},
                    "info": "Rzuca wieloma przedmiotami naraz.", "speed":"Normalna"},
    "Banshee": {"evidence": {"Fingerprints", "Ghost Orb", "D.O.T.S"},
                "info": "Skupia sie na jednym graczu. Krzyk przez mikrofon paraboliczny.", "speed":"Srednia"},
    "Jinn": {"evidence": {"EMF 5", "Fingerprints", "Freezing Temps"},
             "info": "Szybszy przy wlaczonym pradzie. Nie wylacza glownego bezpiecznika.", "speed":"Szybka"},
    "Mare": {"evidence": {"Spirit Box", "Ghost Orb", "Ghost Writing"},
             "info": "Czesciej gasi swiatla. Huntuje czesciej w ciemnosci.", "speed":"Normalna"},
    "Revenant": {"evidence": {"Ghost Orb", "Ghost Writing", "Freezing Temps"},
                 "info": "Bardzo szybki gdy widzi gracza, wolny gdy nie.", "speed":"Szybka"},
    "Shade": {"evidence": {"EMF 5", "Ghost Writing", "Freezing Temps"},
              "info": "Malo aktywny. Nie huntuje przy wielu graczach.", "speed":"Wolna"},
    "Demon": {"evidence": {"Fingerprints", "Ghost Writing", "Freezing Temps"},
              "info": "Moze huntowac wczesnie. Silniejszy wobec krucyfiksu.", "speed":"Normalna"},
    "Yurei": {"evidence": {"Ghost Orb", "Freezing Temps", "D.O.T.S"},
              "info": "Mocniej obniza sanity. Moze zamknac drzwi calkowicie.", "speed":"Srednia"},
    "Oni": {"evidence": {"EMF 5", "Freezing Temps", "D.O.T.S"},
            "info": "Czesciej sie pokazuje. Rzuca mocniej przedmiotami.", "speed":"Szybka"},
    "Hantu": {"evidence": {"Fingerprints", "Ghost Orb", "Freezing Temps"},
              "info": "Szybszy w zimnie, wolniejszy w cieple. Oddycha zimnym powietrzem.", "speed":"Normalna"},
    "Goryo": {"evidence": {"EMF 5", "Fingerprints", "D.O.T.S"},
              "info": "DOTS widoczne tylko przez kamere i bez gracza w pokoju.", "speed":"Szybka"},
    "Myling": {"evidence": {"EMF 5", "Fingerprints", "Ghost Writing"},
               "info": "Cichy podczas krokow. Czesciej slychac przez mikrofon paraboliczny.", "speed":"Normalna"},
    "Onryo": {"evidence": {"Spirit Box", "Ghost Orb", "Freezing Temps"},
              "info": "Moze huntowac po zgaszeniu swieczki. Duch plomieni.", "speed":"Normalna"},
    "The Twins": {"evidence": {"EMF 5", "Spirit Box", "Freezing Temps"},
                  "info": "Atakuja z dwoch miejsc. Moga miec rozna predkosc.", "speed":"Srednia"},
    "Raiju": {"evidence": {"EMF 5", "Ghost Orb", "D.O.T.S"},
              "info": "Szybszy przy elektronice. Zakloca sprzet z wiekszej odleglosci.", "speed":"Szybka"},
    "Obake": {"evidence": {"EMF 5", "Fingerprints", "Ghost Orb"},
              "info": "Rzadkie odciski palcow (6 palcow). Moga szybko znikac.", "speed":"Srednia"},
    "The Mimic": {"evidence": {"Spirit Box", "Fingerprints", "Freezing Temps", "Ghost Orb"},
                  "info": "Nasladuje inne duchy. Zawsze ma dodatkowo Ghost Orb.", "speed":"Zmienna"},
    "Moroi": {"evidence": {"Spirit Box", "Ghost Writing", "Freezing Temps"},
              "info": "Przyspiesza w hunty. Spirit Box oslabia sanity mocniej.", "speed":"Normalna"},
    "Deogen": {"evidence": {"Spirit Box", "Ghost Writing", "D.O.T.S"},
               "info": "Bardzo szybki z daleka, ale spowalnia blisko gracza.", "speed":"Szybka"},
    "Thaye": {"evidence": {"Ghost Orb", "Ghost Writing", "D.O.T.S"},
              "info": "Bardzo aktywny na poczatku, starzeje sie i slabnie.", "speed":"Normalna"}
}

all_evidence = ["EMF 5", "Spirit Box", "Ghost Writing",
                "Ghost Orb", "Fingerprints", "Freezing Temps", "D.O.T.S"]

# ===== Funkcja do wyliczania mozliwych duchow =====
def possible_ghosts(found):
    results = []
    for ghost, data in ghosts.items():
        evidence = data["evidence"]
        if found.issubset(evidence):
            missing = evidence - found
            results.append((ghost, missing, data["info"], data.get("speed","Nieznana")))
    return results

# ===== Streamlit UI =====
st.set_page_config(page_title="Phasmo Assistant", layout="wide")
st.markdown("<h1 style='text-align:center; color: #4CAF50;'>Phasmo Assistant</h1>", unsafe_allow_html=True)

if "found" not in st.session_state:
    st.session_state.found = set()

st.subheader("Wybierz dowody (max 3):")
warning = False
for ev in all_evidence:
    checked = ev in st.session_state.found
    new_state = st.checkbox(ev, value=checked)
    if new_state and ev not in st.session_state.found:
        if len(st.session_state.found) < 3:
            st.session_state.found.add(ev)
        else:
            warning = True
    elif not new_state and ev in st.session_state.found:
        st.session_state.found.discard(ev)

if warning:
    st.warning("Max 3 dowody! Nie mozna dodac wiecej.")

found = st.session_state.found

# Wybrane dowody
st.subheader("Wybrane dowody:")
st.markdown(
    f"<span style='color:#4CAF50;'>{', '.join(found)}</span>" if found else
    "<span style='color:#FF3333;'>Brak dowodow</span>",
    unsafe_allow_html=True
)

# Mozliwe duchy
st.subheader("Mozliwe duchy:")
matches = possible_ghosts(found)

if not found:
    for ghost, data in ghosts.items():
        st.markdown(f"<span style='color:#AAAAAA;'>**{ghost}** - {data['info']} (Predkosc: {data['speed']})</span>", unsafe_allow_html=True)
else:
    if matches:
        for ghost, missing, info, speed in matches:
            color = "#4CAF50" if not missing else "#FFCC00"
            suffix = " ✅" if not missing else ""
            st.markdown(f"<span style='color:{color};'>**{ghost}{suffix}** "
                        f"(brakuje: {', '.join(missing) if missing else 'pelny zestaw'}, Predkosc: {speed}) - {info}</span>",
                        unsafe_allow_html=True)
        if len(found) == 1:
            suggestions = set()
            for _, missing, _, _ in matches:
                suggestions |= missing
            if suggestions:
                st.markdown(f"<span style='color:#FF5733; font-weight:bold;'>Nastepne badania: {', '.join(suggestions)}</span>", unsafe_allow_html=True)
    else:
        st.write("Brak pasujacych duchow.")

# ================== AdSense ==================
st.subheader("Reklama")
components.html("""
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5967954940151736"
    crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-client="ca-pub-5967954940151736"
     data-ad-slot="1234567890"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
""", height=90)
