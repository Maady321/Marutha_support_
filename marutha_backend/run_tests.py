import subprocess
import sys

with open('pytest_result.log', 'w', encoding='utf-8') as f:
    subprocess.run([sys.executable, '-m', 'pytest', '-v'], stdout=f, stderr=f)
