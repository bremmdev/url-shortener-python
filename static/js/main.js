function handleCopyUrl() {
  showToast("Copied to clipboard!");
  const shortenedLink = document.getElementById("short-link").href;
  void navigator.clipboard.writeText(shortenedLink);
}

function showToast(message) {
  const toast = document.getElementById("toast");
  const toastMessage = document.getElementById("toast-message");
  toastMessage.innerText = message;
  toast.classList.remove("hidden");
  hideToast(3000);
}

function hideToast(delay = 0) {
  const toast = document.getElementById("toast");
  setTimeout(() => {
    toast.classList.add("hidden");
  }, delay);
}

function showTooltip() {
  console.log('tooltip')
  const tooltip = document.getElementById("tooltip");
  tooltip.classList.remove("hidden");
}

function hideTooltip() {
  const tooltip = document.getElementById("tooltip");
  tooltip.classList.add("hidden");
}