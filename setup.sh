# This script ensures the TextBlob corpora are available on Streamlit Cloud

mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

# Download the TextBlob corpora required for sentiment analysis
python -m textblob.download_corpora
