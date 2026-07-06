document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");
  const errorMsg = document.getElementById("errorMsg"); // <p> o <div> para mostrar errores (opcional en tu HTML)
 
  form.addEventListener("submit", async (e) => {
    e.preventDefault(); // Evita que la página se recargue
 
    const username = document.getElementById("username").value.trim();
 
    if (!username) {
      mostrarError("Por favor ingresa tu usuario");
      return;
    }
 
    try {
      const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ username })
      });
 
      const data = await response.json();
 
      if (response.ok) {
        // Login exitoso: guardamos el usuario en sessionStorage
        // para usarlo en el dashboard (ej. mostrar nombre, rol, permisos)
        sessionStorage.setItem("user", JSON.stringify(data.user));
 
        // Redirige al dashboard
        window.location.href = "/dashboard";
      } else {
        // El backend regresó un error (ej. usuario no encontrado)
        mostrarError(data.error || "No se pudo iniciar sesión");
      }
    } catch (err) {
      console.error("Error al conectar con el servidor:", err);
      mostrarError("Error de conexión con el servidor");
    }
  });
 
  function mostrarError(texto) {
    if (errorMsg) {
      errorMsg.textContent = texto;
      errorMsg.style.display = "block";
    } else {
      alert(texto);
    }
  }
});