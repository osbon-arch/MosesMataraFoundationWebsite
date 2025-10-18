document.addEventListener("DOMContentLoaded", () => {
  const nav = document.getElementById("mainNav");

  // Navbar scroll effect
// Navbar scroll effect
document.addEventListener("scroll", () => {
  const navbar = document.querySelector("#mainNav");
  if (window.scrollY > 60) {
    navbar.classList.add("scrolled");
  } else {
    navbar.classList.remove("scrolled");
  }
});


  // Stats counters + circle animation
  const circles = document.querySelectorAll(".stat-circle");

  const observerOptions = { threshold: 0.5 };
  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const circle = entry.target;
        circle.classList.add("visible");

        const counter = circle.querySelector(".counter");
        const target = +counter.getAttribute("data-target");
        let count = 0;

        const updateCount = () => {
          const increment = Math.ceil(target / 50); // adjust speed here
          if (count < target) {
            count += increment;
            counter.innerText = count > target ? target : count;
            requestAnimationFrame(updateCount);
          } else {
            counter.innerText = target;
          }
        };

        updateCount();
        observer.unobserve(circle);
      }
    });
  }, observerOptions);

  circles.forEach(circle => observer.observe(circle));
});
// Arc gallery lightbox
document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".arc-card img");
  const lightbox = document.getElementById("arcLightbox");
  const lightboxImg = lightbox.querySelector("img");

  cards.forEach(card => {
    card.addEventListener("click", () => {
      lightboxImg.src = card.src;
      lightbox.classList.add("show");
      document.body.classList.add("modal-open");
    });
  });

  lightbox.addEventListener("click", () => {
    lightbox.classList.remove("show");
    document.body.classList.remove("modal-open");
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".arc-card img");
  const lightbox = document.getElementById("arcLightbox");
  const lightboxImg = lightbox.querySelector("img");

  cards.forEach(card => {
    card.addEventListener("click", () => {
      lightboxImg.src = card.src;
      lightbox.classList.add("show");
      document.body.classList.add("modal-open");
    });
  });

  lightbox.addEventListener("click", () => {
    lightbox.classList.remove("show");
    document.body.classList.remove("modal-open");
  });

  // Disable glide animation on mobile for smoother UX
  if (window.innerWidth < 576) {
    document.querySelector(".arc-gallery").style.animation = "none";
  }
});

// Event gallery lightbox
function openEventGallery(eventId) {
  const lightbox = document.getElementById("eventLightbox");
  const lightboxImages = document.getElementById("lightboxImages");

  // Fetch all event images dynamically
  fetch(`/api/event-images/${eventId}/`)
    .then(res => res.json())
    .then(data => {
      lightboxImages.innerHTML = data.images
        .map(img => `<img src="${img.url}" alt="" />`)
        .join("");
      lightbox.classList.add("show");
    });
}

function closeEventGallery() {
  document.getElementById("eventLightbox").classList.remove("show");
}

document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("eventImageModal");
  const modalContent = document.getElementById("eventImageGrid");
  const closeBtn = document.querySelector(".event-modal-close");
  const sound = document.getElementById("modalSound");

  // Lightbox elements
  const lightbox = document.getElementById("lightboxOverlay");
  const lightboxImg = document.getElementById("lightboxImage");
  const lightboxClose = document.getElementById("lightboxClose");
  const lightboxPrev = document.getElementById("lightboxPrev");
  const lightboxNext = document.getElementById("lightboxNext");

  let currentImages = [];
  let currentIndex = 0;

  // Handle "View Images" click
  document.querySelectorAll(".view-images-btn").forEach(btn => {
    btn.addEventListener("click", async () => {
      const eventId = btn.getAttribute("data-event-id");

      const response = await fetch(`/event-images/${eventId}/`);
      const data = await response.json();
      currentImages = data.images;

      // Populate modal grid
      modalContent.innerHTML = currentImages
        .map((img, index) => `
          <img src="${img.url}" alt="event image" data-index="${index}" class="event-grid-img">
        `)
        .join("");

      // Play sound and show modal
      sound.currentTime = 0;
      sound.play();
      modal.classList.add("show");
      document.body.style.overflow = "hidden";

      // Attach click listeners for grid images
      document.querySelectorAll(".event-grid-img").forEach(img => {
        img.addEventListener("click", (e) => {
          currentIndex = parseInt(e.target.dataset.index);
          openLightbox();
        });
      });
    });
  });

  // Close modal
  closeBtn.addEventListener("click", closeModal);
  modal.addEventListener("click", (e) => {
    if (e.target === modal) closeModal();
  });

  function closeModal() {
    modal.classList.remove("show");
    document.body.style.overflow = "auto";
  }

  // Open fullscreen lightbox
  function openLightbox() {
    lightboxImg.src = currentImages[currentIndex].url;
    lightbox.classList.add("show");
  }

  // Lightbox navigation
  lightboxPrev.addEventListener("click", () => {
    currentIndex = (currentIndex - 1 + currentImages.length) % currentImages.length;
    lightboxImg.src = currentImages[currentIndex].url;
  });

  lightboxNext.addEventListener("click", () => {
    currentIndex = (currentIndex + 1) % currentImages.length;
    lightboxImg.src = currentImages[currentIndex].url;
  });

  // Close lightbox
  lightboxClose.addEventListener("click", closeLightbox);
  lightbox.addEventListener("click", (e) => {
    if (e.target === lightbox) closeLightbox();
  });

  function closeLightbox() {
    lightbox.classList.remove("show");
  }

  // Keyboard support
  document.addEventListener("keydown", (e) => {
    if (lightbox.classList.contains("show")) {
      if (e.key === "ArrowRight") lightboxNext.click();
      if (e.key === "ArrowLeft") lightboxPrev.click();
      if (e.key === "Escape") closeLightbox();
    }
  });
});



document.addEventListener("DOMContentLoaded", () => {
  const counters = document.querySelectorAll(".map-bubble .count");
  const section = document.querySelector(".map-wrapper");

  const animateCount = (el, target) => {
    let count = 0;
    const step = Math.ceil(target / 60);
    const timer = setInterval(() => {
      count += step;
      if (count >= target) {
        count = target;
        clearInterval(timer);
      }
      el.textContent = count + "+";
    }, 20);
  };

  const observer = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) {
      counters.forEach(c => {
        const target = parseInt(c.textContent);
        animateCount(c, target);
      });
      observer.disconnect();
    }
  }, { threshold: 0.3 });

  observer.observe(section);
});
