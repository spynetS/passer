document.addEventListener("DOMContentLoaded", async () => {
  const saltEl = document.getElementById("salt");
  const saveBtn = document.getElementById("save");

  const { salt } = await browser.storage.local.get({ salt: "" });
  saltEl.value = salt;

  saveBtn.addEventListener("click", async () => {
    await browser.storage.local.set({ salt: saltEl.value || "" });
  });
});
