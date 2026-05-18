import pandas as pd
import matplotlib.pyplot as plt
import os

# Ruta relativa al dataset (desde la raíz del repo)
ruta_datos = 'datos/partidos.csv'
df = pd.read_csv(ruta_datos)

# Calcular puntos por equipo
equipos = set(df['local']).union(set(df['visitante']))
puntos = {eq: 0 for eq in equipos}
goles_favor = {eq: 0 for eq in equipos}
goles_contra = {eq: 0 for eq in equipos}

for _, row in df.iterrows():
    local = row['local']
    visit = row['visitante']
    gl = row['goles_local']
    gv = row['goles_visitante']
    
    goles_favor[local] += gl
    goles_favor[visit] += gv
    goles_contra[local] += gv
    goles_contra[visit] += gl
    
    if gl > gv:
        puntos[local] += 3
    elif gl < gv:
        puntos[visit] += 3
    else:
        puntos[local] += 1
        puntos[visit] += 1

# Tabla de posiciones
tabla = pd.DataFrame({
    'Equipo': list(puntos.keys()),
    'Puntos': list(puntos.values()),
    'GF': [goles_favor[e] for e in puntos.keys()],
    'GC': [goles_contra[e] for e in puntos.keys()]
})
tabla['Diferencia'] = tabla['GF'] - tabla['GC']
tabla = tabla.sort_values('Puntos', ascending=False)

# Guardar tabla en /resultados
tabla.to_csv('resultados/tabla_posiciones.csv', index=False)

# Promedio de goles por partido
total_goles = df['goles_local'].sum() + df['goles_visitante'].sum()
promedio = total_goles / len(df)
print(f"Promedio de goles por partido: {promedio:.2f}")

# Gráfico de barras
plt.figure(figsize=(8,5))
plt.bar(tabla['Equipo'], tabla['Puntos'], color='skyblue')
plt.title('Puntos por equipo')
plt.xlabel('Equipo')
plt.ylabel('Puntos')
plt.savefig('resultados/puntos_equipos.png')
print("Gráfico guardado en /resultados")
