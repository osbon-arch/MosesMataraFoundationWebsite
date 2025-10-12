document.addEventListener("DOMContentLoaded", () => {
  const nav = document.getElementById("mainNav");

  // Navbar scroll effect
  const handleNavScroll = () => {
    if (window.scrollY > window.innerHeight - 80) {
      nav.classList.add("scrolled");
    } else {
      nav.classList.remove("scrolled");
    }
  };

  window.addEventListener("scroll", handleNavScroll);
  handleNavScroll(); // run on load in case page is already scrolled

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
