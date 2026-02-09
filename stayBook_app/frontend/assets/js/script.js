// ==================================================
// Layout Loader
// ==================================================
export async function loadLayout(pageContentId) {
    const layoutContainer = document.getElementById("layout");
    if (!layoutContainer) return;

    const response = await fetch("/templates/layout.html");
    const html = await response.text();

    layoutContainer.innerHTML = html;

    const pageContainer = document.getElementById("page-container");
    const pageContent = document.getElementById(pageContentId);

    if (pageContainer && pageContent) {
        pageContainer.appendChild(pageContent);
        pageContent.style.display = "block";
    }

    // Show flash AFTER layout is painted
    requestAnimationFrame(() => {
        showFlash();
    });

    await renderAuthNav();
}


// ==================================================
// Flash Messages
// ==================================================
export function setFlash(message, type = "success") {
    sessionStorage.setItem(
        "flash",
        JSON.stringify({ message, type })
    );
}

export function showFlash() {
    const data = sessionStorage.getItem("flash");
    if (!data) return;

    const container = document.getElementById("flash-container");
    if (!container) return;

    const { message, type } = JSON.parse(data);

    container.innerHTML = `
        <div class="alert alert-${type} alert-dismissible show" role="alert">
            ${message}
            <button type="button" class="btn-close" aria-label="Close"></button>
        </div>
    `;

    const alert = container.querySelector(".alert");
    const closeBtn = container.querySelector(".btn-close");

    closeBtn.onclick = () => alert.remove();

    setTimeout(() => {
        if (alert) alert.remove();
    }, 4500);

    sessionStorage.removeItem("flash");
}


// ==================================================
// AUTH NAV RENDER
// ==================================================
async function renderAuthNav() {
    const authNav = document.getElementById("auth-nav");
    if (!authNav) return;

    const token = localStorage.getItem("access_token");
    authNav.innerHTML = "";

    if (!token) {
        authNav.innerHTML = `
            <button class="btn btn-sm btn-outline-dark ms-2 btn-add">
                <a class="nav-link" href="/new_listing.html">Add your home</a>
            </button>
            <b><a class="nav-link" href="/signup.html">Sign Up</a></b>
            <b><a class="nav-link" href="/login.html">Login</a></b>
        `;
        return;
    }

    try {
        const response = await fetch("/auth/me", {
            headers: { Authorization: `Bearer ${token}` }
        });

        if (!response.ok) throw new Error();

        const user = await response.json();

        authNav.innerHTML = `
            <button class="btn btn-sm btn-outline-dark ms-2 btn-add">
                <a class="nav-link" href="/new_listing.html">Add your home</a>
            </button>
            <span class="nav-link fw-semibold">
                <i class="fa-solid fa-user"></i> ${user.username}
            </span>
            <button class="btn btn-sm btn-outline-dark ms-2" id="logout-btn">
                Logout
            </button>
        `;

        document.getElementById("logout-btn").onclick = () => {
            localStorage.clear();
            setFlash("Logged out successfully.", "info");
            window.location.href = "/";
        };

    } catch {
        localStorage.removeItem("access_token");
    }
}
