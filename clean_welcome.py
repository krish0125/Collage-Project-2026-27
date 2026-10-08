import io
import re

# 1. Remove the span tag from app.js chatWelcomeMessages
with io.open(r'frontend\js\app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Replace the specific span with empty string
app_js = app_js.replace('<span class=\\"material-icons\\" style=\\"vertical-align: middle; font-size: inherit;\\">grass</span>', '')

with io.open(r'frontend\js\app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

# 2. Fix the welcome message in home.html (remove the emoji at the end)
with io.open(r'frontend\home.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('<p>Hello! I am your Kisan AI assistant. Ask me about crops, fertilizers, or weather! &#127793;</p>', '<p>Hello! I am your Kisan AI assistant. Ask me about crops, fertilizers, or weather!</p>')
html = html.replace('<p>Hello! I am your Kisan AI assistant. Ask me about crops, fertilizers, or weather! ??</p>', '<p>Hello! I am your Kisan AI assistant. Ask me about crops, fertilizers, or weather!</p>')

with io.open(r'frontend\home.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('app.js and home.html cleaned successfully!')
