import re

AI_ML_KEYWORDS = [
    r'\b(machine learning|ml|deep learning|dl)\b',
    r'\b(artificial intelligence|ai)\b',
    r'\b(natural language processing|nlp)\b',
    r'\b(computer vision|cv)\b',
    r'\b(llm|large language model)\b',
    r'\b(generative ai|genai|gen ai)\b',
    r'\b(gpt|transformer|attention mechanism)\b',
    r'\b(neural network|neural net)\b',
    r'\b(pytorch|tensorflow|keras|jax|scikit-learn)\b',
    r'\b(hugging[-\s]?face|transformers)\b',
    r'\b(langchain|llamaindex)\b',
    r'\b(vector database|embedding|embeddings)\b',
    r'\b(rag|retrieval[-\s]?augmented[-\s]?generation)\b',
    r'\b(fine[-\s]?tuning|fine tune)\b',
    r'\b(rlhf|reinforcement learning)\b',
    r'\b(stable diffusion|diffusion model|gan)\b',
    r'\b(ai agent|autonomous agent|agentic)\b',
    r'\b(mlops|ml pipeline|model deployment|model serving)\b',
    r'\b(data science|data scientist)\b',
    r'\b(recommendation system|recommender)\b',
    r'\b(time series|forecasting|predictive model)\b',
    r'\b(anomaly detection|classification|regression|clustering)\b',
    r'\b(prompt engineer|prompting)\b',
    r'\b(ai infrastructure|ai platform)\b',
    r'\b(ml engineer|machine learning engineer)\b',
    r'\b(data engineer|data pipeline)\b',
    r'\b(ai research|ml research)\b',
    r'\b(ai product|ml product)\b',
    r'\b(statistical modeling|statistical analysis)\b',
    r'\b(AI/ML|AI-ML)\b',
    r'\b(chatbot|conversational ai)\b',
    r'\b(speech recognition|text to speech|tts)\b',
    r'\b(reinforcement learning|deep reinforcement)\b',
    r'\b(graph neural|gnn)\b',
    r'\b(ai safety|alignment)\b',
    r'\b(multimodal|multi[-\s]?modal)\b',
]

BONUS_SCORE = 3  # extra points per AI keyword match

def score_ai_ml_relevance(text: str) -> int:
    if not text:
        return 0
    text_lower = text.lower()
    score = 0
    for pattern in AI_ML_KEYWORDS:
        matches = re.findall(pattern, text_lower)
        score += len(matches) * BONUS_SCORE
    return score

def filter_ai_ml_jobs(df, min_score: int = 3) -> tuple:
    """Filter jobs by AI/ML relevance. Returns (filtered_df, stats_dict)."""
    title_scores = df['Job Title'].apply(
        lambda x: score_ai_ml_relevance(str(x))) if 'Job Title' in df.columns else 0
    desc_scores = df['Description'].apply(
        lambda x: score_ai_ml_relevance(str(x))) if 'Description' in df.columns else 0
    company_scores = df['Company Industry'].apply(
        lambda x: score_ai_ml_relevance(str(x))) if 'Company Industry' in df.columns else 0

    df['AI_Score'] = title_scores + desc_scores + company_scores
    df_filtered = df[df['AI_Score'] >= min_score].copy()
    df_filtered = df_filtered.sort_values('AI_Score', ascending=False)
    df_filtered = df_filtered.drop(columns=['AI_Score'])

    stats = {
        'total_before_filter': len(df),
        'total_after_filter': len(df_filtered),
        'removed': len(df) - len(df_filtered),
        'min_score_used': min_score,
    }
    return df_filtered, stats
