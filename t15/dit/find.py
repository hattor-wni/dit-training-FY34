from pathlib import Path

cwd = Path.cwd()

for p in cwd.glob('*.txt'):
    print(p.name)

exists = Path('てすと.txt').exists()
print(f'てすと.txt: {exists}')

exists = Path('data.txt').exists()
print(f'data.txt: {exists}')

exists = Path('データ.txt').exists()
print(f'データ.txt: {exists}')
