// Searchable suggestions for the franchise and player fields.
// This replaces native datalist popups, which vary across mobile browsers.
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-autocomplete]").forEach((widget) => {
    const input = widget.querySelector('input[role="combobox"]');
    const list = widget.querySelector('[role="listbox"]');
    const options = Array.from(list.querySelectorAll('[role="option"]'));
    const emptyMessage = document.createElement("div");
    emptyMessage.className = "suggestion-empty";
    emptyMessage.setAttribute("role", "status");
    emptyMessage.textContent = "No matches found.";
    emptyMessage.hidden = true;
    list.append(emptyMessage);

    let visibleOptions = [];
    let activeIndex = -1;

    function setActive(index) {
      activeIndex = index;
      options.forEach((option) => {
        const active = visibleOptions[activeIndex] === option;
        option.classList.toggle("is-active", active);
        option.setAttribute("aria-selected", String(active));
      });

      if (activeIndex >= 0 && visibleOptions[activeIndex]) {
        input.setAttribute("aria-activedescendant", visibleOptions[activeIndex].id);
        visibleOptions[activeIndex].scrollIntoView({ block: "nearest" });
      } else {
        input.removeAttribute("aria-activedescendant");
      }
    }

    function closeList() {
      list.hidden = true;
      input.setAttribute("aria-expanded", "false");
      setActive(-1);
    }

    function filterOptions() {
      const query = input.value.trim().toLocaleLowerCase();
      visibleOptions = options.filter((option) => {
        const searchableText = `${option.dataset.search || ""} ${option.dataset.value || ""}`;
        const matches = searchableText.toLocaleLowerCase().includes(query);
        option.hidden = !matches;
        return matches;
      });

      emptyMessage.hidden = visibleOptions.length > 0;
      list.hidden = false;
      input.setAttribute("aria-expanded", "true");
      setActive(-1);
    }

    function choose(option) {
      input.value = option.dataset.value;
      closeList();
      input.focus();
    }

    options.forEach((option, index) => {
      option.id = `${list.id}-option-${index}`;
      option.addEventListener("mousedown", (event) => event.preventDefault());
      option.addEventListener("click", () => choose(option));
    });

    input.addEventListener("focus", filterOptions);
    input.addEventListener("input", filterOptions);

    input.addEventListener("keydown", (event) => {
      if (event.key === "ArrowDown" || event.key === "ArrowUp") {
        if (list.hidden) filterOptions();
        if (visibleOptions.length === 0) return;
        event.preventDefault();
        const direction = event.key === "ArrowDown" ? 1 : -1;
        if (activeIndex < 0) {
          setActive(direction === 1 ? 0 : visibleOptions.length - 1);
        } else {
          const nextIndex = activeIndex + direction;
          setActive((nextIndex + visibleOptions.length) % visibleOptions.length);
        }
      } else if (event.key === "Enter" && !list.hidden && activeIndex >= 0) {
        event.preventDefault();
        choose(visibleOptions[activeIndex]);
      } else if (event.key === "Escape") {
        closeList();
      }
    });

    input.addEventListener("blur", () => {
      window.setTimeout(closeList, 120);
    });

    document.addEventListener("pointerdown", (event) => {
      if (!widget.contains(event.target)) closeList();
    });
  });
});
