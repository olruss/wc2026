import matplotlib.pyplot as plt

# Данные
players = ['Олег', 'Алекс']
scores = [80, 71]
colors = ['#2196F3', '#f44336']

# Настройка стиля
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(8, 4))

# Создание горизонтального бар-чарта
bars = ax.barh(players, scores, color=colors, height=0.5)

# Добавление текста со счетом на бары
for bar in bars:
    width = bar.get_width()
    ax.text(width - 5, bar.get_y() + bar.get_height()/2, f'{int(width)}', 
            ha='center', va='center', color='white', fontweight='bold', fontsize=14)

# Убираем рамки
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# Настройка осей
ax.tick_params(axis='both', which='both', length=0)
ax.set_xticks([])
ax.set_yticklabels(players, fontsize=14, fontweight='bold')

plt.title('Битва Прогнозистов: Отрыв 9 очков', fontsize=16, pad=20)
plt.tight_layout()

# Сохранение
plt.savefig('telegram_chart_prototype.png', dpi=300, bbox_inches='tight')
print("График сохранен как telegram_chart_prototype.png")
