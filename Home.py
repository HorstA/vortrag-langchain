import streamlit as st

st.set_page_config(
  page_title="LangChain-Vortrag",
  page_icon="🤖"
)

st.markdown(f"### Wilkommen in der KI-Werkstatt!")
st.markdown("Bitte wähle eine Funktion in der rechten Seitenleiste.")
st.info(
    "We love data. And we are German programmer. So we respect your data."
)
st.divider()
st.markdown("**Impressum:** [Impressum](https://www.ki-werkstatt.net/impressum/)")
st.markdown(
    "<sup><sub>made by [KI-Werkstatt](https://www.ki-werkstatt.net), [Horst Amper](mailto:horst.amper@ki-werkstatt.net), September 2023.</sub></sup>",
    unsafe_allow_html=True,
)
