// ==================================================
// Layout Loader
// ==================================================
export async function loadLayout(pageContentId) {
    const layoutContainer = document.getElementById("layout");
    if (!layoutContainer) return;

    const response = await fetch("/templates/layout.html");
    const html = await response.text();
    layoutContainer.innerHTML = html;

    const contentSlot = document.getElementById("content");
    const pageContent = document.getElementById(pageContentId);

    if (contentSlot && pageContent) {
        contentSlot.appendChild(pageContent);
        pageContent.style.display = "block";
    }

    showFlash();
    await renderAuthNav();

}


// ==================================================
// Flash Messages
// ==================================================
export function setFlash(message, type = "success") {
    sessionStorage.setItem("flash", JSON.stringify({ message, type }));
}

export function showFlash() {
    const data = sessionStorage.getItem("flash");
    if (!data) return;

    const { message, type } = JSON.parse(data);
    const container = document.getElementById("flash-container");
    if (!container) return;

    container.innerHTML = `
        <div class="alert alert-${type} fade show d-flex align-items-center" role="alert">
            <span>${message}</span>
            <button
                type="button"
                class="btn-close ms-auto"
                aria-label="Close">
            </button>
        </div>
    `;

    const alert = container.querySelector(".alert");
    const closeBtn = container.querySelector(".btn-close");

    closeBtn.addEventListener("click", () => {
        alert.classList.remove("show");
        setTimeout(() => alert.remove(), 150);
    });

    setTimeout(() => {
        if (alert) {
            alert.classList.remove("show");
            setTimeout(() => alert.remove(), 150);
        }
    }, 3000);

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
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) throw new Error("Auth failed");

        const user = await response.json();
        localStorage.setItem("user_id", user.uid);

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

    } catch (error) {
        console.error("Auth nav error:", error);
        localStorage.removeItem("access_token");

        authNav.innerHTML = `
            <a class="nav-link" href="/login.html">Login</a>
        `;
    }
}


