"""
ui/components.py
----------------
Small reusable rendering helpers so page modules stay declarative.
"""

from __future__ import annotations

import streamlit as st
from ui.theme import PALETTE


def hero(title: str, subtitle: str, badge: str = "NEUROSCIENCE • SIGNAL PROCESSING"):
    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-badge">{badge}</div>
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_card(icon: str, title: str, desc: str):
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def glass_card_open():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)


def glass_card_close():
    st.markdown("</div>", unsafe_allow_html=True)


def stat_pill(value: str, label: str):
    st.markdown(
        f"""
        <div class="stat-pill">
            <div class="stat-value">{value}</div>
            <div class="stat-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def band_badge(band_name: str, color: str):
    st.markdown(
        f'<span class="band-badge" style="background:{color};">{band_name}</span>',
        unsafe_allow_html=True,
    )


def section_label(text: str):
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)


def footer():
    st.markdown(
        '<div class="app-footer">EEG Frequency Band Analyzer &middot; Built with '
        "Streamlit, MNE-Python &amp; Plotly</div>",
        unsafe_allow_html=True,
    )


def no_data_warning(page_name: str = "this page"):
    st.warning(
        f"⚠️ No EEG recording is loaded yet. Go to **📂 Upload EEG** first, "
        f"then come back to {page_name}.",
        icon="⚠️",
    )


def success_toast(message: str):
    st.success(message, icon="✅")


def error_box(message: str, exc: Exception | None = None):
    st.error(message, icon="🚫")
    if exc is not None:
        with st.expander("Show technical error details"):
            st.exception(exc)
