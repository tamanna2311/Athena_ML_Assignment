import streamlit as st
import os
import tempfile
from main import analyze_pitch

st.set_page_config(page_title="Shark Tank Pitch Analyzer", page_icon="🦈", layout="wide")

st.title("🦈 Shark Tank Pitch Analyzer")
st.markdown("### Upload your pitch and face the AI Sharks!")

# Sidebar for API Key (optional override)
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Google API Key (Optional)", type="password")
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
    
    st.info("This tool analyzes your vocal tone and business content to give you feedback from virtual investors.")

uploaded_file = st.file_uploader("Upload Video or Audio", type=['mp4', 'mov', 'wav', 'mp3'])

if uploaded_file is not None:
    # Save to temp file
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1])
    tfile.write(uploaded_file.read())
    tfile.close()
    
    st.audio(uploaded_file)
    
    if st.button("Analyze Pitch 🚀"):
        with st.spinner("The Sharks are listening... (Processing Audio & Content)"):
            try:
                results = analyze_pitch(tfile.name)
                
                # --- Display Results ---
                
                # 1. High Level Scores
                st.divider()
                st.subheader("📊 Pitch Scorecard")
                col1, col2, col3 = st.columns(3)
                
                tone_score = results['tone_metrics'].get('delivery_score', 0)
                content_score = results['content_metrics'].get('overall_viability_score', 0)
                
                col1.metric("🎙️ Delivery Score", f"{tone_score:.1f}/100")
                col2.metric("📈 Business Viability", f"{content_score}/100")
                col3.metric("🏆 Final Verdict", results['shark_feedback'].get('final_verdict', 'Pending'))
                
                # 2. Detailed Breakdown
                st.divider()
                tab1, tab2, tab3 = st.tabs(["🗣️ Vocal Analysis", "📝 Business Content", "🦈 Shark Feedback"])
                
                with tab1:
                    st.markdown("#### 🗣️ Vocal Delivery Metrics")
                    t_metrics = results['tone_metrics']
                    labels = t_metrics.get('labels', {})
                    
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Pitch Variation", f"{t_metrics.get('pitch_variation', 0):.1f} Hz", labels.get('pitch', ''))
                    c2.metric("Pace", f"{t_metrics.get('estimated_tempo', 0):.0f} BPM", labels.get('pace', ''))
                    c3.metric("Pause Ratio", f"{t_metrics.get('pause_ratio', 0):.1%}", labels.get('pause', ''))
                    
                    # --- NEW: AI Vibe Check ---
                    ai_data = t_metrics.get('ai_analysis', {})
                    if ai_data:
                        st.divider()
                        st.markdown("#### 🧠 AI Vibe Check")
                        v_col1, v_col2 = st.columns(2)
                        v_col1.info(f"**Detected Emotion:** {ai_data.get('emotion', 'Analyzing...')}")
                        v_col2.success(f"**Vocal Confidence:** {ai_data.get('confidence', 'Analyzing...')}")
                        
                        if ai_data.get('tip'):
                            st.warning(f"💡 **Coaching Tip:** {ai_data.get('tip')}")
                    # --------------------------

                with tab2:
                    st.markdown("#### Content Analysis")
                    c_metrics = results['content_metrics']
                    scores = c_metrics.get('scores', {})
                    
                    # --- NEW: Radar Chart ---
                    import plotly.graph_objects as go
                    
                    categories = ['Problem Clarity', 'Product Differentiation', 'Business Model', 'Market Opportunity', 'Competition Awareness']
                    values = [
                        scores.get('problem_clarity', 0),
                        scores.get('product_differentiation', 0),
                        scores.get('business_model', 0),
                        scores.get('market_opportunity', 0),
                        scores.get('competition_awareness', 0)
                    ]
                    
                    fig = go.Figure(data=go.Scatterpolar(
                        r=values,
                        theta=categories,
                        fill='toself',
                        name='Pitch Profile'
                    ))
                    fig.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                        showlegend=False,
                        margin=dict(l=40, r=40, t=20, b=20)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    # ------------------------
                    
                    # --- NEW: Filler Word Analysis ---
                    filler_data = c_metrics.get('filler_analysis', {})
                    if filler_data:
                        st.markdown("#### 🗣️ Speech Cleanliness")
                        f_col1, f_col2 = st.columns(2)
                        f_col1.metric("Filler Words Detected", filler_data.get('total_count', 0))
                        f_col2.metric("Cleanliness Score", f"{filler_data.get('cleanliness_score', 100)}/100")
                        
                        if filler_data.get('total_count', 0) > 0:
                            st.caption(f"Detected: {', '.join([f'{k} ({v})' for k,v in filler_data.get('breakdown', {}).items()])}")
                    # ---------------------------------

                    st.markdown("#### Pitch Structure Detected")
                    structure = c_metrics.get('structure', {})
                    s_cols = st.columns(4)
                    s_cols[0].checkbox("Hook", value=structure.get('hook', False), disabled=True)
                    s_cols[1].checkbox("Problem", value=structure.get('problem', False), disabled=True)
                    s_cols[2].checkbox("Solution", value=structure.get('solution', False), disabled=True)
                    s_cols[3].checkbox("Ask", value=structure.get('ask', False), disabled=True)
                    
                    with st.expander("View Transcript"):
                        st.text(results['transcript'])

                with tab3:
                    st.markdown("#### The Shark Panel")
                    sharks = results['shark_feedback'].get('sharks', [])
                    
                    report_text = f"SHARK TANK PITCH ANALYZER REPORT\n\n"
                    report_text += f"Final Verdict: {results['shark_feedback'].get('final_verdict', 'N/A')}\n"
                    report_text += f"Delivery Score: {tone_score:.1f}/100\n"
                    report_text += f"Business Score: {content_score}/100\n\n"
                    
                    for shark in sharks:
                        with st.chat_message("user", avatar="🦈"):
                            st.write(f"**{shark['name']}**")
                            st.write(f"_{shark['feedback']}_")
                            if shark['decision'] == "Invest":
                                st.success(f"Decision: {shark['decision']}")
                            else:
                                st.error(f"Decision: {shark['decision']}")
                        
                        report_text += f"{shark['name']}:\n{shark['feedback']}\nDecision: {shark['decision']}\n\n"
                    
                    st.markdown("### Final Summary")
                    summary = results['shark_feedback'].get('summary_reason', '')
                    st.write(summary)
                    report_text += f"SUMMARY:\n{summary}\n"
                    
                    # --- NEW: Download Button ---
                    st.download_button(
                        label="📄 Download Full Report",
                        data=report_text,
                        file_name="shark_tank_report.txt",
                        mime="text/plain"
                    )
                    # ----------------------------

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.exception(e)
            finally:
                os.unlink(tfile.name)
