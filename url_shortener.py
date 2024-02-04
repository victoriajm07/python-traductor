import pyshorteners
import streamlit as st

def shorted_url(url):
    s = pyshorteners.Shortener()
    shorted_url = s.tinyurl.short(url)
    return shorted_url

st.set_page_config(page_title="URL Shortener", page_icon="/", layout="centered")
st.image