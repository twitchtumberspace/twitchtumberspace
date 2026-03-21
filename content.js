const TARGET_DOMAIN = "deine-domain.tld";
const JOIN_TEXT = "join";
const CANDIDATE_SELECTORS = [
  "button",
  "a",
  "[role='button']",
  "[role='link']",
  "[class*='chat']",
  "[class*='join']",
  "[data-testid*='join']"
];

console.log("[join-extension] Script loaded", {
  targetDomain: TARGET_DOMAIN,
  currentHostname: window.location.hostname,
});

if (window.location.hostname === TARGET_DOMAIN) {
  console.log("[join-extension] Hostname matches target domain, starting scan.");
  findAndJoin();
} else {
  console.log("[join-extension] Hostname does not match target domain, skipping.");
}

function findAndJoin() {
  console.log("[join-extension] Searching for a join element.");

  const elements = Array.from(
    document.querySelectorAll(CANDIDATE_SELECTORS.join(","))
  );

  const matchingElement = elements.find((element) => {
    const text = (element.textContent || "").trim().toLowerCase();
    const className = (element.className || "").toString().toLowerCase();
    const style = window.getComputedStyle(element);
    const looksGreen =
      style.color.includes("0, 128, 0") ||
      style.backgroundColor.includes("0, 128, 0") ||
      className.includes("green");
    const hasJoinText = text.includes(JOIN_TEXT);
    const likelyJoinTarget = hasJoinText || (looksGreen && className.includes("join"));

    return likelyJoinTarget && isVisibleAndClickable(element);
  });

  if (matchingElement) {
    console.log("[join-extension] Join element found, clicking.", matchingElement);
    matchingElement.click();
    return;
  }

  console.log("[join-extension] No matching join element found.");
}

function isVisibleAndClickable(element) {
  if (!(element instanceof HTMLElement)) {
    return false;
  }

  const style = window.getComputedStyle(element);
  const rect = element.getBoundingClientRect();
  const visible =
    style.display !== "none" &&
    style.visibility !== "hidden" &&
    style.opacity !== "0" &&
    rect.width > 0 &&
    rect.height > 0;
  const enabled = !element.hasAttribute("disabled") && style.pointerEvents !== "none";

  return visible && enabled;
}
