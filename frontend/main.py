import subprocess
from pathlib import Path

ruta_proyecto = Path(__file__).resolve().parent.parent
motor_scheme = ruta_proyecto / "backend" / "motor.scm"

resultado = subprocess.run(
    ["racket", str(motor_scheme)],
    capture_output=True,
    text=True,
    check=True
)

print("Respuest recibida desde Scheme:")
print(resultado.stdout)