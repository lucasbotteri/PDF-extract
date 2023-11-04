import openai

SYSTEM_PROMPT = """
Enviare un texto extraido de una resolucion, tu trabajo sera extrar los datos requeridos de este texto
Esta resolucion explica en alguno de sus articulos que debido a alguna causa, en general asignaciones de roles en el campo de la medicina, se le debe asignar algun pago complementario a esta persona.
Requiero 
- El numero de resolucion
- el nombre de la persona a la que hace referencia el documento
- el numero de legajo de la persona a la que hace referencia el documento
- La fecha en la que se debe aplicar la resolucion

El numero de resolucion se extrae de una seccion del documento que generalmente tiene la forma: `Numero: XXXX` al principio del documento
El nombre se encuentra en los articulos donde explican la causa de la resolucion y a quien se le debe aplicar
Luego se encuentra el numero de legajo, que se encuentra
La fecha se extrae de una seccion que generalmente tiene la forma: `A partir del XXXX`'

El output debe tener el siguiente formato:
nombre_de_la_persona,numero_de_resolucion,numero_de_legajo,fecha_de_aplicacion

Si no se encuentra alguno de los datos, se debe dejar el campo con un string "NA"

"""

SYSTEM_PROMPT_MESSAGE = {"role": "system", "content": SYSTEM_PROMPT}

openai.api_key = ""


def get_csv_from_document_text(document_text: str) -> str:
    document_message = {"role": "user", "content": document_text}

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[SYSTEM_PROMPT_MESSAGE, document_message],
        temperature=0,
        max_tokens=256,
    )
    csvResponse = response["choices"][0]["message"]["content"]

    return csvResponse
