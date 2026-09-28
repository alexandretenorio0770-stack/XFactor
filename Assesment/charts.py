import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from mplsoccer import Pitch, VerticalPitch

def plot_pass_map(events, player_name=None):
    """Gera mapa de passes utilizando mplsoccer."""
    passes = events[events['type'] == 'Pass'].copy()
    
    if player_name:
        passes = passes[passes['player'] == player_name]
        
    if passes.empty:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, "Nenhum passe encontrado", ha='center', va='center')
        return fig

    # Separar coordenadas X, Y de início e fim
    passes[['location_x', 'location_y']] = pd.DataFrame(passes['location'].tolist(), index=passes.index)
    passes[['pass_end_x', 'pass_end_y']] = pd.DataFrame(passes['pass_end_location'].tolist(), index=passes.index)
    
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(10, 7))
    
    # Separar passes certos e errados
    complete = passes[passes['pass_outcome'].isna()]
    incomplete = passes[passes['pass_outcome'].notna()]
    
    # Desenhar linhas de passe
    pitch.arrows(complete.location_x, complete.location_y,
                 complete.pass_end_x, complete.pass_end_y,
                 color='#56ae6c', ax=ax, width=2, headwidth=3, label='Completo')
    
    pitch.arrows(incomplete.location_x, incomplete.location_y,
                 incomplete.pass_end_x, incomplete.pass_end_y,
                 color='#e74c3c', ax=ax, width=2, headwidth=3, label='Incompleto')
    
    ax.legend(facecolor='#22312b', edgecolor='none', labelcolor='white', loc='upper left')
    title = f"Mapa de Passes - {player_name}" if player_name else "Mapa de Passes da Partida"
    ax.set_title(title, fontsize=14, color='white')
    
    return fig


def plot_shot_map(events):
    """Gera mapa de chutes utilizando mplsoccer."""
    shots = events[events['type'] == 'Shot'].copy()
    
    if shots.empty:
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.text(0.5, 0.5, "Nenhum chute registrado", ha='center', va='center')
        return fig

    shots[['location_x', 'location_y']] = pd.DataFrame(shots['location'].tolist(), index=shots.index)
    
    pitch = VerticalPitch(pitch_type='statsbomb', half=True, pitch_color='#22312b', line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(8, 6))
    
    goals = shots[shots['shot_outcome'] == 'Goal']
    non_goals = shots[shots['shot_outcome'] != 'Goal']
    
    # Chutes normais
    pitch.scatter(non_goals.location_x, non_goals.location_y,
                  s=(non_goals['shot_statsbomb_xg'] * 500) + 50,
                  color='#3498db', alpha=0.6, edgecolors='white', ax=ax, label='Chute (Tam = xG)')
    
    # Gols
    pitch.scatter(goals.location_x, goals.location_y,
                  s=(goals['shot_statsbomb_xg'] * 500) + 100,
                  color='#e74c3c', alpha=0.9, edgecolors='yellow', marker='*', ax=ax, label='Gol')
    
    ax.legend(facecolor='#22312b', edgecolor='none', labelcolor='white', loc='lower center')
    ax.set_title("Mapa de Chutes (xG vs Gol)", fontsize=14, color='white')
    
    return fig


def plot_pass_heatmap(events):
    
    passes = events[events['type'] == 'Pass'].copy()
    passes[['location_x', 'location_y']] = pd.DataFrame(passes['location'].tolist(), index=passes.index)
    
    pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#101010', line_color='#444444')
    fig, ax = pitch.draw(figsize=(10, 7))
    
    kde = pitch.kdeplot(passes.location_x, passes.location_y, ax=ax,
                        fill=True, levels=100, thresh=0, cmap='hot', alpha=0.7)
    
    ax.set_title("Heatmap de Distribuição de Passes", fontsize=14, color='white')
    return fig