import re

with open('docs/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update Chart style (fill: false, thinner lines)
js = re.sub(r"borderWidth: 3,\s*tension: 0.4,(\s*//.*?)?\s*fill: true,", r"borderWidth: 2,\n                    tension: 0.2,\n                    fill: false,", js)

# 2. Add maxTicksLimit to x axis
x_axis_replacement = r"""x: {
                    grid: {
                        display: false,
                        drawBorder: false
                    },
                    ticks: {
                        color: '#9aa0a6',
                        maxRotation: 45,
                        minRotation: 45,
                        maxTicksLimit: window.innerWidth < 600 ? 10 : 25,
                        font: { family: "'Inter', sans-serif", size: 10 }
                    }
                }"""
js = re.sub(r"x: \{\s*grid: \{.*?(?= \}\s*\}\s*\}\s*\);)", x_axis_replacement, js, flags=re.DOTALL)

with open('docs/app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("app.js updated!")
