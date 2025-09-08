// Utility: SHA-256 using Web Crypto
async function sha256(str) {
  const enc = new TextEncoder();
  const buf = await crypto.subtle.digest("SHA-256", enc.encode(str));
  return new Uint8Array(buf); // 32 bytes
}

// Build alphabet from selected options
function buildAlphabet(opts) {
  const lower = "abcdefghijklmnopqrstuvwxyz";
  const upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  const digits = "0123456789";
  const special = "!\"#$%&'()*+,-./:;<=>?@[\\]^_{|}~";
  let alphabet = "";
  if (opts.useLower) alphabet += lower;
  if (opts.useUpper) alphabet += upper;
  if (opts.useDigits) alphabet += digits;
  if (opts.useSpecial) alphabet += special;
  return alphabet;
}

// Deterministic mapping: bytes -> alphabet
function mapBytesToAlphabet(bytes, alphabet, length) {
  if (!alphabet) throw new Error("Alphabet is empty (choose at least one set).");
  const out = [];
  for (let i = 0; i < bytes.length && out.length < length; i++) {
    const idx = bytes[i] % alphabet.length;
    out.push(alphabet[idx]);
  }
  return out.join("");
}

async function generatePassword(pas, salt, opts) {
  const encoder = new TextEncoder();
  const data = encoder.encode(pas+salt);

  const hashBuffer = await crypto.subtle.digest('SHA-256', data);

  if (opts.legacy) {
    // Return hex digest (like Python's hexdigest)
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

  const digest = new Uint8Array(hashBuffer);

  const alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';  // Define your alphabet here

  const chars = Array.from(digest).map(byte => {
    return alphabet[byte % alphabet.length];
  });

  return chars.join('');
}

document.addEventListener("DOMContentLoaded", async () => {
  const masterEl = document.getElementById("master");
  const lengthEl = document.getElementById("length");
  const useLowerEl = document.getElementById("useLower");
  const useUpperEl = document.getElementById("useUpper");
  const useDigitsEl = document.getElementById("useDigits");
  const useSpecialEl = document.getElementById("useSpecial");
  const resultEl = document.getElementById("result");
  const generateBtn = document.getElementById("generate");
  const copyBtn = document.getElementById("copy");
  const legacyEl = document.getElementById("legacy");

  const saved = await browser.storage.local.get({
    length: 25, useLower: true, useUpper: true, useDigits: true, useSpecial: true, useLegacy: false
  });
  lengthEl.value = saved.length;
  useLowerEl.checked = saved.useLower;
  useUpperEl.checked = saved.useUpper;
  useDigitsEl.checked = saved.useDigits;
  useSpecialEl.checked = saved.useSpecial;
  legacyEl.checked = saved.useLegacy;

  async function runGenerate() {
    try {
      const master = masterEl.value || "";
      const opts = {
        length: Math.max(4, Math.min(128, parseInt(lengthEl.value || "25", 10))),
        useLower: useLowerEl.checked,
        useUpper: useUpperEl.checked,
        useDigits: useDigitsEl.checked,
        useSpecial: useSpecialEl.checked
        ueseLegacy: useLegacy.checked
      };
      await browser.storage.local.set(opts);
      const { salt } = await browser.storage.local.get({ salt: "" });
      const pwd = await generatePassword(master, salt, opts);
      resultEl.value = pwd.slice(0, opts.length);
    } catch (e) {
      console.error(e);
      resultEl.value = "Error: " + e.message;
    }
  }

  generateBtn.addEventListener("click", runGenerate);

  copyBtn.addEventListener("click", async () => {
    if (!resultEl.value) return;
    try {
      await navigator.clipboard.writeText(resultEl.value);
    } catch (e) {
      resultEl.select();
      document.execCommand("copy");
    }
  });
});
