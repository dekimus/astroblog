// --- Fondo de estrellas ---
const canvas = document.getElementById("starfield");
const ctx = canvas.getContext("2d");

let width, height, stars;
let mouseX = 0, mouseY = 0;

function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    generarEstrellas();
}

function generarEstrellas() {
    const cantidad = Math.floor((width * height) / 6000); // densidad según tamaño de pantalla
    stars = [];
    for (let i = 0; i < cantidad; i++) {
        stars.push({
            x: Math.random() * width,
            y: Math.random() * height,
            radius: Math.random() * 1.4 + 0.3,
            depth: Math.random() * 0.6 + 0.2,       // 0.2 (lejana) a 0.8 (cercana)
            phase: Math.random() * Math.PI * 2,      // punto de partida del titileo
            speed: Math.random() * 0.015 + 0.005,    // velocidad de titileo
        });
    }
}

function dibujar(tiempo) {
    ctx.clearRect(0, 0, width, height);

    for (const star of stars) {
        const parallaxX = (mouseX - width / 2) * star.depth * 0.02;
        const parallaxY = (mouseY - height / 2) * star.depth * 0.02;

        const titileo = Math.sin(tiempo * star.speed + star.phase) * 0.5 + 0.5;
        const alpha = 0.3 + titileo * 0.7;

        ctx.beginPath();
        ctx.arc(star.x + parallaxX, star.y + parallaxY, star.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(232, 236, 245, ${alpha})`;
        ctx.fill();
    }

    requestAnimationFrame(dibujar);
}

window.addEventListener("resize", resize);
window.addEventListener("mousemove", (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
});

resize();
requestAnimationFrame(dibujar);
// --- Animación de scroll en la galería ---
const observador = new IntersectionObserver(
    (entradas) => {
        entradas.forEach((entrada) => {
            if (entrada.isIntersecting) {
                entrada.target.classList.add("visible");
                observador.unobserve(entrada.target); // ya no hace falta seguir observando
            }
        });
    },
    { threshold: 0.15 } // se activa cuando el 15% del elemento es visible
);

document.querySelectorAll(".gallery-item").forEach((item, indice) => {
    item.style.transitionDelay = `${indice * 60}ms`;
    observador.observe(item);
});

// --- Lightbox de foto ---
const trigger = document.querySelector(".photo-full-trigger");
const lightbox = document.getElementById("lightbox");

if (trigger && lightbox) {
    trigger.addEventListener("click", () => {
        lightbox.classList.add("open");
        document.body.style.overflow = "hidden"; // evita el scroll de fondo mientras está abierto
    });

    lightbox.addEventListener("click", () => {
        lightbox.classList.remove("open");
        document.body.style.overflow = "";
    });

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && lightbox.classList.contains("open")) {
            lightbox.classList.remove("open");
            document.body.style.overflow = "";
        }
    });
}