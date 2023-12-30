/**********GLOBAL ERRORS ***********/
document.addEventListener("htmx:afterRequest", function (event) {
  if (event.detail.xhr.status === 500) {
    document.getElementById("error").innerHTML =
      "Something went wrong, please try again later.";
  } else {
    //clear any existing errors
    if (document.getElementById("error") !== null) {
      document.getElementById("error").innerHTML = "";
    }
  }
});

document.addEventListener("htmx:beforeRequest", function (event) {
  if (event.detail.pathInfo.requestPath === "/shorten") {
    document.getElementById("error").innerHTML = "";
  }
});

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
  const tooltip = document.getElementById("tooltip");
  tooltip.classList.remove("hidden");
}

function hideTooltip() {
  const tooltip = document.getElementById("tooltip");
  tooltip.classList.add("hidden");
}
