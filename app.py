import json
import random
from datetime import datetime
import streamlit as st


# ==========================================
# BACKEND LOGIC (UNTOUCHED)
# ==========================================

def get_playing_team():
    with open("fc.json", "r", encoding="utf-8") as file:
        fc_data = json.load(file)

    countries = fc_data["countries"]
    country_size = len(countries)
    r_country_num = random.randint(0, country_size - 1)
    r_country = countries[r_country_num]

    leagues = r_country["leagues"]
    leagues_size = len(leagues)
    r_league_num = random.randint(0, leagues_size - 1)
    r_league = leagues[r_league_num]

    teams = r_league["teams"]
    teams_size = len(teams)
    r_team_num = random.randint(0, teams_size - 1)
    r_team = teams[r_team_num]

    playing_country = r_country["name"]
    playing_league = r_league["name"]
    playing_team = r_team["name"]

    return f"{playing_country},{playing_league},{playing_team}"


def get_little_playing_team():
    with open("little_played.json", "r", encoding="utf-8") as file:
        little_played = json.load(file)
    little_play_details = get_playing_team()
    details = little_play_details.split(",")
    fetched_team = details[2]
    already_played_teams = []
    for play_detail in little_played:
        team_name = play_detail["teamName"]
        already_played_teams.append(team_name)
    max_tries = 3
    if fetched_team in already_played_teams:
        while max_tries > 0 and fetched_team in already_played_teams:
            max_tries = max_tries - 1
            little_play_details = get_playing_team()
            details = little_play_details.split(",")
            fetched_team = details[2]
    return little_play_details


def get_naman_playing_team():
    with open("naman_played.json", "r", encoding="utf-8") as file:
        little_played = json.load(file)
    little_play_details = get_playing_team()
    details = little_play_details.split(",")
    fetched_team = details[2]
    already_played_teams = []
    for play_detail in little_played:
        team_name = play_detail["teamName"]
        already_played_teams.append(team_name)
    max_tries = 3
    if fetched_team in already_played_teams:
        while max_tries > 0 and fetched_team in already_played_teams:
            max_tries = max_tries - 1
            little_play_details = get_playing_team()
            details = little_play_details.split(",")
            fetched_team = details[2]
    return little_play_details


def get_last_match_number():
    # If in sandbox mode and a simulated counter exists, use the virtual count
    if not st.session_state.get("write_enabled", True) and "virtual_match_count" in st.session_state:
        return st.session_state["virtual_match_count"]

    with open("match_details.json", "r", encoding="utf-8") as file:
        match_details = json.load(file)
    last_match_number = match_details[len(match_details) - 1]["gameCount"]
    return last_match_number


def update_match_details(l_pd, n_pd):
    with open("match_details.json", "r", encoding="utf-8") as file:
        match_details = json.load(file)
    last_match_details = match_details[len(match_details) - 1]
    last_match_count = last_match_details["gameCount"]
    data = {
        "namanTeam": l_pd,
        "littleTeam": n_pd,
        "timeStamp": get_date_time_stamp(),
        "gameCount": last_match_count + 1,
    }
    match_details.append(data)

    with open("match_details.json", "w", encoding="utf-8") as f:
        json.dump(match_details, f, indent=4)


def is_prime(num):
    c = 0
    for i in range(1, num + 1):
        if num % i == 0:
            c = c + 1
    if c == 2:
        return True
    else:
        return False


def is_sum_of_num_prime(num):
    temp = abs(num)
    digit_sum = 0
    while temp > 0:
        digit_sum += temp % 10
        temp //= 10
    return is_prime(digit_sum)


def get_date_time_stamp():
    now = datetime.now()
    formatted_date = now.strftime("%d %b, %Y %H:%M")
    return formatted_date


def get_match_history():
    with open("match_details.json", "r", encoding="utf-8") as file:
        match_details = json.load(file)
    m_history = []
    match_detail_size = len(match_details)
    for match in range(match_detail_size - 1, -1, -1):
        m_history.append(match_details[match])
    return m_history[0:10]


def start_game():
    last_match_num = get_last_match_number()
    is_p = is_prime(last_match_num) or is_sum_of_num_prime(last_match_num)
    if is_p:
        return "it's el classico"

    n_team = get_naman_playing_team()
    n_details_list = n_team.split(",")
    n_country = n_details_list[0]
    n_league = n_details_list[1]
    n_team = n_details_list[2]

    l_team = get_little_playing_team()
    l_details_list = l_team.split(",")
    l_country = l_details_list[0]
    l_league = l_details_list[1]
    l_team = l_details_list[2]

    if n_team == "Al-Nassr FC" or n_team == "Inter Miami CF":
        return "it's battle of gods: naman won"
    elif l_team == "Al-Nassr FC" or l_team == "Inter Miami CF":
        return "it's battle of gods: little won"
    else:
        return f"{n_country},{n_league},{n_team}|{l_country},{l_league},{l_team}"


# ==========================================
# FRONTEND UI & STYLING
# ==========================================

st.set_page_config(
    page_title="FC Arena • Matchmaker",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cabinet+Grotesk:wght@700;800;900&family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .hero-container {
        text-align: center;
        padding: 2.5rem 1rem 1.5rem 1rem;
        background: radial-gradient(circle at center, rgba(34, 197, 94, 0.15) 0%, rgba(15, 23, 42, 0) 70%);
        border-radius: 24px;
        margin-bottom: 2rem;
    }

    .hero-title {
        font-family: 'Cabinet Grotesk', sans-serif;
        font-size: 3rem;
        font-weight: 900;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #4ade80 0%, #38bdf8 50%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .hero-sub {
        font-size: 1.1rem;
        color: #94a3b8;
        font-weight: 500;
    }

    /* Player Cards */
    .player-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 1.8rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .player-card:hover {
        transform: translateY(-4px);
        border-color: rgba(56, 189, 248, 0.4);
    }

    .player-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 1rem;
        margin-bottom: 1.25rem;
    }

    .player-avatar {
        font-size: 2rem;
        background: rgba(255, 255, 255, 0.05);
        padding: 0.4rem 0.6rem;
        border-radius: 12px;
    }

    .player-name {
        font-family: 'Cabinet Grotesk', sans-serif;
        font-size: 1.5rem;
        font-weight: 800;
        color: #f8fafc;
    }

    .team-badge {
        font-size: 1.6rem;
        font-weight: 800;
        color: #38bdf8;
        margin: 0.8rem 0;
        line-height: 1.2;
    }

    .meta-row {
        display: flex;
        align-items: center;
        margin: 0.4rem 0;
        color: #cbd5e1;
        font-size: 0.95rem;
    }

    .meta-label {
        color: #64748b;
        width: 90px;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
    }

    /* Special Banner Cards */
    .special-banner {
        background: linear-gradient(135deg, #f59e0b 0%, #ef4444 100%);
        border-radius: 18px;
        padding: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(239, 68, 68, 0.3);
        margin: 1.5rem 0;
    }

    .special-title {
        font-family: 'Cabinet Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }

    .vs-divider {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        font-family: 'Cabinet Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 900;
        color: #64748b;
    }

    /* History Table Card */
    .history-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.2rem;
        margin-top: 1rem;
    }

    .history-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        background: rgba(30, 41, 59, 0.5);
        border-radius: 10px;
        border-left: 4px solid #38bdf8;
    }

    .history-match-num {
        font-weight: 800;
        color: #94a3b8;
        font-size: 0.85rem;
    }

    .history-teams {
        font-weight: 600;
        color: #f1f5f9;
        font-size: 1rem;
    }

    .history-time {
        color: #64748b;
        font-size: 0.8rem;
    }

    /* Mode Banner */
    .mode-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        margin-bottom: 1rem;
    }

    .mode-prod {
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }

    .mode-sandbox {
        background: rgba(245, 158, 11, 0.15);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    /* Dice Roll Keyframe Animation */
    @keyframes dice-spin {
        0% { transform: rotate(0deg) scale(1); }
        25% { transform: rotate(-90deg) scale(1.15); }
        50% { transform: rotate(180deg) scale(1.25); }
        75% { transform: rotate(270deg) scale(1.15); }
        100% { transform: rotate(360deg) scale(1); }
    }

    @keyframes button-wobble {
        0% { transform: translateY(0); }
        25% { transform: translateY(-4px) rotate(-1deg); }
        50% { transform: translateY(2px) rotate(1.5deg); }
        75% { transform: translateY(-2px) rotate(-1deg); }
        100% { transform: translateY(0) rotate(0deg); }
    }

    /* Button Enhancements & Dynamic Rolling Effects */
    div.stButton > button:first-child {
        width: 100%;
        background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
        color: white;
        font-weight: 800;
        font-size: 1.2rem;
        letter-spacing: 0.03em;
        padding: 0.85rem 2rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 10px 20px -5px rgba(34, 197, 94, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        perspective: 800px;
    }

    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 16px 28px -6px rgba(34, 197, 94, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.4);
    }

    /* Trigger tumble and dice spin on click */
    div.stButton > button:first-child:active {
        animation: button-wobble 0.45s ease-in-out forwards;
        box-shadow: 0 4px 10px rgba(34, 197, 94, 0.4);
    }

    div.stButton > button:first-child:hover p {
        display: inline-block;
        animation: dice-spin 0.65s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Section
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">⚡ FC DERBY ARENA ⚡</div>
        <div class="hero-sub">Automated Match Selector • Prime Derby Engine • Dynamic Fixtures</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Environment / Sandbox Toggle Controls
control_col1, control_col2 = st.columns([3, 1])
with control_col2:
    write_enabled = st.toggle(
        "💾 Production Write Mode",
        value=True,
        key="write_enabled",
        help="Turn ON to log matches to match_details.json (PROD). Turn OFF for suggestion-only Sandbox mode.",
    )

# Sync virtual sandbox counter with actual file when in PROD mode
try:
    with open("match_details.json", "r", encoding="utf-8") as f:
        file_history = json.load(f)
        real_file_count = file_history[-1]["gameCount"] if file_history else 0
except Exception:
    real_file_count = 0

if write_enabled or "virtual_match_count" not in st.session_state:
    st.session_state["virtual_match_count"] = real_file_count

with control_col1:
    if write_enabled:
        st.markdown(
            '<div class="mode-indicator mode-prod">🟢 PROD MODE: Fixtures will be saved to history</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="mode-indicator mode-sandbox">🟡 SANDBOX MODE: Suggestions only (Virtual Match #{st.session_state["virtual_match_count"]})</div>',
            unsafe_allow_html=True,
        )

# Call to Action
col_btn_left, col_btn_center, col_btn_right = st.columns([1, 2, 1])
with col_btn_center:
    spin_trigger = st.button("🎲 ROLL THE FIXTURE 🎲", use_container_width=True)

if spin_trigger:
    try:
        game_details = start_game()

        if game_details == "it's el classico":
            st.balloons()
            if write_enabled:
                update_match_details("Real Madrid", "FC Barca")
                st.toast("⚡ Match saved to history!", icon="💾")
            else:
                st.session_state["virtual_match_count"] += 1
                st.toast("🧪 Sandbox Mode: Result simulated (Not saved to file)", icon="🛡️")

            st.markdown(
                """
                <div class="special-banner">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">👑 🔥 🇪🇸</div>
                    <div class="special-title">EL CLÁSICO SPECIAL!</div>
                    <p style="font-size: 1.1rem; opacity: 0.9; margin-top: 0.5rem;">
                        The gods of football have spoken. <b>Real Madrid</b> takes on <b>FC Barcelona</b> in the ultimate showdown!
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        elif "battle of gods" in game_details:
            st.snow()
            if not write_enabled:
                st.session_state["virtual_match_count"] += 1
            winner = "Naman" if "naman won" in game_details else "Little"
            st.markdown(
                f"""
                <div class="special-banner" style="background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%);">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🐐 ⚡ 🏆</div>
                    <div class="special-title">BATTLE OF THE GODS!</div>
                    <p style="font-size: 1.2rem; font-weight: 700; margin-top: 0.5rem;">
                        Instant Glory: {winner} claims supremacy with legendary selection!
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        else:
            game_detail_list = game_details.split("|")

            naman_game_details = game_detail_list[0]
            naman_country = naman_game_details.split(",")[0]
            naman_league = naman_game_details.split(",")[1]
            naman_team = naman_game_details.split(",")[2]

            little_game_details = game_detail_list[1]
            little_country = little_game_details.split(",")[0]
            little_league = little_game_details.split(",")[1]
            little_team = little_game_details.split(",")[2]

            if write_enabled:
                update_match_details(naman_team, little_team)
                st.toast("⚡ Fixture Locked & Logged!", icon="⚽")
            else:
                st.session_state["virtual_match_count"] += 1
                st.toast("🧪 Sandbox Mode: Fixture generated (Not saved)", icon="🛡️")

            st.write("")
            card_col1, vs_col, card_col2 = st.columns([5, 1, 5])

            with card_col1:
                st.markdown(
                    f"""
                    <div class="player-card">
                        <div class="player-header">
                            <div class="player-avatar">🎮</div>
                            <div>
                                <div class="player-name">LITTLE</div>
                                <div style="font-size: 0.8rem; color: #38bdf8; font-weight: 600;">HOME SIDE</div>
                            </div>
                        </div>
                        <div class="meta-row">
                            <span class="meta-label">Team</span>
                        </div>
                        <div class="team-badge">🛡️ {little_team}</div>
                        <div class="meta-row">
                            <span class="meta-label">League</span>
                            <span>🏆 {little_league}</span>
                        </div>
                        <div class="meta-row">
                            <span class="meta-label">Nation</span>
                            <span>🌍 {little_country}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with vs_col:
                st.markdown('<div class="vs-divider">VS</div>', unsafe_allow_html=True)

            with card_col2:
                st.markdown(
                    f"""
                    <div class="player-card">
                        <div class="player-header">
                            <div class="player-avatar">🕹️</div>
                            <div>
                                <div class="player-name">NAMAN</div>
                                <div style="font-size: 0.8rem; color: #4ade80; font-weight: 600;">AWAY SIDE</div>
                            </div>
                        </div>
                        <div class="meta-row">
                            <span class="meta-label">Team</span>
                        </div>
                        <div class="team-badge" style="color: #4ade80;">🛡️ {naman_team}</div>
                        <div class="meta-row">
                            <span class="meta-label">League</span>
                            <span>🏆 {naman_league}</span>
                        </div>
                        <div class="meta-row">
                            <span class="meta-label">Nation</span>
                            <span>🌍 {naman_country}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    except ValueError:
        st.info("💪 Wildcard Round! You get to freely choose your teams for this match.")

# Match Stats & History Section
try:
    with open("match_details.json", "r", encoding="utf-8") as f:
        history_raw = json.load(f)
        total_games = history_raw[-1]["gameCount"] if history_raw else 0
        last_played = history_raw[-1]["timeStamp"] if history_raw else "N/A"

    st.write("")
    st.markdown("---")
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    with stat_col1:
        st.metric("🔥 Total Fixtures Logged", total_games)
    with stat_col2:
        st.metric("🕒 Last Kickoff Logged", last_played)
    with stat_col3:
        st.metric("⚙️ Storage Engine", "PROD (Writing)" if write_enabled else "SANDBOX (Simulation)")

    # Match History UI (Last 10 Matches)
    with st.expander("📜 View Recent Fixture History (Last 10 Matches)", expanded=False):
        recent_matches = get_match_history()
        if recent_matches:
            for item in recent_matches:
                st.markdown(
                    f"""
                    <div class="history-item">
                        <div>
                            <span class="history-match-num">MATCH #{item.get('gameCount', '-')}</span>
                            <div class="history-teams">🛡️ {item.get('namanTeam', 'N/A')} <span style="color: #64748b;">vs</span> 🛡️ {item.get('littleTeam', 'N/A')}</div>
                        </div>
                        <div class="history-time">📅 {item.get('timeStamp', 'N/A')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.write("No match history recorded yet.")
except Exception:
    pass
