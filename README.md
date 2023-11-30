# Entrega-Final-Compiladores

Este repositorio contiene todas las fases y requisitos que el profesor especificó para la realización del proyecto.

# Analizador Léxico
Instrucción: En esta parte del proyecto, deberán construir un módulo de 
análisis léxico para el lenguaje **PL0**.  Para ello, deberán 
utilizar la herramienta de automatización "Lexer" (SLY).
# Analizador Léxico
En esta parte del proyecto, se construirá un módulo de análisis
sintático para **PL0**. Para ello, se basará en su módulo de
análisis léxico y en el uso de una herramienta adicional de
generación de código de forma automática llamada `sly.Parser`
(un derivado de `bison` en Python--la popular herramienta 
GNU LALR(1) de generadores sintáticos).
# Analizador semántico

1. Nombres y Simbolos:

	Todos los identificadores deben ser definidos antes de que ellos sean usados. Esto incluye variables, constantes y nombres de tipo. Pro ejemplo, esta clase de codigo genera un error:

		fun main()
		begin
			a := 3    /* Error. 'a' no definida.
		end

2. Tipos de literales y constantes

	Todos los símbolos literales se escriben implícitamente y se les debe asignar un tipo de "int" o "float". Este tipo se utiliza para establecer el tipo de constantes. Por ejemplo:

		fun main()
			const a = 42;         // Tipo "int"
			const b = 4.2;        // Tipo "float"
		begin
			skip
		end

3. Comprobar el tipo del operador

	Los operadores binarios sólo operan con operandos de un tipo compatible.
	De lo contrario, obtendrá un error de tipo. Por ejemplo:

		fun main()
			a : int;
			b : float;
			c : int;
			d : int;
			e : int;
		begin
			a := 2;
			b := 3.14;
			c := a + 3;    // OK
			d := a + b;    // Error.  int + float
			e := b + 4.5;  // Error.  int = float
		end

	Además, debe asegurarse de que solo se permitan operadores compatibles.

4.  Asignacion.

	Los lados izquierdo y derecho de una operación de asignación deben declararse como del mismo tipo.

		fun main()
			a : int;
		begin
			a = 4 + 5;     // OK
			a = 4.5;       // Error. int = float
		end

	Los valores sólo se pueden asignar a declaraciones de variables, no a constantes.

		fun main()
			a : int;
			const b = 42;
		begin
			a := 37;        // OK
			b := 37;        // Error. b is const
