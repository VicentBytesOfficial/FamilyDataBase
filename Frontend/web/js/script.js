// Esperamos a que el puente de Python cargue
window.addEventListener("pywebviewready", () => {
    
    const ipInput = document.getElementById('ip-input');
    const btnContinue = document.getElementById('btn-continue');
    const errorMsg = document.getElementById('error-msg');

    async function connect() {
        const ip = ipInput.value.trim();

        if (ip === "") {
            errorMsg.textContent = "[Error 2]: You must enter a valid IPv4 address";
            errorMsg.style.color = "#ff6b6b"; 
            errorMsg.classList.remove('oculto');
        } else {
            // 1. Mostramos el mensaje de "Pensando"
            errorMsg.textContent = "Connecting...";
            errorMsg.style.color = "white";
            errorMsg.classList.remove('oculto');
            
            try {
                // 2. Congelamos la ejecución aquí hasta que Python haga el 'return'
                const res = await window.pywebview.api.login(ip, "admin", "password");
                
                // 3. Evaluamos la respuesta de Python
                if (res.success === true) {
                    // Éxito: Ocultamos el texto de "Connecting..." y lanzamos la alerta
                    errorMsg.classList.add('oculto');
                    alert("¡Éxito! Conectado al servidor.");
                } else {
                    // Fallo: Cambiamos el texto de "Connecting" a rojo y lanzamos alerta
                    errorMsg.textContent = "Fallo la conexión: " + res.message;
                    errorMsg.style.color = "#ff6b6b";
                    alert("Fallo la conexión: " + res.message);
                }
            } catch (error) {
                // Error crítico (ej. el backend se cerró inesperadamente)
                errorMsg.textContent = "Error crítico al comunicarse con Python.";
                errorMsg.style.color = "#ff6b6b";
                alert("Error crítico al comunicarse con Python.");
            }
        }
    }

    btnContinue.addEventListener('click', connect);

    ipInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            connect();
        }
    });
});