import io

# 1. Fix home.html
with io.open(r'frontend\home.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the language options and label
html = html.replace('<label> Language:</label>', '<label>🌐 Language:</label>')
html = html.replace('<label>??? Language:</label>', '<label>🌐 Language:</label>')
html = html.replace('<option value=\"en\"> English</option>', '<option value=\"en\">🇬🇧 English</option>')
html = html.replace('<option value=\"hi\"> (Hindi)</option>', '<option value=\"hi\">🇮🇳 हिन्दी (Hindi)</option>')
html = html.replace('<option value=\"gu\"> (Gujarati)</option>', '<option value=\"gu\">🇮🇳 ગુજરાતી (Gujarati)</option>')
html = html.replace('<option value=\"mr\"> (Marathi)</option>', '<option value=\"mr\">🇮🇳 मराठी (Marathi)</option>')
html = html.replace('<option value=\"pa\"> (Punjabi)</option>', '<option value=\"pa\">🇮🇳 ਪੰਜਾਬੀ (Punjabi)</option>')
html = html.replace('<option value=\"ta\"> (Tamil)</option>', '<option value=\"ta\">🇮🇳 தமிழ் (Tamil)</option>')
html = html.replace('<option value=\"te\"> (Telugu)</option>', '<option value=\"te\">🇮🇳 తెలుగు (Telugu)</option>')
html = html.replace('<option value=\"bn\"> (Bengali)</option>', '<option value=\"bn\">🇮🇳 বাংলা (Bengali)</option>')
html = html.replace('<option value=\"kn\"> (Kannada)</option>', '<option value=\"kn\">🇮🇳 ಕನ್ನಡ (Kannada)</option>')
html = html.replace('<option value=\"ml\"> (Malayalam)</option>', '<option value=\"ml\">🇮🇳 മലയാളം (Malayalam)</option>')
html = html.replace('<option value=\"or\"> (Odia)</option>', '<option value=\"or\">🇮🇳 ଓଡ଼ିଆ (Odia)</option>')
html = html.replace('<option value=\"ur\"> (Urdu)</option>', '<option value=\"ur\">🇮🇳 اردو (Urdu)</option>')

with io.open(r'frontend\home.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Fix chat.js
with io.open(r'frontend\js\chat.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Revert spans to actual emojis in JS
replacements = [
    ('<span class=\"material-icons\" style=\"vertical-align: middle; font-size: inherit;\">grass</span>', '🌾'),
    ('<span class=\"material-icons\" style=\"vertical-align: middle; font-size: inherit;\">spa</span>', '🌿'),
    ('<span class=\"material-icons\" style=\"vertical-align: middle; font-size: inherit;\">yard</span>', '🌱'),
    ('<span class=\"material-icons\" style=\"vertical-align: middle; font-size: inherit;\">science</span>', '🧪'),
    ('<span class=\"material-icons\" style=\"vertical-align: middle; font-size: inherit;\">wb_sunny</span>', '☀️'),
    ('<span class=\"material-icons\" style=\"vertical-align: middle; font-size: inherit;\">water_drop</span>', '💧'),
    ('<span class=\"material-icons\" style=\"vertical-align: middle; font-size: inherit;\">pest_control</span>', '🐛'),
    ('<span class=\"material-icons\" style=\"vertical-align: middle; font-size: inherit;\">account_balance</span>', '🏛️'),
    ('<span class=\"material-icons\" style=\"vertical-align: middle; font-size: inherit;\">payments</span>', '💰'),
    ('<span class=\"material-icons\" style=\"vertical-align: middle; font-size: inherit;\">eco</span>', '♻️')
]

for old, new in replacements:
    js = js.replace(old, new)

# Revert the btn textContent change since now we have raw emojis instead of spans!
js = js.replace('btn.innerHTML = `${t.emoji} ${t.label}`;', 'btn.textContent = `${t.emoji} ${t.label}`;')

with io.open(r'frontend\js\chat.js', 'w', encoding='utf-8') as f:
    f.write(js)
print('Fixed successfully!')
