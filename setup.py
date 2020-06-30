import cx_Freeze
executables = [cx_Freeze.Executable("Riverfand2.py")]
# Mude o nome teste-1.py para o nome do
# seu arquivo python do jogo
cx_Freeze.setup(
 name="RIVERFAND", # Voce pode colocar
 # outro nome para
# seu jogo
 options={"build_exe": {"packages": ["pygame"],
 "include_files": ["src/"
 # Nome do arquivo ou arquivos
# de imagens, sons, etc,
 # separados por virgula
 # Exemplo "racecar.png"
 ]}},
 executables=executables
)
