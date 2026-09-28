import streamlit as st
import pandas as pd
from statsbombpy import sb

@st.cache_data(ttl=3600)
def load_competitions():
    df_comp = sb.competitions()
    return df_comp

@st.cache_data(ttl=3600)
def load_matches(competition_id, season_id):

    df_matches = sb.matches(competition_id=competition_id, season_id=season_id)
    return df_matches

@st.cache_data(ttl=3600)
def load_events(match_id):
   
    events = sb.events(match_id=match_id)
    return events

def get_match_summary(events):
    
    shots = events[events['type'] == 'Shot'] if 'type' in events.columns else pd.DataFrame()
    passes = events[events['type'] == 'Pass'] if 'type' in events.columns else pd.DataFrame()
    
    total_shots = len(shots)
    total_goals = len(shots[shots['shot_outcome'] == 'Goal']) if not shots.empty and 'shot_outcome' in shots.columns else 0
    total_passes = len(passes)
    successful_passes = len(passes[passes['pass_outcome'].isna()]) if not passes.empty and 'pass_outcome' in passes.columns else 0
    
    return {
        "total_shots": total_shots,
        "total_goals": total_goals,
        "total_passes": total_passes,
        "successful_passes": successful_passes,
        "pass_accuracy": round((successful_passes / total_passes * 100), 1) if total_passes > 0 else 0
    }